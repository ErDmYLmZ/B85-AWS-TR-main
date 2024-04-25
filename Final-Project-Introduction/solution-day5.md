## Create .ssh folder under Jenkins home and move the key file to this folder

```shell
mkdir -p ${JENKINS_HOME}/.ssh
mv my-cfn-key ${JENKINS_HOME}/.ssh/my-cfn-key
```

## Create a Jenkinsfile for Docker Swarm Cluster Creation and Configuration

```Jenkinsfile
pipeline {
    agent any
    environment {
        PATH=sh(script:"echo $PATH:/usr/local/bin", returnStdout:true).trim()
        APP_NAME="car-rental"
        APP_STACK_NAME="$APP_NAME-App-ver-${BUILD_NUMBER}"
        AWS_REGION="us-east-1"
        CFN_KEYPAIR="my-cfn-key"
        CFN_TEMPLATE="./infrastructure/cfn-template.yaml"
        ANSIBLE_PRIVATE_KEY_FILE="${JENKINS_HOME}/.ssh/${CFN_KEYPAIR}"
        ANSIBLE_HOST_KEY_CHECKING="False"
    }
    stages {
        stage('Create Infrastructure') {
            steps {
                echo 'Creating Infrastructure for Automation Environment with Cloudfomation'
                sh "aws cloudformation deploy --template-file ./infrastructure/cfn-template.yaml --stack-name ${APP_STACK_NAME} --parameter-overrides KeyPairName=${CFN_KEYPAIR} --capabilities CAPABILITY_IAM"
                
            }
        }

        stage('Create Docker Swarm  Environment') {
            steps {

                echo "Setup Docker Swarm for  Automation Build for ${APP_NAME} App"
                echo "Update dynamic environment"
                sh "sed -i 's/APP_STACK_NAME/${APP_STACK_NAME}/' ./ansible/inventory/dynamic_inventory_aws_ec2.yaml"
                echo "Swarm Setup for all nodes (instances)"
                sh "ansible-playbook -i ./ansible/inventory/dynamic_inventory_aws_ec2.yaml -b ./ansible/playbooks/setup_for_all_docker_swarm_instances.yaml"
                echo "Swarm Setup for Grand Master node"
                sh "ansible-playbook -i ./ansible/inventory/dynamic_inventory_aws_ec2.yaml -b ./ansible/playbooks/initialize_docker_swarm.yaml"
                echo "Swarm Setup for Other Managers nodes"
                sh "ansible-playbook -i ./ansible/inventory/dynamic_inventory_aws_ec2.yaml -b ./ansible/playbooks/join_docker_swarm_managers.yaml"
                echo "Swarm Setup for Workers nodes"
                sh "ansible-playbook -i ./ansible/inventory/dynamic_inventory_aws_ec2.yaml -b ./ansible/playbooks/join_docker_swarm_workers.yaml"
            }
        }
    }
    post {
        failure {
            echo 'Tear down the Docker Swarm infrastructure using AWS CLI'
            sh "aws cloudformation delete-stack --region ${AWS_REGION} --stack-name ${APP_STACK_NAME}"
        }
    }
}
```


## Create an Ansible playbook file to deploy app on cluster

```deploy_app_on_docker_swarm.yaml
---
- hosts: role_grand_master
  tasks:
  - name: Copy docker compose file to grand master
    copy:
      src: "{{ workspace }}/docker-compose-swarm-tagged.yml"
      dest: /home/ec2-user/docker-compose-swarm-tagged.yml

  - name: get login credentials for ecr
    shell: "export PATH=$PATH:/usr/local/bin/ && aws ecr get-login-password --region {{ aws_region }} | docker login --username AWS --password-stdin {{ ecr_registry }}"

  - name: deploy the app stack on swarm
    shell: "docker stack deploy --with-registry-auth -c /home/ec2-user/docker-compose-swarm-tagged.yml {{ app_name }}"
    register: output

  - debug: msg="{{ output.stdout }}"
```


## Create a docker compose swarm file

