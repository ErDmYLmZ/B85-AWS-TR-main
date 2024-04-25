Introduction to Amazon EC2 - Lab
==========================

Overview
--------

This lab provides you with a basic overview of launching, resizing, managing, and monitoring an Amazon EC2 instance.

**Amazon Elastic Compute Cloud (Amazon EC2)** is a web service that provides resizable compute capacity in the cloud. It is designed to make web-scale cloud computing easier for developers.  
Amazon EC2's simple web service interface allows you to obtain and configure capacity with minimal friction. It provides you with complete control of your computing resources and lets you run on Amazon's proven computing environment. Amazon EC2 reduces the time required to obtain and boot new server instances to minutes, allowing you to quickly scale capacity, both up and down, as your computing requirements change.

Amazon EC2 changes the economics of computing by allowing you to pay only for capacity that you actually use. Amazon EC2 provides developers the tools to build failure resilient applications and isolate themselves from common failure scenarios.

### Topics covered

By the end of this lab, you will be able to:

*   Launch a web server with termination protection enabled
*   Monitor Your EC2 instance
*   Modify the security group that your web server is using to allow HTTP access
*   Resize your Amazon EC2 instance to scale
*   Explore EC2 limits
*   Test termination protection
*   Terminate your EC2 instance


### Task 1: Launch Your Amazon EC2 Instance
---------------------------------------

In this task, you will launch an Amazon EC2 instance with _termination protection_. Termination protection prevents you from accidentally terminating an EC2 instance. You will deploy your instance with a User Data script that will allow you to deploy a simple web server.

3.  In the **AWS Management Console** on the Services menu, click **EC2**.
    
4.  At the top right of the screen, if you see **New EC2 Experience** toggle to use the new UI, if it is not enabled by default.
    
5.  Click Launch instance > **Launch instance**.
    

### Step 1: Choose an Amazon Machine Image (AMI)

An **Amazon Machine Image (AMI)** provides the information required to launch an instance, which is a virtual server in the cloud. An AMI includes:

*   A template for the root volume for the instance (for example, an operating system or an application server with applications)
*   Launch permissions that control which AWS accounts can use the AMI to launch instances
*   A block device mapping that specifies the volumes to attach to the instance when it is launched

The **Quick Start** list contains the most commonly-used AMIs. You can also create your own AMI or select an AMI from the AWS Marketplace, an online store where you can sell or buy software that runs on AWS.

6.  Click Select next to **Amazon Linux 2 AMI** (at the top of the list).

### Step 2: Choose an Instance Type

Amazon EC2 provides a wide selection of _instance types_ optimized to fit different use cases. Instance types comprise varying combinations of CPU, memory, storage, and networking capacity and give you the flexibility to choose the appropriate mix of resources for your applications. Each instance type includes one or more _instance sizes_, allowing you to scale your resources to the requirements of your target workload.

7.  Scroll down and select **t2.micro**.

A **t2.micro** instance type has 1 virtual CPUs and 1 GiB of memory.

8.  Click Next: Configure Instance Details

### Step 3: Configure Instance Details

This page is used to configure the instance to suit your requirements. This includes networking and monitoring settings.

The **Network** indicates which Virtual Private Cloud (VPC) you wish to launch the instance into. You can have multiple networks, such as different ones for development, testing and production.

9.  For **Network**, select **default VPC**.


10.  For **Enable termination protection**, select **Protect against accidental termination**.

When an Amazon EC2 instance is no longer required, it can be _terminated_, which means that the instance is stopped and its resources are released. A terminated instance cannot be started again. If you want to prevent the instance from being accidentally terminated, you can enable _termination protection_ for the instance, which prevents it from being terminated.

11.  Scroll down, then expand **Advanced Details**.

A field for **User data** will appear.

When you launch an instance, you can pass _user data_ to the instance that can be used to perform common automated configuration tasks and even run scripts after the instance starts.

