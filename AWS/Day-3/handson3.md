# Introduction to AWS Identity and Access Management (IAM)
========================================================

Lab Overview
------------

**AWS Identity and Access Management (IAM)** is a web service that enables Amazon Web Services (AWS) customers to manage users and user permissions in AWS. With IAM, you can centrally manage **users**, **security credentials** such as access keys, and **permissions** that control which AWS resources users can access.

Topics covered
--------------

This lab will demonstrate:

-   Exploring pre-created **IAM Users and Groups**
-   Inspecting **IAM policies** as applied to the pre-created groups
-   Following a **real-world scenario**, adding users to groups with specific capabilities enabled
-   Locating and using the **IAM sign-in URL**
-   **Experimenting** with the effects of policies on service access

**Other AWS Services**

During this lab, you may receive error messages when performing actions beyond the steps in this lab guide. These messages will not impact your
ability to complete the lab.

**AWS Identity and Access Management**

AWS Identity and Access Management (IAM) can be used to:

-   **Manage IAM Users and their access:** You can create Users and assign them individual security credentials (access keys, passwords, and multi-factor authentication devices). You can manage permissions to control which operations a User can perform.

-   **Manage IAM Roles and their permissions:** An IAM Role is similar to a User, in that it is an AWS identity with permission policies that determine what the identity can and cannot do in AWS. However, instead of being uniquely associated with one person, a Role is intended to be *assumable* by anyone who needs it.

# Start Lab
---------


# Task 1: Explore the Users and Groups
------------------------------------


In this task, you will explore the Users and Groups that have already
been created for you in IAM.

1.  In the **AWS Management Console**, on the **Services** menu, click **IAM**.

2.  In the navigation pane on the left, click **Users** and creat The following IAM Users :

-   user-1(EC2-Admin)
```bash
# Add User
User name: user-1
Select AWS Credential Type: Access key - Programmatic Access # ve
                            Password - AWS Management Console access > Custom Password > Techpro12345
Require password reset # tiki kaldir

# Permissions
Attach existing policies directly
    AdministratorAccess

# Add tags (optional)
Key: Jobtitle
Value(optional): Devops

# Review
Create user

# Success
Download .csv
```
-   user-2(EC2-Support) <AmazonEC2FullAccess>

```bash
# Add User
User name: user-2
Select AWS Credential Type: Access key - Programmatic Access # ve
                            Password - AWS Management Console access > Custom Password > Techpro12345
Require password reset # tiki kaldir

# Permissions
Attach existing policies directly
    AmazonEC2FullAccess

# Add tags (optional)
Key: Jobtitle
Value(optional): Devops

# Review
Create user

# Success
Download .csv
```
-   user-3(S3-Support) <AmazonS3FullAccess>

```bash
# Add User
User name: user-3
Select AWS Credential Type: Access key - Programmatic Access # ve
                            Password - AWS Management Console access > Custom Password > Techpro12345
Require password reset # tiki kaldir

# Permissions
Attach existing policies directly
    AmazonS3FullAccess

# Add tags (optional)
Key: Jobtitle
Value(optional): Devops

# Review
Create user

# Success
Download .csv
```


7.  In the navigation pane on the left, click **User Groups**. Lets create The following groups.

```bash
EC2-Admin
    Attach permission policies - Optional
        AdministratorAccess
EC2-Support
    Attach permission policies - Optional
        AmazonEC2FullAccess
S3-Support
    Attach permission policies - Optional
        AmazonS3FullAccess
```
- Sonrasinda 

# Business Scenario
-----------------
# Task 1 - Creating Users
For the remainder of this lab, you will work with these Users and Groups to enable permissions supporting the following business scenario:
Your company is growing its use of Amazon Web Services, and is using many Amazon EC2 instances and a great deal of Amazon S3 storage. You wish to give access to new staff depending upon their job function:

```txt
User -  In Group -  Permissions

Abuzer - S3-Support - Read-Only access to Amazon S3

Muhittin - EC2 Support - Read-Only access to Amazon EC2

Ali - EC2-Admin - View, Start and Stop Amazon EC2 instances
```

# Task 2: Add Users to Groups
---------------------------

You have recently hired **user-1** into a role where they will provide support for Amazon S3. You will add them to the **S3-Support** group so that they inherit the necessary permissions via the attached *AmazonS3ReadOnlyAccess* policy.

## Add Abuzer to the S3-Support Group

8. In the left navigation pane, click **User Groups**.

9. Click the **S3-Support** group.

10. Click the **Users** tab.

11. In the **Users** tab, click **Add Users to Group**.

12. In the **Add Users to Group** window, configure the following:

-   Select **Abuzer**.
-   At the bottom of the screen, click **Add Users**.

* In the **Users** tab you will see that **Abuzer** has been added to the group.

## Add Muhittin to the EC2-Support Group

You have recently hired **Muhittin** into a role where they will provide support for Amazon EC2. You will add them to the **EC2 Support** group so that they inherit the necessary permissions via the attached *AmazonEC2ReadOnlyAccess* policy.


13. Using similar steps to the ones above, add **Muhittin** to the  **EC2-Support** group.

* **Muhittin** should now be part of the **EC2-Support** group.

