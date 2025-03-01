# Hands-on EFS:

## Outline

- Part 1 - Prep(EC2 SecGrp, EFS SecGrp, EC2 Linux 2 Instance)

- Part 2 - Creating EFS

- Part 3 - Attach the EFS to the multiple EC2 Linux 2 instances


## Part 1 - Prep (EC2 SecGrp, EFS SecGrp, EC2 Linux 2 Instance)

### Step 1 - Create EC2 SecGrp:

- Open the Amazon EC2 console at https://console.aws.amazon.com/ec2/.

- Choose the Security Groups on left-hand menu

- Click the `Create Security Group`.

```text
Security Group Name  : InstancesSecGrp
Description          : SecGrp for EC2
VPC                  : Default VPC
Inbound Rules:
- Type: SSH ----> Source: 0.0.0.0/0
Outbound Rules: Keep it as default
Tag:
    - Key   : Name
      Value : EC2-SecGrp
```

### Step 2 - Create EFS SecGrp:

- Click the `Create Security Group`.

```text
Security Group Name  : EFS-SecGrp
Description          : SecGrp for EFS
VPC                  : Default VPC 
Inbound Rules:
- Type: NFS ----> Port: 2049 ------>Source: Custom: InstancesSecGrp # Yukarida olusturdugumuz bu
Outbound Rules: Keep it as default
Tag:
    - Key   : Name
      Value : EFS-SecGrp
```
```bash
# NFS(Network File Sharing) 2049 dosya erisimi icin kullanilir.
```

### Step 3 - Create EC2 :

- Configure First Instance in N.Virginia

```text
AMI             : Amazon Linux 2
Instance Type   : t2.micro
Network         : default
Subnet          : default
Security Group  : InstancesSecGrp
    Sec.Group Name :InstancesSecGrp
Tag             :
    Key         : Name
    Value       : EC2-1
```

- Configure Second Instance in N.Virginia

```text
AMI             : Amazon Linux 2
Instance Type   : t2.micro
Network         : default
Subnet          : default
Security Group  : InstancesSecGrp
    Sec.Group Name : InstancesSecGrp
Tag             :
    Key         : Name
    Value       : EC2-2
```

## Part 2 - Creating EFS

Open the Amazon EFS console at https://console.aws.amazon.com/efs/.

- Click "Create File System" 

```text

Name                            : myEFS
Virtual Private Cloud (VPC)     : Default VPC (Keep default)
Availability and Durability     : Regional (Keep default)
```

- To customize settings manually, select the "Customize" option seen at the bottom 

```text

General

Name                    : myEFS (Comes default from previous setting)

Availability and Durability : Regional (Comes default from previous setting)

Automatic backups       : Unchecked "Enable automatic backups"

Lifecycle management    : Select "None"

Performance mode        : General Purpose

Throughput mode         : Bursting

Encryption              : Enable encryption of data at rest

Tags                    : optional
```
Click Next

```text

- Virtual Private Cloud (VPC): Default VPC

- Mount targets: 
  - select all AZ (keep it default)
  - Clear "default sg" from all AZ
  - Add "EFS-SecGrp" to all AZ
  

- Show that you can only add one mount point for each AZ though it has multiple subnets(for example custom VPC) 
```
Click next 

```text
File system policy - optional------> keep it as is
```
Click next. Then review and Create 

Show that it is created. 

## Part 3 - Attach the EFS to the multiple EC2 Linux 2 instances

### STEP-1: Configure the EC2-1 instance


- open EC2 console

-  Connect to EC2-1 with SSH.
```text
ssh -i .....pem ec2-user@..................
```
- Update the installed packages and package cache on your instance.

```text
sudo yum update -y
```

- Install the "Amazon-efs-utils Package" on Amazon Linux

```text
sudo yum install -y amazon-efs-utils
```

- Create Mounting point 

```text
sudo mkdir efs
```

- Go to the EFS console and click  on "myEFS" . Then click "Attach" button seen top of the "EFS" page.

- On the pop up window, copy the script seen under "Using the EFS mount helper" option: "sudo mount -t efs -o tls fs-60d485e2:/ efs"

- Turn back to the terminal and mount EFS using the "EFS mount helper" to the "efs" mounting point

```text
sudo mount -t efs -o tls fs-xxxxxx:/ efs
```
- Check the "efs" folder
```text
ls
```
- Go the "efs" folder and create a new file with Nano editor.

```text
cd efs
sudo nano hello.txt
```
- Write something, save and exit;
```text
"hello from  EC2-1"
```

- check the hello.txt

```text
cat hello.txt
```
### STEP-2: Configure the EC2-2 instance


-  Connect to EC2-2 with SSH.
```text
ssh -i .....pem ec2-user@..................
```
- Update the installed packages and package cache on your instance.

```text
sudo yum update -y
```

- Install the "Amazon-efs-utils Package" on Amazon Linux

```text
sudo yum install -y amazon-efs-utils
```

- Create Mounting point 

```text
sudo mkdir efs
```

- Go to the EFS console and click  on "myEFS" . Then click "Attach" button seen top of the "EFS" page.

- On the pop up window, copy the script seen under "Using the EFS mount helper" option: "sudo mount -t efs -o tls fs-60d485e2:/ efs"

- Turn back to the terminal and mount EFS using the "EFS mount helper" to the "efs" mounting point

```text
sudo mount -t efs -o tls fs-xxxxxxx:/ efs
```
- Check the "efs" folder
```text
ls
```
- Check the hello.txt. Show that you can also reach the same file.

```text
cat hello.txt
```

- Add something hello.txt

```text
sudo nano hello.txt
"hello from  EC2-2"
```
- Check the hello.txt

```text
cat hello.txt

"hello from first EC2-1"
"hello from first EC2-2"
```
- Connect from EC2-1 to the "efs" and show the hello.txt:


```text
cd efs
cat hello.txt

"hello from first EC2-1"
"hello from first EC2-2"
```
### STEP-3: Configure the EC2-3 instance with EFS while Launching

- go to the EC2 console and click "Launch Instance"

- Configure third Instance in N.Virginia

```text
AMI             : Amazon Linux 2
Instance Type   : t2.micro
Network         : default
**File systems  :Add file system-------> myEFS (Note down the mnt point "/mnt/efs/fs1")
Subnet          : default
Security Group  : InstancesSecGrp
    Sec.Group Name :  SecGrp for EC2
Tag             :
    Key         : Name
    Value       : EC2-3
```
- Connect to EC2-3 with SSH

```text
ssh -i .....pem ec2-user@..................
```
- Go to the directory of mount target 
```text
cd /mnt/efs/fs1/
```
- Show the hello.txt:

```text
cat hello.txt

"hello from  EC2-1"
"hello from  EC2-2"
```
 - Add something hello.txt

```text
sudo nano hello.txt
"hello from  EC2-3"
```
- Check the hello.txt

```text
cat hello.txt

"hello from first EC2-1"
"hello from first EC2-2"
"hello from first EC2-3"
```

- Terminate instances and delete file system from console.