Your instance is running Amazon Linux, so you will provide a _shell script_ that will run when the instance starts.

* *Asagida aslinda hani demistik ya(notlarda) bi HTML sayfamiz olacak EC2 makinemizde diye, iste o HTML sayfasinin kodu var.*

12.  Copy the following commands and paste them into the **User data** field:

    #!/bin/bash
    yum -y install httpd
    systemctl enable httpd
    systemctl start httpd
    

The script will:

*   Install an Apache web server (httpd)
*   Configure the web server to automatically start on boot
*   Activate the Web server
*   Create a simple web page

13.  Click Next: Add Storage

### Step 4: Add Storage

Amazon EC2 stores data on a network-attached virtual disk called _Elastic Block Store_.

You will launch the Amazon EC2 instance using a default 8 GiB disk volume. This will be your root volume (also known as a 'boot' volume).

14.  Click Next: Add Tags

### Step 5: Add Tags

Tags enable you to categorize your AWS resources in different ways, for example, by purpose, owner, or environment. This is useful when you have many resources of the same type — you can quickly identify a specific resource based on the tags you have assigned to it. Each tag consists of a Key and a Value, both of which you define.

15.  Click Add Tag then configure:

*   **Key:** 
*   **Value:** 

16.  Click Next: Configure Security Group

### Step 6: Configure Security Group

A _security group_ acts as a virtual firewall that controls the traffic for one or more instances. When you launch an instance, you associate one or more security groups with the instance. You add _rules_ to each security group that allow traffic to or from its associated instances. You can modify the rules for a security group at any time; the new rules are automatically applied to all instances that are associated with the security group.

* *Instance bazinda guvenlik security group'larla saglanir.*

17.  On **Step 6: Configure Security Group**, configure:

Keep the default selection, Create a **new** security group.

*   **Security group name:** 
*   **Description:** 

In this lab, you will not log into your instance using SSH. Removing SSH access will improve the security of the instance.

18.  Delete the existing SSH rule.
    
19.  Click Review and Launch
    

### Step 7: Review Instance Launch

The Review page displays the configuration for the instance you are about to launch.

20.  Click Launch

A **Select an existing key pair or create a new key pair** window will appear.

Amazon EC2 uses public–key cryptography to encrypt and decrypt login information. To log in to your instance, you must create a key pair, specify the name of the key pair when you launch the instance, and provide the private key when you connect to the instance.

In this lab you will not log into your instance, so you do not require a key pair.

YOU MUST select **Proceed without a key pair** below. If you do not select this, your instance will fail to launch.

21.  Click the **Choose an existing key pair** drop-down and select **Proceed without a key pair**
    
22.  Select **I acknowledge that ...**.
    
23.  Click Launch Instances
    

Your instance will now be launched.

24.  Click View Instances

The instance will appear in a _pending_ state, which means it is being launched. It will then change to _running_, which indicates that the instance has started booting. There will be a short time before you can access the instance.

The instance receives a _public DNS name_ that you can use to contact the instance from the Internet.

Select Your **Web Server** and the **Details** tab displays detailed information about your instance.

To view more information in the Details tab, drag the window divider upwards.

Review the information displayed in the **Details** tab. It includes information about the instance type, security settings and network settings.

25.  Wait for your instance to display the following:

*   **Instance State:** running
*   **Status Checks:** 2/2 checks passed

**Congratulations!** You have successfully launched your first Amazon EC2 instance.

### Task 2: Monitor Your Instance
-----------------------------

Monitoring is an important part of maintaining the reliability, availability, and performance of your Amazon Elastic Compute Cloud (Amazon EC2) instances and your AWS solutions.

26.  Click the **Status Checks** tab.

With instance status monitoring, you can quickly determine whether Amazon EC2 has detected any problems that might prevent your instances from running applications. Amazon EC2 performs automated checks on every running EC2 instance to identify hardware and software issues.

Notice that both the **System reachability** and **Instance reachability** checks have passed.