```docker-compose-swarm.yml
version: '3'
services:
  ui:
    image: "${IMAGE_TAG_UI}"
    deploy:
      replicas: 3
      update_config:
          parallelism: 2
          delay: 5s
          order: start-first
    depends_on:
      - app
      - db
    links: 
      - "app"  
    ports:
      - "80:3000"
    environment: 
      - APP_URL=http://52.90.8.65:8080/car-rental/api/
    networks:
      - carrental-net
  app:
    image: "${IMAGE_TAG_API}"
    deploy:
      replicas: 3
      update_config:
          parallelism: 2
          delay: 5s
          order: start-first
    depends_on:
      - db
    links:
      - "db" 
    ports:
      - "8080:8080"
    restart: always
    environment:
      - DATABASE_URL=jdbc:postgresql://db:5432/carrental
    networks:
      - carrental-net
          
  db:
    image: 'postgres:13.1-alpine'
    container_name: postgres
    environment:
      - POSTGRES_USER=techprodb_user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=carrental

    ports:
      - "5432:5432"
    volumes:
      - db-data:/var/lib/postgresql/data/
    networks:
      - carrental-net

volumes:
    db-data:
networks:
    carrental-net:
        driver: overlay
```


## Create a Jenkinsfile for application deployment

```Jenkinsfile-app-deploy
pipeline {
    agent any
    environment {
        PATH=sh(script:"echo $PATH:/usr/local/bin", returnStdout:true).trim()
        APP_NAME="car-rental"
        APP_STACK_NAME="car-rental-App-ver-2"
        APP_REPO_NAME="techproeducation-car-rental"
        AWS_ACCOUNT_ID=sh(script:'export PATH="$PATH:/usr/local/bin" && aws sts get-caller-identity --query Account --output text', returnStdout:true).trim()
        AWS_REGION="us-east-1"
        ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        CFN_KEYPAIR="my-cfn-key"
        ANSIBLE_PRIVATE_KEY_FILE="${JENKINS_HOME}/.ssh/${CFN_KEYPAIR}"
        ANSIBLE_HOST_KEY_CHECKING="False"
    }
    stages {
        stage('Prepare Tags for Docker Images') {
            steps {
                echo 'Preparing Tags for Docker Images'
                script {
                    env.IMAGE_TAG_UI="${ECR_REGISTRY}/${APP_REPO_NAME}:frontend-ver-${BUILD_NUMBER}"
                    env.IMAGE_TAG_API="${ECR_REGISTRY}/${APP_REPO_NAME}:backend-ver-${BUILD_NUMBER}"
                }
            }
        }
        stage('Build App Docker Images') {
            steps {
                echo 'Building App Dev Images'
                sh """
                  docker build --force-rm -t "${IMAGE_TAG_UI}" "${WORKSPACE}/bluerentalcars-frontend"
                  docker build --force-rm -t "${IMAGE_TAG_API}" "${WORKSPACE}/bluerentalcars-backend"
                  docker image ls
                """
            }
        }
        stage('Push Images to ECR Repo') {
            steps {
                echo "Pushing ${APP_NAME} App Images to ECR Repo"
                sh """
                  aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY} 
                  docker push "${IMAGE_TAG_UI}"
                  docker push "${IMAGE_TAG_API}"
                """
             }
        }
        stage('Deploy App on Docker Swarm'){
            steps {
                echo 'Deploying App on Swarm'
                sh """
                  sed -i "s/APP_STACK_NAME/${APP_STACK_NAME}/" ./ansible/inventory/dynamic_inventory_aws_ec2.yaml
                  envsubst < docker-compose-swarm.yml > docker-compose-swarm-tagged.yml
                  ansible-playbook -i ./ansible/inventory/dynamic_inventory_aws_ec2.yaml -b --extra-vars "workspace=${WORKSPACE} app_name=${APP_NAME} aws_region=${AWS_REGION} ecr_registry=${ECR_REGISTRY}" ./ansible/playbooks/deploy_app_on_docker_swarm.yaml
                """
            }
        }
    }
    post {
        always {
            echo 'Deleting all local images'
            sh 'docker image prune -af'
        }
    }
}
```
