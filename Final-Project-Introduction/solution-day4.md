## Create dynamic inventory file

```dynamic_inventory_aws_ec2.yaml
plugin: aws_ec2
regions:
  - "us-east-1"
filters:
  tag:app-stack-name: APP_STACK_NAME
  tag:environment: dev
keyed_groups:
  - key: tags['app-stack-name']
    prefix: 'app_stack_'
    separator: ''
  - key: tags['swarm-role']
    prefix: 'role_'
    separator: ''
  - key: tags['environment']
    prefix: 'env_'
    separator: ''
  - key: tags['server']
    separator: ''
hostnames:
  - "private-ip-address"
compose:
  ansible_user: "'ec2-user'"
```

## Ping machines using dynamic inventory in Jenkins Freestyle job under execute shell

```shell
APP_NAME="car-rental"
CFN_KEYPAIR="my-cfn-key"
PATH="$PATH:/usr/local/bin"
export ANSIBLE_PRIVATE_KEY_FILE="${WORKSPACE}/${CFN_KEYPAIR}"
export ANSIBLE_HOST_KEY_CHECKING=False
export APP_STACK_NAME="$APP_NAME-App-22"
# Dev Stack
sed -i "s/APP_STACK_NAME/$APP_STACK_NAME/" ./ansible/inventory/dynamic_inventory_aws_ec2.yaml
cat ./ansible/inventory/dynamic_inventory_aws_ec2.yaml
ansible-inventory -v -i ./ansible/inventory/dynamic_inventory_aws_ec2.yaml --graph
ansible -i ./ansible/inventory/dynamic_inventory_aws_ec2.yaml all -m ping
```


## Prepare playbooks

```setup_for_all_docker_swarm_instances.yaml
---
- hosts: all
  tasks:
  - name: update os
    yum:
      name: '*'
      state: present
  - name: install docker
    command: amazon-linux-extras install docker=latest -y
  - name: start docker
    service:
      name: docker
      state: started
      enabled: yes
  - name: add ec2-user to docker group
    shell: "usermod -a -G docker ec2-user"
  - name: install docker compose.
    get_url:
      url: https://github.com/docker/compose/releases/download/1.26.2/docker-compose-Linux-x86_64
      dest: /usr/local/bin/docker-compose
      mode: 0755
  - name: uninstall aws cli v1
    file:
      path: /bin/aws
      state: absent
  - name: download awscliv2 installer
    unarchive:
      src: https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip
      dest: /tmp
      remote_src: yes
      creates: /tmp/aws
      mode: 0755
  - name: run the installer
    command:
    args:
      cmd: "/tmp/aws/install"
      creates: /usr/local/bin/aws
```


```initialize_docker_swarm.yaml
---
- hosts: role_grand_master
  tasks:
  - name: initialize docker swarm
    shell: docker swarm init
  - name: install git
    yum:
      name: git
      state: present
  - name: run the visualizer app for docker swarm
    shell: |
      docker service create \
        --name=viz \
        --publish=8088:8080/tcp \
        --constraint=node.role==manager \
        --mount=type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
        dockersamples/visualizer
```


```join_docker_swarm_managers.yaml
---
- hosts: role_grand_master
  tasks:
  - name: Get swarm join-token for managers
    shell: docker swarm join-token manager | grep -i 'docker'
    register: join_command_for_managers

  - debug: msg='{{ join_command_for_managers.stdout.strip() }}'
  
  - name: register grand_master with variable
    add_host:
      name: "grand_master"
      manager_join: "{{ join_command_for_managers.stdout.strip() }}"

- hosts: role_manager
  tasks:
  - name: Join managers to swarm
    shell: "{{ hostvars['grand_master']['manager_join'] }}"
    register: result_of_joining

  - debug: msg='{{ result_of_joining.stdout }}'
```


```join_docker_swarm_workers.yaml
---
- hosts: role_grand_master
  tasks:
  - name: Get swarm join-token for workers
    shell: docker swarm join-token worker | grep -i 'docker'
    register: join_command_for_workers

  - debug: msg='{{ join_command_for_workers.stdout.strip() }}'
  
  - name: register grand_master with variable
    add_host:
      name: "grand_master"
      worker_join: "{{ join_command_for_workers.stdout.strip() }}"

- hosts: role_worker
  tasks:
  - name: Join workers to swarm
    shell: "{{ hostvars['grand_master']['worker_join'] }}"
    register: result_of_joining

  - debug: msg='{{ result_of_joining.stdout }}'
```


## Run playbooks in Jenkins Freestyle job

```shell
APP_NAME="car-rental"
CFN_KEYPAIR="my-cfn-key"
PATH="$PATH:/usr/local/bin"
export ANSIBLE_PRIVATE_KEY_FILE="${WORKSPACE}/${CFN_KEYPAIR}"
export ANSIBLE_HOST_KEY_CHECKING=False
export APP_STACK_NAME="$APP_NAME-App-22"
sed -i "s/APP_STACK_NAME/$APP_STACK_NAME/" ./ansible/inventory/dynamic_inventory_aws_ec2.yaml
# Swarm Setup for all nodes (instances)
ansible-playbook -i ./ansible/inventory/dynamic_inventory_aws_ec2.yaml -b ./ansible/playbooks/setup_for_all_docker_swarm_instances.yaml
# Swarm Setup for Grand Master node
ansible-playbook -i ./ansible/inventory/dynamic_inventory_aws_ec2.yaml -b ./ansible/playbooks/initialize_docker_swarm.yaml
# Swarm Setup for Other Managers nodes
ansible-playbook -i ./ansible/inventory/dynamic_inventory_aws_ec2.yaml -b ./ansible/playbooks/join_docker_swarm_managers.yaml
# Swarm Setup for Workers nodes
ansible-playbook -i ./ansible/inventory/dynamic_inventory_aws_ec2.yaml -b ./ansible/playbooks/join_docker_swarm_workers.yaml
```