27.  Click the **Monitoring** tab.

This tab displays CloudWatch metrics for your instance. Currently, there are not many metrics to display because the instance was recently launched.

You can click on a graph to see an expanded view.

Amazon EC2 sends metrics to Amazon CloudWatch for your EC2 instances. Basic (five-minute) monitoring is enabled by default. You can enable detailed (one-minute) monitoring.

28.  In the Actions menu, select **Monitor and troubleshooting** **Get system log**.

The System Log displays the console output of the instance, which is a valuable tool for problem diagnosis. It is especially useful for troubleshooting kernel problems and service configuration issues that could cause an instance to terminate or become unreachable before its SSH daemon can be started. _If you do not see a system log, wait several minutes and then try again._

29.  Scroll through the output and note that the HTTP package was installed from the **user data** that you added when you created the instance.


30.  Click **Cancel**
    
31.  In the Actions menu, select **Monitor and troubleshoot** **Get instance screenshot**.
    

This shows you what your Amazon EC2 instance console would look like if a screen were attached to it.


If you are unable to reach your instance via SSH or RDP, you can capture a screenshot of your instance and view it as an image. This provides visibility as to the status of the instance, and allows for quicker troubleshooting.

32.  Click **Cancel**

**Congratulations!** You have explored several ways to monitor your instance.

### Task 3: Update Your Security Group and Access the Web Server
------------------------------------------------------------

When you launched the EC2 instance, you provided a script that installed a web server and created a simple web page. In this task, you will access content from the web server.

33.  Click the **Details** tab.
    
34.  Copy the **Public IPv4 address** of your instance to your clipboard.
    
35.  Open a new tab in your web browser, paste the IP address you just copied, then press **Enter**.
    

**Question:** Are you able to access your web server? Why not?

You are **not** currently able to access your web server because the _security group_ is not permitting inbound traffic on port 80, which is used for HTTP web requests. This is a demonstration of using a security group as a firewall to restrict the network traffic that is allowed in and out of an instance.

To correct this, you will now update the security group to permit web traffic on port 80.

36.  Keep the browser tab open, but return to the **EC2 Management Console** tab.
    
37.  In the left navigation pane, click **Security Groups**.
    
38.  Click **Security group ID** with the Security group name **Web Server security group**.
    

The security group currently has no rules.

39.  Click Edit inbound rules.
    
40.  Click Add rule then configure:
    

*   **Type:** _HTTP_
*   **Source:** _Anywhere_
*   Click Save rules

The new Inbound HTTP rule will create an entry for both IPV4 IP address (0.0.0.0/0) as well as IPV6 IP address (::/0).

**Note:** using "Anywhere", or more specifically, using 0.0.0.0/0 or ::/0 is not a recommended best practice for production workloads.

41.  Return to the web server tab that you previously opened and refresh the page.


**Congratulations!** You have successfully modified your security group to permit HTTP traffic into your Amazon EC2 Instance.

### Task 4: Resize Your Instance: Instance Type and EBS Volume
----------------------------------------------------------

As your needs change, you might find that your instance is over-utilized (too small) or under-utilized (too large). If so, you can change the _instance type_. For example, if a _t2.micro_ instance is too small for its workload, you can change it to an _t3.small_ instance. Similarly, you can change the size of a disk.

### Stop Your Instance

Before you can resize an instance, you must _stop_ it.

When you stop an instance, it is shut down. There is no charge for a stopped EC2 instance, but the storage charge for attached Amazon EBS volumes remains.

42.  On the **EC2 Management Console**, in the left navigation pane, click **Instances**.

**Web Server** should already be selected.

43.  Select **Instance state** **Stop instance**.
    
44.  Click Stop
    

Your instance will perform a normal shutdown and then will stop running.

45.  Wait for the **Instance State** to display: stopped

### Change The Instance Type

46.  Select your **Web Server**
    
47.  In the Actions menu, select **Instance settings** **Change instance type**, then configure:
    