## Add Ali to the EC2-Admin Group

You have recently hired **Ali** into a role where they will provide support for Amazon EC2. You will add them to the **EC2 Admin** group so that they inherit the necessary permissions via the attached *AmazonEC2FullAccess* policy.

14. Using similar steps to the ones above, add **Ali** to the **EC2-Admin** group.

* **Ali** should now be part of the **EC2-Admin** group.

15. In the navigation pane on the left, click **User Groups**.

- Each Group should have a **1** in the Users column for the number of Users in each Group.

- If you do not have a **1** beside each group, revisit the above instructions to ensure that each user is assigned to a Group, as shown
in the table in the Business Scenario section.

16. click the users from the sidebar andclick *user-1*  and look at the *permissions* click the permissions and inspect the *JSON* format of the policy.

# Task 3: Sign-In and Test Users
------------------------------

In this task, you will test the permissions of each IAM User.

17. In the navigation pane on the left, click **Dashboard**.

An **IAM users sign-in link** is displayed.

This link can be used to sign-in to the AWS Account you are currently using.

18. Copy the **IAM users sign-in link** to a text editor.

19. Open a private window.<Yani gizli sekme>


20. Paste the **IAM users sign-in** link into your private window and press **Enter**.

You will now sign-in as **Abuzer**, who has been hired as your Amazon S3 storage support staff.

21. Sign-in with:

-   **IAM user name:**
-   **Password:** Paste the value of *AdministratorPassword* located to the left of these instructions.

22. In the **Services** menu, click **S3**.

23. Try to list *S3 Bucket*

Since your user is part of the **S3-Support** Group in IAM, they have permission to view a list of Amazon S3 buckets and the contents of the **S3**.

Now, test whether they have access to Amazon EC2.

25. In the **Services** menu, click **EC2**.

26. Navigate to the region that your lab was launched in by:

-   Clicking the drop-down ** arrow at the top of the screen, to the left of **Support**
-   Selecting the region value that matches the value of **Region** to the left of these instructions

27. In the left navigation pane, click **Instances**.

You cannot see any instances. This is because your user has not been assigned any permissions to use Amazon EC2.

You will now sign-in as **Abuzer**, who has been hired as your Amazon EC2 support person.

28. `Sign Abuzer out` of the **AWS Management Console** by configuring the
    following:

-   At the top of the screen, click **Abuzer**
-   Click **Sign Out**

29. Paste the **IAM users sign-in** link into your private window and press **Enter**.

This links should be in your text editor.

30. Sign-in with:

-   **IAM user name:Muhittin**
-   **Password:** Paste the value of *AdministratorPassword* located to the left of these instructions.

31. In the **Services** menu, click **EC2**.

* At the top right of the screen, enable **New EC2 Experience** by toggling the button, if it is not enabled by default.

32. Navigate to the region that your lab was launched in by:

-   Clicking the drop-down ** arrow at the top of the screen, to the
    left of **Support**
-   Selecting the region value that matches the value of **Region** to
    the left of these instructions

33. In the navigation pane on the left, click **Instances**.

- You are now able to see an Amazon EC2 instance because you have Read Only permissions. However, you will not be able to make any changes to
Amazon EC2 resources.

Your EC2 instance should be selected ** If it is not selected, select ** it.

34. In **Instance state**, menu click **Stop instance**.

35. In the **Stop instance** window, click **Stop**.

* You will receive an error stating *You are not authorized to perform this operation*. This demonstrates that the policy only allows you to
information, without making changes.

36. Close the displayed error message.

-   Next, check if Muhittin can access Amazon S3.

37. In the **Services**, click **S3**.

-   You will receive an ** **Error Access Denied** because user-2 does not permission to use Amazon S3.

38. You will now sign-in as **Ali**, who has been hired as your Amazon EC2 administrator.

-   `Sign Muhittin out` of the **AWS Management Console** by configuring the
    following:

-   At the top of the screen, click **Muhittin**

-   Click **Sign Out**

39. Paste the **IAM users sign-in** link into your private window and press **Enter**.

40. Paste the sign-in link into your web browser address bar again. If it is not in your clipboard, retrieve it from the text editor where you stored it earlier.

41. Sign-in with:

-   **IAM user name:**
-   **Password:** Paste the value of *AdministratorPassword* located to the left of these instructions.

42. In the **Services** menu, click **EC2**.

43. Navigate to the region that your lab was launched in by:

-   Clicking the drop-down ** arrow at the top of the screen, to the left of **Support**
-   Selecting the region value that matches the value of **Region** to the left of these instructions

44. In the navigation pane on the left, click **Instances**.

-   As an EC2 Administrator, you should now have permissions to Stop the Amazon EC2 instance.

-   Your EC2 instance should be selected **. If it is not, please select  ** it.

45. In **Instance state**, menu click **Stop instance**.

46. In the **Stop Instance** window, click **Stop**.

-   The instance will enter the *stopping* state and will shutdown.

47. Close your private window.

End Lab
-------

This lab shows you how to manage access and permissions to your AWS services using AWS Identity and Access Management (IAM). Practice the
steps to add users to groups, manage passwords, log in with IAM-created users, and see the effects of IAM policies on access to specific
services.