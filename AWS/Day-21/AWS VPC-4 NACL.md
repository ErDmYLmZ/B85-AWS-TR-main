
# Hands-On AWS VPC NACL:
-----------------------------


Architecture Diagram
====================

![Architecture Diagram](./task_id_aws_vpc_nacl.png)

Task Details 
============

1.  Creating a New VPC

2.  Create Subnets

3.  Create and attach an Internet Gateway

4.  Create Route Tables and Associate them it with Subnets

5.  Update Route Table and Configure the Internet Gateway

6.  Enabling Auto-Assign Public IP for Public Subnets

7.  Launching an EC2 Instance in the Public Subnet

8.  Launching an EC2 Instance in the Private Subnet

9.  Testing Both EC2 instances.

10. Creating Custom NACL and Associate it to the Subnet

11. Testing the Public and Private Server 

12. Adding Rules to Custom NACL (MyPublicNACL)

13. Testing Both EC2 instances

14. Validation of the lab

Lab Steps
=========

Task 1: Creating a New VPC
--------------------------

1.  Navigate to VPC by clicking on the **Services** button on the top of the AWS Console.

2.  Click on **VPC** (under **Networking & Content Delivery** section) or you can also search for VPC.

3.  Click on **Your VPCs**from the left menu.

4.  Here you can see the list of all VPC. No need to do anything yet. We  will create a new VPC for this lab.

5.  Click on ```Create VPC```

    -   **Name tag:** Enter **MyVPC**

    -   **IPv4 CIDR block:** Enter **10.0.0.0/16**

    -   **IPv6 CIDR block:** No need to change this, make sure **No IPv6 CIDR Block** is checked.

    -   **Tenancy:** No need to change this, just be sure **Default**is selected.

    -   Click on ```CreateVPC``` 


Task 2: Creating Subnets
------------------------

**Note:** In this lab, we will create one public subnet and a private subnet in us-east-1a and us-east-1b Availability Zones.

1.  For the Public Subnet click on **Subnets** from the left menu and click on **Create subnet.**

    -   **VPC ID           :** Select **MyVPC** from the list.

    -   **Subnet Name      :** Enter ***MyPublicSubnet***

    -   **Availability Zone    :** Select **us-east-1a**

    -   **IPv4 CIDR block    :** Enter the range ***10.0.1.0/24***

    -   Click on **Create Subnet**

2.  For Private Subnet click on **Create Subnet**again. 

    -   **VPC ID            :** Select **MyVPC** from the list.

    -   **Subnet Name        :** Enter ***MyPrivateSubnet***

    -   **Availability Zone    :** Select **us-east-1b**

    -   **IPv4 CIDR block    :** Enter the range ***10.0.2.0/24***

    -   Click on **Create subnet.**


Task 3: Create and attach an Internet Gateway
---------------------------------------------

**Note:** By default, instances that are launched in a VPC cannot communicate with the Internet.

To enable Internet access, an Internet gateway needed to be attached to the VPC

1.  Click on **Internet Gateways**from the left menu and click ***Create internet  gateway***

    -   **Name Tag :** Enter ***MyInternetGateway***

    -   Click on ***Create internet  gateway***

2.  Select the Internet gateway you created from the list.

    -   Click on **Actions**.

    -   Click on **Attach to VPC**.

    -   Select MyVPC and click on **Attach to VPC.**

Task 4: Create Route Tables and Associate them it with Subnets.
--------------------------------------------------------------

1.  Go to **Route Tables** from the left menu and click on **Create route table.**

    -   **Name Tag: **Enter** ***PublicRouteTable***

    -   **VPC:** Select **MyVPC** from the list.

    -   Click on **Create route table.**

2.  We will be using the **default (main) Route Table** created by VPC.


-   You will be able to see the Route table with **VPC ID MyVPC** and  **Main** as **Yes**

-   Select the Route Table and rename it.??????????????????

-   **Name Tag:** Enter ***PrivateRouteTable***

3.  Now **associate the subnets** to the route tables.

4.  Click on **PublicRouteTable** and go to the **Action** and in that  go to **Edit Subnet Associations tab.**

    -   Click on  **Edit Subnet Associations**.

    -   Select **MyPublicSubnet** from the list.

    -   Click on **Save Associations**

5.  Click on **PrivateRouteTable** and go to the **Action** and in that go to **Edit Subnet Associations tab.**

    -   Click on  **Edit Subnet Associations**.

    -   Select **MyPrivateSubnet** from the list.

    -   Click on **Save Associations**

Task 5: Update Route Table and Configure the Internet Gateway
-------------------------------------------------------------

1.  **PublicRouteTable** : Add a route to allow Internet traffic to the VPC.

-   Select **PublicRouteTable.**

-   Go to the **Routes** tab click on **Edit routes**. On the next page, click on **Add route.**

-   Specify the following values: 

    -   **Destination:** Enter ***0.0.0.0/0***

    -   **Target:** Select **Internet Gateway** from the dropdown menu to select **MyInternetGateway**.

    -   Click on **Save changes.**