*   **Instance type:** _t3.small_
*   Click Apply

When the instance is started again it will be a _t3.small_, which has twice as much memory as a _t3.micro_ instance.

### Resize the EBS Volume

48.  In the left navigation menu, click **Volumes**.
    
49.  In the Actions menu, select **Modify Volume**.
    

The disk volume currently has a size of 8 GiB. You will now increase the size of this disk.

50.  Change the size to: 
    
51.  Click Modify
    
52.  Click Yes to confirm and increase the size of the volume.
    
53.  Click Close
    

### Start the Resized Instance

You will now start the instance again, which will now have more memory and more disk space.

54.  In left navigation pane, click **Instances**.
    
55.  Select **Instance state** **Start instance**.
    

**Note:** An EBS volume being modified goes through a sequence of states: Modifying, Optimizing, and finally Complete.

**Congratulations!** You have successfully resized your Amazon EC2 Instance. In this task you changed your instance type from _t2.micro_ to a _t3.small_. You also modified your root disk volume from 8 GiB to 10 GiB.

### Task 5: Explore EC2 Limits
--------------------------

Amazon EC2 provides different resources that you can use. These resources include images, instances, volumes, and snapshots. When you create an AWS account, there are default limits on these resources on a per-region basis.

56.  In the left navigation pane, click **Limits**.
    
57.  Click the **All limits** and select **Running instances**.
    

Notice that there is a limit for the instance type based on the number of vCPUs required. For example, **For running On-Demand All Standard**, you have a limit of 32 vCPUs. A t2.micro instance requires 1 vCPUs. Therefore, in this region, you could launch 32 t2.micro instances in this region.

You can request an increase for many of these limits.

### Task 6: Test Termination Protection
-----------------------------------

You can delete your instance when you no longer need it. This is referred to as _terminating_ your instance. You cannot connect to or restart an instance after it has been terminated.

In this task, you will learn how to use _termination protection_.

58.  In left navigation pane, click **Instances**.
    
59.  In the Instance state menu, select **Terminate instance**.
    
60.  In the **Terminate instance** dialogue box, click Terminate
    

Note that there is a message that says: _Failed to terminate instances i-0aws5436tfr32._

This is a safeguard to prevent the accidental termination of an instance. If you really want to terminate the instance, you will need to disable the termination protection.

61.  Close the displayed error message.
    
62.  In the Actions menu, select **Instance settings** **Change termination protection**.
    
63.  Deselect **Enable**
    
64.  Click Save
    

You can now terminate the instance.

65.  In the Instance state menu, select **Terminate instance**.
    
66.  In the **Terminate instance** dialogue box, click Terminate
    

**Congratulations!** You have successfully tested termination protection and terminated your instance.

End Lab
-------

Follow these steps to close the console, end your lab!


Additional Resources
--------------------

*   [Launch Your Instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/LaunchingAndUsingInstances.html)
*   [Amazon EC2 Instance Types](https://aws.amazon.com/ec2/instance-types)
*   [Amazon Machine Images (AMI)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html)
*   [Amazon EC2 - User Data and Shell Scripts](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html)
*   [Amazon EC2 Root Device Volume](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/RootDeviceStorage.html)
*   [Tagging Your Amazon EC2 Resources](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html)
*   [Security Groups](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-network-security.html)
*   [Amazon EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)
*   [Status Checks for Your Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-system-instance-status-check.html?icmpid=docs_ec2_console)
*   [Getting Console Output and Rebooting Instances](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-console.html)
*   [Amazon EC2 Metrics and Dimensions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/ec2-metricscollected.html)
*   [Resizing Your Instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-resize.html)
*   [Stop and Start Your Instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Stop_Start.html)
*   [Amazon EC2 Service Limits](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html)
*   [Terminate Your Instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html)
*   [Termination Protection for an Instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html)



This lab provides you with a basic overview of launching, resizing, managing, and monitoring an Amazon EC2 instance.