## Cloudformation template to set Jenkins Server EBS storage to 10gb

AWSTemplateFormatVersion: 2010-09-09
Description: >
  This Cloudformation Template creates a Jenkins Server using JDK 11 on EC2
  Instance. Jenkins Server is enabled with Git, Docker and Docker Compose, AWS
  CLI Version 2, Python 3, Ansible, and Boto3.  Jenkins Server will run on
  Amazon Linux 2 EC2 Instance with custom security group allowing HTTP(80, 8080)
  and SSH (22) connections from anywhere.
Parameters:
  KeyPairName:
    Description: Enter the name of your Key Pair for SSH connections.
    Type: 'AWS::EC2::KeyPair::KeyName'
    ConstraintDescription: Must one of the existing EC2 KeyPair
Resources:
  EmpoweringRoleforJenkinsServer:
    Type: 'AWS::IAM::Role'
    Properties:
      AssumeRolePolicyDocument:
        Statement:
          - Effect: Allow
            Principal:
              Service:
                - ec2.amazonaws.com
            Action:
              - 'sts:AssumeRole'
      ManagedPolicyArns:
        - 'arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess'
        - 'arn:aws:iam::aws:policy/AWSCloudFormationFullAccess'
        - 'arn:aws:iam::aws:policy/AdministratorAccess'
  JenkinsServerEC2Profile:
    Type: 'AWS::IAM::InstanceProfile'
    Properties:
      Roles:
        - !Ref EmpoweringRoleforJenkinsServer
  JenkinsServerSecurityGroup:
    Type: 'AWS::EC2::SecurityGroup'
    Properties:
      GroupDescription: Enable SSH and HTTP for Jenkins Server
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 8080
          ToPort: 8080
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 5432
          ToPort: 5432
          CidrIp: 0.0.0.0/0
  JenkinsServer:
    Type: 'AWS::EC2::Instance'
    Properties:
      ImageId: ami-087c17d1fe0178315
      InstanceType: t3.small
      KeyName: !Ref KeyPairName
      IamInstanceProfile: !Ref JenkinsServerEC2Profile
      BlockDeviceMappings:
        - DeviceName: "/dev/xvda"
          Ebs:
            VolumeType: gp2
            VolumeSize: 10
            
      SecurityGroupIds:
        - !GetAtt 
          - JenkinsServerSecurityGroup
          - GroupId
      Tags:
        - Key: Name
          Value: !Sub 'Jenkins Server of ${AWS::StackName}'
        - Key: server
          Value: jenkins
      UserData: !Base64 >
        #! /bin/bash

        # update os

        yum update -y

        # set server hostname as jenkins-server

        hostnamectl set-hostname jenkins-server

        # install git

        yum install git -y

        # install java 11

        yum install java-11-amazon-corretto -y

        # install jenkins

        wget -O /etc/yum.repos.d/jenkins.repo
        https://pkg.jenkins.io/redhat/jenkins.repo

        rpm --import https://pkg.jenkins.io/redhat/jenkins.io.key

        amazon-linux-extras install epel

        yum install jenkins -y

        systemctl daemon-reload

        systemctl start jenkins

        systemctl enable jenkins

        # install docker

        amazon-linux-extras install docker -y

        systemctl start docker

        systemctl enable docker

        usermod -a -G docker ec2-user

        usermod -a -G docker jenkins

        # configure docker as cloud agent for jenkins

        cp /lib/systemd/system/docker.service
        /lib/systemd/system/docker.service.bak

        sed -i 's/^ExecStart=.*/ExecStart=\/usr\/bin\/dockerd -H
        tcp:\/\/127.0.0.1:2375 -H unix:\/\/\/var\/run\/docker.sock/g'
        /lib/systemd/system/docker.service

        systemctl daemon-reload

        systemctl restart docker

        systemctl restart jenkins

        # install docker compose

        curl -L
        "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname
        -s)-$(uname -m)" \

        -o /usr/local/bin/docker-compose

        chmod +x /usr/local/bin/docker-compose

        # uninstall aws cli version 1

        rm -rf /bin/aws

        # install aws cli version 2

        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o
        "awscliv2.zip"

        unzip awscliv2.zip

        ./aws/install

        # install python 3

        yum install python3 -y

        # install ansible

        pip3 install ansible

        # install boto3

        pip3 install boto3
Outputs:
  JenkinsDNS:
    Description: Jenkins Server DNS Name
    Value: !Sub 
      - '${PublicAddress}'
      - PublicAddress: !GetAtt 
          - JenkinsServer
          - PublicDnsName
  JenkinsURL:
    Description: Jenkins Server URL
    Value: !Sub 
      - 'http://${PublicAddress}:8080'
      - PublicAddress: !GetAtt 
          - JenkinsServer
          - PublicDnsName

## AWS CLI command in shell execution on Jenkins Freestyle Job to create ECR repo

PATH="$PATH:/usr/local/bin"
APP_REPO_NAME="techproeducation-repo/car-rental"
AWS_REGION="us-east-1"

aws ecr create-repository \
  --repository-name ${APP_REPO_NAME} \
  --image-scanning-configuration scanOnPush=false \
  --image-tag-mutability MUTABLE \
  --region ${AWS_REGION}

## AWS CLI command in shell execution on Jenkins Freestyle Job to delete ECR repo

PATH="$PATH:/usr/local/bin"
APP_REPO_NAME="techproeducation-repo/car-rental"
AWS_REGION="us-east-1"

aws ecr delete-repository --repository-name ${APP_REPO_NAME} --force

## AWS CLI command in shell execution on Jenkins Freestyle Job to create key file

PATH="$PATH:/usr/local/bin"
CFN_KEYPAIR="my-cfn-key"
CFN_KEYPAIR_FILE="my-cfn-key.pem"
AWS_REGION="us-east-1"
aws ec2 create-key-pair --region ${AWS_REGION} --key-name ${CFN_KEYPAIR} --query "KeyMaterial" --output text > ${CFN_KEYPAIR_FILE}
chmod 400 ${CFN_KEYPAIR_FILE}