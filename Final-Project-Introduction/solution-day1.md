## Terraform to create development environment

terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.11.0"
    }
    
  }
}

resource "aws_instance" "tf-car-rental" {
  ami = "ami-0f9fc25dd2506cf6d"
  instance_type = "t2.small"
  key_name = "ubuntunv"
  #security_groups = ["car-rental-Sec-Gr"]
  vpc_security_group_ids = [aws_security_group.car-rental-Sec-Gr.id]
  tags = {
    Name = "Web Server of car-rental"
  }

  user_data = <<-EOF
          #! /bin/bash
          yum update -y
          yum install git -y
          amazon-linux-extras install docker -y
          systemctl start docker
          systemctl enable docker
          usermod -a -G docker ec2-user
          newgrp docker
          curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" \
          -o /usr/local/bin/docker-compose
          chmod +x /usr/local/bin/docker-compose
          EOF

  
}

resource "aws_security_group" "car-rental-Sec-Gr" {
  name = "car-rental-Sec-Gr"
  tags = {
    Name = "car-rental-Sec-Gr"
  }
  ingress {
    from_port = 80
    protocol = "tcp"
    to_port = 80
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 8080
    protocol = "tcp"
    to_port = 8080
    cidr_blocks = ["0.0.0.0/0"]
   }
  ingress {
    from_port = 3000
    protocol = "tcp"
    to_port = 3000
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 5432
    protocol = "tcp"
    to_port = 5432
    cidr_blocks = ["0.0.0.0/0"]
   }
  ingress {
    from_port = 22
    protocol = "tcp"
    to_port = 22
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    protocol = "-1"
    to_port = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "website" {
  value = "http://${aws_instance.tf-car-rental.public_dns}"

}

## Terraform to create github repo and dev env

terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "4.11.0"
    }
    github = {
      source = "integrations/github"
      version = "4.23.0"
    }
  }
}

provider "aws" {
  # Configuration options
}

provider "github" {
  # Configuration options
  token = "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"
}

resource "github_repository" "myrepo" {
  name = "car-rental-repo"
  auto_init = true
  visibility = "private"
}

resource "github_branch_default" "main" {
  branch = "main"
  repository = github_repository.myrepo.name
}


resource "aws_instance" "tf-car-rental" {
  ami = "ami-0f9fc25dd2506cf6d"
  instance_type = "t3a.medium"
  key_name = "mykey"
  security_groups = ["car-rental-SG"]
  tags = {
    Name = "Web Server of car-rental"
  }

  user_data = <<-EOF
          #! /bin/bash
          yum update -y
          yum install git -y
          amazon-linux-extras install docker -y
          systemctl start docker
          systemctl enable docker
          usermod -a -G docker ec2-user
          curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" \
          -o /usr/local/bin/docker-compose
          chmod +x /usr/local/bin/docker-compose
          EOF

  depends_on = [github_repository.myrepo]
}

resource "aws_security_group" "car-rental-SG" {
  name = "car-rental-SG"
  tags = {
    Name = "car-rental-SG"
  }
  ingress {
    from_port = 80
    protocol = "tcp"
    to_port = 80
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 8080
    protocol = "tcp"
    to_port = 8080
    cidr_blocks = ["0.0.0.0/0"]
   }
  ingress {
    from_port = 3000
    protocol = "tcp"
    to_port = 3000
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 5432
    protocol = "tcp"
    to_port = 5432
    cidr_blocks = ["0.0.0.0/0"]
   }
  ingress {
    from_port = 22
    protocol = "tcp"
    to_port = 22
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    protocol = "-1"
    to_port = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "website" {
  value = "http://${aws_instance.tf-car-rental.public_dns}"

}

## Dockerfile for frontend

- consider node version substitution node:16.18

FROM node:14 
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm","start"]

## Dockerfile for backend

FROM maven:3.8.1-openjdk-11-slim AS build
RUN mkdir -p workspace
WORKDIR /workspace
COPY pom.xml /workspace/
COPY src /workspace/src
RUN mvn clean package -DskipTests

FROM adoptopenjdk:11-jre-hotspot
COPY --from=build /workspace/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","app.jar"]

## docker-compose.yaml

version: '3'

services:
  ui:
    image: 'bluerentalcars-frontend:latest'
    build:
      context: ./bluerentalcars-frontend
    container_name: brc-frontend
    depends_on:
      - app
      - db
    links: 
      - "app"  
    ports:
      - "80:3000"
    environment: 
      - APP_URL=http://localhost:8080/car-rental/api/
    networks:
      - carrental-net
  app:
    image: 'bluerentalcars-backend:latest'
    build:
      context: ./bluerentalcars-backend
    container_name: brc-backend
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
        driver: bridge


## Cloudformation template for Jenkins Server

AWSTemplateFormatVersion: 2010-09-09

Description: >
  This Cloudformation Template creates a Jenkins Server using JDK 11 on EC2 Instance.
  Jenkins Server is enabled with Git, Docker and Docker Compose,
  AWS CLI Version 2, Python 3, Ansible, and Boto3. 
  Jenkins Server will run on Amazon Linux 2 EC2 Instance with
  custom security group allowing HTTP(80, 8080) and SSH (22) connections from anywhere.

Parameters:
  KeyPairName:
    Description: Enter the name of your Key Pair for SSH connections.
    Type: AWS::EC2::KeyPair::KeyName
    ConstraintDescription: Must one of the existing EC2 KeyPair
Resources:
  EmpoweringRoleforJenkinsServer:
    Type: "AWS::IAM::Role"
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
        - arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess
        - arn:aws:iam::aws:policy/AWSCloudFormationFullAccess
        - arn:aws:iam::aws:policy/AdministratorAccess
  JenkinsServerEC2Profile:
    Type: "AWS::IAM::InstanceProfile"
    Properties:
      Roles: #required
        - !Ref EmpoweringRoleforJenkinsServer
  JenkinsServerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
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
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-087c17d1fe0178315
      InstanceType: t3.small
      KeyName: !Ref KeyPairName
      IamInstanceProfile: !Ref JenkinsServerEC2Profile
      SecurityGroupIds:
        - !GetAtt JenkinsServerSecurityGroup.GroupId
      Tags:                
        - Key: Name
          Value: !Sub Jenkins Server of ${AWS::StackName}
        - Key: server
          Value: jenkins
      UserData:
        Fn::Base64: |
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
          wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat/jenkins.repo
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
          cp /lib/systemd/system/docker.service /lib/systemd/system/docker.service.bak
          sed -i 's/^ExecStart=.*/ExecStart=\/usr\/bin\/dockerd -H tcp:\/\/127.0.0.1:2375 -H unix:\/\/\/var\/run\/docker.sock/g' /lib/systemd/system/docker.service
          systemctl daemon-reload
          systemctl restart docker
          systemctl restart jenkins
          # install docker compose
          curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-$(uname -s)-$(uname -m)" \
          -o /usr/local/bin/docker-compose
          chmod +x /usr/local/bin/docker-compose
          # uninstall aws cli version 1
          rm -rf /bin/aws
          # install aws cli version 2
          curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
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
      - ${PublicAddress}
      - PublicAddress: !GetAtt JenkinsServer.PublicDnsName
  JenkinsURL:
    Description: Jenkins Server URL
    Value: !Sub 
      - http://${PublicAddress}:8080
      - PublicAddress: !GetAtt JenkinsServer.PublicDnsName


