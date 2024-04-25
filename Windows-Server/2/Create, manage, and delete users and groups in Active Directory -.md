## Preview

- Oncelikle Windows 10'un kurulumunu yap. Kurulumu da `New Virtual Machine > Typical > ISO > SW_DVD... > Windows 10 Pro > Customize Hardware(Network olarak NAT secili kalsin > Finish`
- **`Windows10` ve `Windows Server 2012` makinalarinin saat ve tarihleri ayni olmali!!**
- Sonrasinda gecen ders kurdugun `Windows Server 2012` makinasina git;

## Create a new Organizational Unit in Active Directory

1. `Active Directory Users and Computers`i ac.

2. `devops.com` a sag tikla ve `New > Organizational Unit` i sec.

3. Burada iki tane OU olusturacagiz: **Ankara** ve **Izmir**. Bu iki OU'nun altinda 3'er OU daha olacak: **Computers**, **Users**, **Groups**

```txt
Ankara
    Computers
        HR
        IT
    Users
    Groups
Izmir
    Computers
        HR
        IT
    Users
    Groups
```

-----------------------------------------------------------------------------------------
## Create a new user in Active Directory

Use the following steps to create a new user in Active Directory:

1.  Log in to your domain controller(`Windows Server 2012`) by using the Remote Desktop.

2.  Use one of the following options to open **Active Directory Users
    and Computers** :

    -   Right-click the **Start** menu, select **Run**, enter
        **dsa.msc**, and click **OK**.

    -   Use the Windows® search function by clicking on **Start** and
        entering **dsa.msc**.

    -   Click on **Server Manager -\> Tools** and select **Active
        Directory Users and Computers** from the menu.

3.  Expand your domain from the left-hand menu.

4.  Depending on whether you are using organizational units or not, find
    the appropriate object to place the user in. By default, you can use
    the **Users** object if you do not have or plan to create an
    organizational unit.

5.  After you find the appropriate object for the new user, right-click
    it, select **New** from the menu, and select **User**.

6.  In the **New Object - User** window, enter the **First Name**,
    **Last Name**, and **User logon name**. When you enter the **First
    Name** and **Last Name**, the wizard auto-populates the **Full
    Name**. **Note**: If you use the **User logon name
    (pre-Windows 2000)**, this choice limits you to 20 characters.