Task 6: Enabling Auto-Assign Public IP for Public Subnets.
---------------------------------------------------------

**Note**: This setting will allow you to automatically assign public IP for all the EC2 instances launched in the public subnet

 Click on **Subnets** from the left menu on VPC.

-   Select  **MyPublicSubnet** from the Subnet list

-   Click on **Actions** and then select **Edit subnet settings**

-   Check the **Enable** and **Auto-assign IPv4 address** check box

-   Now click on **Save**

Task 7: Launching an EC2 Instance in the Public Subnet
------------------------------------------------------

1.  Navigate to **EC2** by clicking on the **Services** menu in the top, then click on **ÈC2** in the **Compute**  section.

2.  Navigate to **Instances**from the left side menu and click on **Launch Instances**button.

3.  **Choose an Amazon Machine Image (AMI):** Search for **Amazon Linux 2 AMI** in the search box and click on the **select** button.

4.  Choose an Instance Type: Select **t2.micro** and click on   **Next: Configure Instance Details**

5.  Configure Instance Details:

    -   **Network        :** Choose **MyVPC**

    -   **Subnet            :** Choose **MyPublicSubnet**

    -   **Auto-assign Public IP    :**  **Enable**

    -   Under the **User data:** section, enter the following script to create an HTML page served by Apache:


```bash
#!/bin/bash                                                       

sudo su                                                              
yum update -y                                                       
yum install httpd -y                                                
echo "<html><h1>Welcome to my Website</h1\><html>" >> /var/www/html/index.html                                              
systemctl start httpd                                               
systemctl enable httpd                                             
```
   
   -   Leave all other settings as default. Click on  **Next: Add Storage**

6.  Add Storage: No need to change anything in this step, click on **Add Tag**

7.  **Add Tags:** Click on **Add Tag**

    -   Key    : Enter ***Name***

    -   Value    : Enter ***MyPublicEC2Server***

    -   Click on **Next: Configure Security Group**

8.  Configure Security Group:

    -   Security group name: Enter** ***MyWebserverSG***

    -   Description : Enter ***My EC2 Security Group***

    -   SSH is already available,

        -   **Choose Type:** ***SSH***

        -   **Source :** Select ***Anywhere*** 

    -   For **HTTP**, click on ***Add Rule***,

    -   **ChooseType:** ***HTTP***

    -   **Source :** Enter ***Anywhere*** (From ALL IP addresses accessible).

    -   Click on **Review and Launch**.

        1.  **Review and Launch:** Review all settings and click on **Launch.**

        2.  **Key Pair :** Create a new key Pair, Key pair name : ***Mykey*** and click on****Download Key Pair**after that click on **Launch Instances**.

        3.  **Launch Status:** Your instance is now launching. Select the instance and wait for the instance to change status to **Running**.

        4.  Note the Public IP address of **MyPublicEC2Server** 

Task 8: Launching an EC2 Instance in the Private Subnet
-------------------------------------------------------

1.  Click on **Launch Instances**

2.  ***Search and Choose Amazon Linux 2 AMI:***

3.  Choose an Instance Type: Select **t2.micro**  and click on the **Next: Configure Instance Details**

4.  Configure Instance Details: 

    -   **Network**        : Choose **MyVPC**

    -   **Subnet**           : Choose **MyPrivateSubnet**

    -   **Auto-assign Public IP**    : Use Subnet Setting(Disable) - default

    -   Leave all other settings as default.

    -   Click on **Next: Add Storage**

5.  Add Storage: No need to change anything in this step, click on  **Next: Add Tags**

6.  **Add Tags:** Click on **Add Tag**

    -   Key    : Enter ***Name***

    -   Value    : Enter ***MyPrivateEC2Server***

    -   Click on **Next: Configure Security Group**

7.  Configure Security Group:

    -   Security group name: Enter ***MyServerSG***

    -   Description : Enter ***My EC2 Security Group***

    -   SSH is already available,

        -   **Choose Type:** ***SSH***

        -   **Source**: ***custom : 0.0.0.0/0***

    -   For **ALL ICMP IPv4** , Click on ***All ICMP -IPv4***

        -   **Choose Type:** ***All ICMP -IPv4***

        -   **Source:**   **Anywhere** (From ALL IP addresses accessible).

    -   Click on **Review and Launch**

8.  Review and Launch : Review all settings and click on **Launch**

9.  Key Pair : Select the existing key pair created earlier (**MyKey.pem**).

10. Click on **Launch Instances**.

11. Launch Status: Your instance is now launching, Select the instance and wait for the instance to change status to **Running**.

12. Note the Private IP Address of **MyPrivateEC2Server.**

13. Two servers are launched and ready.

Task 9: Testing Both EC2 instances
-----------------------------------

1.  **Public EC2 instances**: We have installed a web application on  this server.

    -   Select the **MyPublicEC2Server**EC2 instance from the instancelist.

    -   From the Description tab, copy the **IPv4 Public IP**.

    -   Now paste this IP in you Web Browser

    -   You will be able to see the following page:
  
