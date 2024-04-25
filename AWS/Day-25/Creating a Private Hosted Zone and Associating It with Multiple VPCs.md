
Creating a Private Hosted Zone and Associating It with Multiple VPCs
====================================================================

# Overview
------------
DNS names only need to be resolved internally, a Route 53 private hosted zone is created. In this hands-on lab, we will create a private hosted zone. To get started, we will create a peer relationship between the VPCs. We will then use Route 53 to create a private hosted zone and connectivity between the VPC peers by pinging the host by the fully qualified hostname we create in Route 53.

![AWS Architecture diagram showing the components of the serverless  architecture that have/will be deployed](./VPCDiagram.png)


## Task 1: Create an EC2 Instance and a Private Hosted Zone on Route 53

### Create an EC2 Instance

1.  Navigate to **EC2** --> **Instances** and click **Launch Instance**.

2.  On the AMI page, select the **Amazon Linux 2 AMI**.

3.  For instance type, choose **t2.micro**.

4.  Click **Next: Configure Instance Details**. 

5.  On the *Configure Instance Details* page:

    -   *Network*: **VPC-A**
    -   *Subnet*: **PublicSubnet1**
    -   *Auto-assign Public IP*: **Enable**

6.  Click **Next: Add Storage**, and then click **Next: Add Tags**. 

7.  On the *Add Tags* page, add the following tag:

    -   *Key*: **Name**
    -   *Value*: **Client**

8.  Click **Next: Configure Security Group**. 

9.  Click **Select an create s security group** and add inbound rules **All ICMP - IPv4** and **SSH** --> **Anywhere, 0.0.0.0/0**

10. Name the security group with  **EC2SecurityGroup**.

11. Click **Review and Launch** --> **Launch**.


12. In the key pair dialog, select **Create a new key pair**.

13. Give it a *Key pair name* of "PrivateKeyPair".

14. Click **Download Key Pair**, and then **Launch Instances**.

15. Click **View Instances**.

### Create a Private Hosted Zone on Route 53

1.  In a new browser tab, navigate to **Route 53** --> **Hosted zones**.

2.  Click **Create Hosted Zone**.

3.  In the *Create Hosted Zone* pane, set the following values:

    -   *Domain Name*: **privatezone.com**
    -   *Type*: **Private Hosted Zone for Amazon VPC**
    -   *VPC ID*: **VPC-A** in *US East (N. Virginia)*

4.  Click **Create**.

5.  Click **Back to Hosted Zones**.

6.  Select **privatezone.com**.

7.  In the *VPC ID* dropdown, select **VPC-B** in *US East (N.Virginia)*.

8.  Click **Associate New VPC**.

9.  In the *VPC ID* dropdown, select **VPC-C** in *US East (N. Virginia)*.

10. Click **Associate New VPC**.

## Task 2: Check VPC Configuration

In a new browser tab, navigate to **VPC** --> **Your VPCs**.

- **VPC-A**

1.  Select **VPC-A**.

2.  Click **Actions** --> **Edit DNS resolution**.

3.  Ensure *DNS resolution* is set to **enable**.

4.  Click **Cancel**.

5.  Click **Actions** --> **Edit DNS hostnames**.

6.  Ensure *DNS hostnames* is set to **enable**.

7.  Click **Cancel**.

- **VPC-B**

1.  Select **VPC-B**.

2.  Click **Actions** --> **Edit DNS resolution**.

3.  Ensure *DNS resolution* is set to **enable**.

4.  Click **Cancel**.

5.  Click **Actions** --> **Edit DNS hostnames**.

6.  Ensure *DNS hostnames* is set to **enable**.

7.  Click **Cancel**.

- **VPC-C**

1.  Select **VPC-C**.

2.  Click **Actions** --> **Edit DNS resolution**.

3.  Ensure *DNS resolution* is set to **enable**.

4.  Click **Cancel**.

5.  Click **Actions** --> **Edit DNS hostnames**.

6.  Ensure *DNS hostnames* is set to **enable**.

7.  Click **Cancel**.

## Task 3: Create a Route 53 A Record

1.  In the Route 53 console browser tab, click **Go to Record Sets**.
2.  Click **Create Record Set**.
3.  Set the following values:
    -   *Name*: **host**
    -   *Type*: **A — IPv4 address**
    -   *Alias*: **no**
    -   *Value*: In the **EC2 Instances** browser tab, select **Client**, copy its private IP, and paste it here.

4.  Click **Create**.

## Task 4: Create a VPC Peer Relationship and Configure Routing

### Create a VPC Peering Connection

1.  In the VPC console browser tab, click **Peering Connections** in the left-hand menu.

2.  Click **Create Peering Connection**.

3.  Set the following values:
    -   *Peering connection name tag*: **a2bpeering**
    -   *VPC (Requester)*: **VPC-A**
    -   *Account*: **My account**
    -   *Region*: **This region (us-east-1)**
    -   *VPC (Accepter)*: **VPC-B**

4.  Click **Create Peering Connection** and then **OK**.

5.  With *a2bpeering* accepted, click **Actions** --> **Accept Request**.

6.  In the dialog, click **Yes, Accept**.

### Configure Routing

1.  Click **Route Tables** in the left-hand menu.

2.  In the EC2 instances console browser tab, make note of the subnet the *Client* instance is in.

3.  In the VPC route tables browser tab, select the route table  associated with the subnet you just noted.

4.  Click the **Routes** tab.

5.  Click **Edit routes**.

6.  Click **Add route**:
    -   *Destination*: **10.2.0.0/16**
    -   *Target*: **Peering Connection**, **a2bpeering**

7.  Click **Save routes**.

8.  In the EC2 instances console browser tab, make note of the subnet the *Instance2* instance is in.

9.  In the VPC route tables browser tab, select the route table  associated with the subnet you just noted.

10. Click the **Routes** tab.

11. Click **Edit routes**.

12. Click **Add route**:

    -   *Destination*: **10.1.0.0/16**
    -   *Target*: **Peering Connection**, **a2bpeering**

13. Click **Save routes**.

14. In the EC2 console browser tab, click **Security Groups** in the left-hand menu.

15. Copy the *Group ID* of `SG-Public2`.
16. Select **SG-Public1**.
17. Click the **Inbound** tab.
18. Click **Edit**.
19. Click **Add Rule**:
    -   *Type*: **Custom TCP**
    -   *Source*: **Custom**, the `SG-Public2` ID

20. Click **Save**.
21. Copy the *Group ID* of *SG-Public1*.
22. Select **SG-Public2**.
23. Click the **Inbound** tab.
24. Click **Edit**.
25. Click **Add Rule**:
    -   *Type*: **Custom TCP**
    -   *Source*: **Custom**, the `SG-Public1` ID

26. Click **Save**.

## Task 5: Verify Connectivity

1.  Click **Instances** in the left-hand menu.

2.  Select **Instance2**.

3.  Copy its public IP address.

4.  Connect to the instance via SSH using the provided keyname.

```bash
ssh -i keyname.pem ec2-user<INSTANCE2_PUBLIC_IP>
```

5.  Enter the following:

```bash
ping privatezone.com
```

- We should be successful.

6.  Exit the ping by pressing **Ctrl**+**C**.

7.  Note the IP returned in the ping.

8.  In the AWS console, check the private IP listed for the *Client*  instance. It should match the one returned in the ping, meaning we  were successful.

Conclusion
----------

Congratulations on successfully completing this hands-on lab!