7.  Click **Next**. For the new password, we recommend using an online
    tool to generate a random password or creating a complex password
    that includes at least three of the four following categories:

    -   English uppercase characters (A through Z)

    -   English lowercase characters (a through z)

    -   Base 10 digits (0 through 9)

    -   Non-alphabetic characters (For example, !, \$, \#, %)

8.  Input the password. When finished, click **Next**.

9.  After you review the **Summary**, click **Finish**.

10. Create 8 users in total for OU's constantly

```txt
Admin: User for devops.com domain
  Coordinator: User coordinates Ankara and Izmir OU's; less authority than Admin
    Ankara Lead: User for Ankara
        IT Support Ankara: User for Ankara/IT
        HR: HR for Ankara
    Izmir Lead: User for Izmir
        IT Support Izmir: User for Izmir/IT
        HR: HR for Izmir
```
-----------------------------------------------------------------------
## Create a new group within Active Directory

Use the following steps to create a new group in Active Directory:

1.  Log in to your domain controller by using the Remote Desktop.

2.  Use one of the following options to open **Active Directory Users
    and Computers**:

    -   Right-click the **Start** menu, select **Run**, enter
        **dsa.msc**, and click **OK**.

    -   Use the Windows search function by clicking on **Start** and
        entering **dsa.msc**.

    -   Click on **Server Manager -\> Tools** and select **Active
        Directory Users and Computers** from the menu.

3.  Expand your domain from the left-hand menu.

4.  Depending on whether you are using organizational units or not, find
    the appropriate object to place the user in. By default, the
    built-in Microsoft default groups are under the **Users**
    organization unit. If you prefer, you can put the user in a custom
    organization unit.

5.  Right-click the object you want to choose for the user, select
    **New**, and select **Group**.

6.  In the wizard, enter your group name. By default, the wizard
    preselects **Global** under **Group Scope** and **Security** under
    **Group Type**. Do not change the group type to **Distribution**
    because that option creates distribution groups for Microsoft
    Exchange® and e-mail.


------------------------------------------------------------------------
## Add or remove users to or from a group

You can add and remove a user to or from a group from the **Group** or
from the **User**. This section describes both options.

Use the following steps to add or remove a users to or from groups in
Active Directory:

1.  Log in to your domain controller by using Remote Desktop.

2.  Use one of the following options to open **Active Directory Users
    and Computers**:

    -   Right-click the **Start** menu, select **Run**, enter
        **dsa.msc**, and click **OK**.

    -   Use the Windows search function by clicking on **Start** and
        entering **dsa.msc**.

    -   Click on **Server Manager -\> Tools** and select **Active
        Directory Users and Computers** from the menu.

3.  Expand your domain from the left-hand menu.

- Kullanicini olusturdun, olusturdugun kullaniciya sag tikladin ve `properties`'ini actin. Oradan `Account > Logon Hours` dersen kullanicinin hangi saat araliginda giris yapip domain'ine baglanabilecegini belirleyebilirsin. `Account Expires > End of` tan tarih secersen de kullanici sectigin tarihe kadar var olur. 
- `Member of` a tiklarsan mesela kullanicinin uyesi oldugu gruplari gorebilirsin. 
    - Burada `Domain Users` grubu slaytta soyledigim gibi kullaniciya default tanimli gelmis..
    - Kullaniciyi ayni zamanda gruplara da burdan eklersin.
    - `Set Primary Groups` ile de eger kullanici birden fazla gruba uyeyse secim durumunda hangi grubun onceliklu olacagini belirleyebilirsin.

4.  To add the user to a group from the **Group**, use the following
    steps:

    a\. Right-click your domain and select **Find**. Ensure that you
    select **Users, Contacts, and Groups** from the **Find** drop-down
    menu. Enter the **Name** of the group and click **Find Now**.

    b\. Right-click the group and select **Properties**.

    c\. Click the **Members** tab.

    d\. To remove a user, click the user to highlight it and click
    **Remove**.

    e\. To add a user, click **Add**. Type the username into **Enter the
    object names to select**. Click **Check Names**. Click **OK** when
    the wizard underlines the name.

5.  To add a user to a group from the **User**, use the following steps:

    a\. Right-click your domain and select **Find**. Ensure that you
    select **Users, Contacts, and Groups** from the **Find** drop-down
    menu. Enter the **Name** of the user and click **Find Now**.

    b\. Right-click the user and select **Properties**.

    c\. Click the **Member Of** tab.

    d\. To remove the user from a group, click the group and click
    **Remove**.

    e\. To add the user to a group click **Add**. Type the group name
    into **Enter the object names to select**. Click **Check Names** and
    click **OK** when the wizard underlines the name.

- Create 5 groups and add the users as follows:

```txt
Admins: devops.com(admin, coordinator)
    Ankara: Ankara(Ankaralead, hrankara, itankara)
    Izmir: Izmir(Izmirlead, hrizmir, itizmir)

    hr: devops.com(hrankara, hrizmir)
    it: devops.com(itankara, itizmir)
```

-----------------------------------------------------------------------
## Delete or remove a user from Active Directory

Use the following steps to delete a new user from Active Directory:

1.  Log in to your domain controller by using Remote Desktop.

2.  Use one of the following options to open **Active Directory Users
    and Computers**:

    -   Right-click the **Start** menu, select **Run**, enter
        **dsa.msc**, and click **OK**.

    -   Use the Windows search function by clicking on **Start** and
        entering **dsa.msc**.

    -   Click on **Server Manager -\> Tools** and select **Active
        Directory Users and Computers** from the menu.

3.  Expand your domain from the left-hand menu.

4.  To use the **Find** function in Active Directory, right-click your
    domain and select **Find**. Ensure that you select **Users,
    Contacts, and Groups** from the **Find** drop-down menu. Then, type
    the **Name** of the user you want to delete.

5.  You can delete or disable the user. **Note**: Deleting the user is
    not reversible.

    -   To delete the user, right-click the user and select **delete**.
        Click **Yes** in the confirmation window if you are sure.

    -   To disable the user, right-click the user and select
        **disable**. Click **Yes** in the confirmation window if you are
        sure.

- Remove the following users from the `HR` and `IT` groups:

```txt
hrizmir
itankara
```
--------------------------------------------------------------------------------
## Delete a Group within Active Directory

Use the following steps to delete a group from Active Directory:

1.  Log in to your domain controller by using Remote Desktop.

2.  Use one of the following options to open **Active Directory Users
    and Computers**:

    -   Right-click the **Start** menu, select **Run**, enter
        **dsa.msc**, and click **OK**.

    -   Use the Windows search function by clicking on **Start** and
        entering **dsa.msc**.

    -   Click on **Server Manager -\> Tools** and select **Active
        Directory Users and Computers** from the menu.

3.  Expand your domain from the left-hand menu.

4.  To use the **Find** function within Active Directory, right-click
    your domain and select **Find**. Ensure that you select **Users,
    Contacts, and Groups** from the **Find** drop down menu. Type the
    **Name** of the group you want to delete.

5.  Right-click the group and select **delete**. Click **Yes** in the
    confirmation window if you are sure.

- Delete the `HR` and `IT` groups..
---------------------------------------------------------------------------------
