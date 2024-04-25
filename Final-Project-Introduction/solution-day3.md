## Cloudformation template to create Docker Swarm Stack

```yaml
AWSTemplateFormatVersion: 2010-09-09

Description: >
  This Cloudformation Template creates an infrastructure for Docker Swarm
  with five EC2 Instances with Amazon Linux 2. Instances are configured
  with custom security group allowing SSH (22), HTTP (80) UDP (4789, 7946), 
  and TCP(2377, 7946, 8080) connections from anywhere.
  User needs to select appropriate key name when launching the template.

Parameters:
  KeyPairName:
    Description: Enter the name of your Key Pair for SSH connections.
    Type: AWS::EC2::KeyPair::KeyName
    ConstraintDescription: Must one of the existing EC2 KeyPair

Resources:  
  RoleEnablingEC2forECR:
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
  EC2Profile:
    Type: "AWS::IAM::InstanceProfile"
    Properties:
      Roles: #required
        - !Ref RoleEnablingEC2forECR
  DockerMachinesSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Enable SSH and HTTP for Docker Machines
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 2377
          ToPort: 2377
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 7946
          ToPort: 7946
          CidrIp: 0.0.0.0/0
        - IpProtocol: udp
          FromPort: 7946
          ToPort: 7946
          CidrIp: 0.0.0.0/0
        - IpProtocol: udp
          FromPort: 4789
          ToPort: 4789
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 8080
          ToPort: 8080
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 8088
          ToPort: 8088
          CidrIp: 0.0.0.0/0
        - IpProtocol: tcp
          FromPort: 5432
          ToPort: 5432
          CidrIp: 0.0.0.0/0
  DockerMachineLT:
    Type: "AWS::EC2::LaunchTemplate"
    Properties:
      LaunchTemplateData:
        ImageId: ami-0947d2ba12ee1ff75
        InstanceType: t3.small
        KeyName: !Ref KeyPairName
        IamInstanceProfile: 
          Arn: !GetAtt EC2Profile.Arn
        SecurityGroupIds:
          - !GetAtt DockerMachinesSecurityGroup.GroupId
        TagSpecifications: 
          - ResourceType: instance
            Tags: 
              - Key: app-stack-name
                Value: !Sub ${AWS::StackName}
              - Key: environment
                Value: dev
  DockerInstance1:
    Type: AWS::EC2::Instance
    DependsOn:
        - "DockerInstance2"
    Properties:
      LaunchTemplate:
        LaunchTemplateId: !Ref DockerMachineLT
        Version: !GetAtt DockerMachineLT.LatestVersionNumber
      Tags:                
        - Key: server
          Value: docker-instance-1                       
        - Key: swarm-role
          Value: grand-master                       
        - Key: Name
          Value: !Sub ${AWS::StackName} Docker Machine 1st        
  DockerInstance2:
    Type: AWS::EC2::Instance
    Properties:
      LaunchTemplate:
        LaunchTemplateId: !Ref DockerMachineLT
        Version: !GetAtt DockerMachineLT.LatestVersionNumber
      Tags:                
        - Key: server
          Value: docker-instance-2                       
        - Key: swarm-role
          Value: manager                       
        - Key: Name
          Value: !Sub ${AWS::StackName} Docker Machine 2nd
  DockerInstance3:
    Type: AWS::EC2::Instance
    Properties:
      LaunchTemplate:
        LaunchTemplateId: !Ref DockerMachineLT
        Version: !GetAtt DockerMachineLT.LatestVersionNumber
      Tags:                
        - Key: server
          Value: docker-instance-3                       
        - Key: swarm-role
          Value: manager                       
        - Key: Name
          Value: !Sub ${AWS::StackName} Docker Machine 3rd
  DockerInstance4:
    Type: AWS::EC2::Instance
    Properties:
      LaunchTemplate:
        LaunchTemplateId: !Ref DockerMachineLT
        Version: !GetAtt DockerMachineLT.LatestVersionNumber
      Tags:                
        - Key: server
          Value: docker-instance-4                       
        - Key: swarm-role
          Value: worker                       
        - Key: Name
          Value: !Sub ${AWS::StackName} Docker Machine 4th
  DockerInstance5:
    Type: AWS::EC2::Instance
    Properties:
      LaunchTemplate:
        LaunchTemplateId: !Ref DockerMachineLT
        Version: !GetAtt DockerMachineLT.LatestVersionNumber
      Tags:                
        - Key: server
          Value: docker-instance-5                       
        - Key: swarm-role
          Value: worker                       
        - Key: Name
          Value: !Sub ${AWS::StackName} Docker Machine 5th
Outputs:
  1stDockerInstanceDNSName:
    Description: 1st Docker Instance DNS Name
    Value: !Sub 
      - ${PublicAddress}
      - PublicAddress: !GetAtt DockerInstance1.PublicDnsName
  2ndDockerInstanceDNSName:
    Description: 2nd Docker Instance DNS Name
    Value: !Sub 
      - ${PublicAddress}
      - PublicAddress: !GetAtt DockerInstance2.PublicDnsName
  3rdDockerInstanceDNSName:
    Description: 3rd Docker Instance DNS Name
    Value: !Sub 
      - ${PublicAddress}
      - PublicAddress: !GetAtt DockerInstance3.PublicDnsName
  4thDockerInstanceDNSName:
    Description: 4th Docker Instance DNS Name
    Value: !Sub 
      - ${PublicAddress}
      - PublicAddress: !GetAtt DockerInstance4.PublicDnsName
  5thDockerInstanceDNSName:
    Description: 5th Docker Instance DNS Name
    Value: !Sub 
      - ${PublicAddress}
      - PublicAddress: !GetAtt DockerInstance5.PublicDnsName
```
## Create Docker Swarm stack using Jenkins Freestyle Job on excute shell build section