2.  Next, we will try to ping the Private EC2 from the Public EC2instance.

    -   SSH into EC2 Instance

    -   Please follow the steps in SSH into EC2 Instance.

    -   Once connected to the server:

        -   Change to root user: **sudo su**

-   Copy the Private IP of **MyPrivateEC2Server** from the Description tab.

-   Ping the Private Instance using the Private IPv4
-   Example:

-   Press [Ctrl] + C to stop instead of pause.

-   **Note: You were able to do these tasks because the Default NACL that was created during VPC creation allows both INBOUND and  OUTBOUND by Default.**

Task 10: Creating Custom NACL and Associate it to the Subnet
------------------------------------------------------------

**Note:** By default, both subnets will be associated with the Default NACL of **MyVPC.** Once you create a custom NACL and attach it to the  public subnet and private Subnet.

1.  Navigate to **VPC** under the Services menu. Click on ***Network ACL***  under **Security**

2.  Click on **Create Network ACL**

3.  Create Network ACL:

    -   Name tag: Enter ***MyPublicNACL***

    -   VPC: Select **MyVPC****from the dropdown list.

    -   Click on **Create.**

4.  Associating **MyPublicNACL** to the Public Subnet

    -   Select the Action tab and click on **Edit subnet associations**

    -   Select both the **Public and Private** subnets from the table.

    -   Click on **Save changes**

5.  Renaming the Main NACL

    -   Select the **Default NACL** of the VPC MyVPC\

    -   Enter the name ***MyPrivateNACL*** and click on **Save**

Task 11: Testing the Public and Private Server 
-----------------------------------------------

1.  Public EC2 Instance:

    -   Navigate to the **EC2 Instance Dashboard.** Click on   **Instances** from the left side menu.

    -   Select the **MyPublicEC2Server**EC2 instance from the instance list.

    -   From the Description tab, copy the **IPv4 Public IP**.

    -   Now paste this IP into your web browser and click [Enter]

    -   You will see the following page:\

       **Note: This is because the Custom NACL which is attached to your Public subnet restricts both INBOUND and OUTBOUND traffic.**

2.  Private EC2 Instance:

    -   Since the Public NACL restricts all traffic, you won't be able to SSH into the public EC2 Instance to ping the Private Instance.

    -   Next, we are going to solve this.

Task 12: Adding Rules to Custom NACL (MyPublicNACL)
---------------------------------------------------

1.  Navigate to **VPC** under the **Services** menu. Click on **Network ACLs**    under **Security.**

2.  Select **MyPublicNACL** from the list.

3.  In the Inbound rules, click **Edit inbound rules**

4.  Add the following rules:

    -   **HTTP** click on **Add rules,**

        -   Rule# : Enter ***100***

        -   Type: Choose **HTTP (80)**

        -   Source: Enter ***0.0.0.0/0***

        -   Allow / Deny: Select Allow

    -   For **ALL ICMP- IPv4**, click on **Add rules**,

        -   **Rule#** : Enter ***150***

        -   Type: Choose**ALL ICMP - IPv4 **

        -   Source: Enter ***0.0.0.0/0***

        -   Allow / Deny: Select Allow

    -   For **SSH**, click on **Add rules**,

        -   **Rule# : Enter** ***200***

        -   Type: Choose **SSH (22) **

        -   Source: Enter ***0.0.0.0/0***

        -   Allow / Deny: Select Allow\

        -   Click on **Save changes**

5.  In the **Outbound rules** Tab, Click Edit outbound rules

6.  Add the following rules:

    -   **Custom Port** is already available,

        -   Rule# : Enter ***100***

        -   Type: Choose **Custom TCP Rule**

        -   Port Range: Enter ***1024 - 65535***

        -   Source: Enter ***0.0.0.0/0***

        -   Allow / Deny: Select *Allow*

    -   For **ALL ICMP- IPv4**, click on **Add rules**,

        -   Rule\# : Enter ***150***

        -   Type: Choose **ALL ICMP - IPv4 **

        -   Source: Enter ***0.0.0.0/0***

        -   Allow / Deny: Select Allow

    -   For **SSH**, click on **Add rules** ,

        -   Rule# : Enter ***200***

        -   Type: Choose **SSH (22) **

        -   Source: Enter******0.0.0.0/0**

        -   Allow / Deny: Select Allow
           
        -   Click on **Save**

Task 14: Testing Both EC2 instances
-----------------------------------

1.  We will try to ping the Private EC2 from the Public EC2 instance.

    -   SSH into EC2 Instance

        -   Please follow the steps in  Once connected to the server:

        -   Change to root user: **sudo su**

    -   Copy the Private IP of **MyPrivateEC2Server** from the Description tab.![]

    -   Ping to the Private Instance using the Private IPv4


-   Press [Ctrl] + C again to cancel the process instead of pausing it.

-   Note: You were able to do these tasks because we added NACL Rules.


End Lab 