- this code uses aws cloudformation deploy command

```sh
PATH="$PATH:/usr/local/bin"
CFN_KEYPAIR="project-key-1"
AWS_REGION="us-east-1"
APP_NAME="car-rental"
APP_STACK_NAME="$APP_NAME-App-${BUILD_NUMBER}"
aws cloudformation deploy  --template-file ./infrastructure/cfn-template.yaml \
--stack-name ${APP_STACK_NAME} --parameter-overrides KeyPairName=${CFN_KEYPAIR} --capabilities CAPABILITY_IAM
```

- this code uses aws cloudformation create-stack command

```sh
PATH="$PATH:/usr/local/bin"
APP_NAME="car-rental"
APP_STACK_NAME="$APP_NAME-App-${BUILD_NUMBER}"
CFN_KEYPAIR="my-cfn-key.pem"
CFN_TEMPLATE="./infrastructure/docker-swarm-infrastructure-cfn-template.yml"
AWS_REGION="us-east-1"
aws cloudformation create-stack --region ${AWS_REGION} --stack-name ${APP_STACK_NAME} --capabilities CAPABILITY_IAM --template-body file://${CFN_TEMPLATE} --parameters ParameterKey=KeyPairName,ParameterValue=${CFN_KEYPAIR}
```


- modify ansible hosts.ini file after creation of stack

```ini
172.31.86.88 ansible_user=ec2-user  
172.31.85.8 ansible_user=ec2-user
172.31.80.171  ansible_user=ec2-user
172.31.84.183  ansible_user=ec2-user
172.31.89.248 ansible_user=ec2-user
```

- ping hosts using static inventory file

```sh
PATH="$PATH:/usr/local/bin"
CFN_KEYPAIR="my-project-key"
export ANSIBLE_INVENTORY="${WORKSPACE}/ansible/inventory/hosts.ini"
export ANSIBLE_PRIVATE_KEY_FILE="${WORKSPACE}/${CFN_KEYPAIR}"
export ANSIBLE_HOST_KEY_CHECKING=False
ansible all -m ping
```
