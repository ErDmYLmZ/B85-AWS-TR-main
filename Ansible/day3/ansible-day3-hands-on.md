# Hands-on Ansible-03 : Using vars, facts and secrets

Purpose of the this hands-on training is to give students the knowledge of ansible facts gathering and working with secret values.

## Learning Outcomes

At the end of this hands-on training, students will be able to;

- Explain how and what facts gathering is and how to use it in the playbook
- Learn how to deal with secret values with ansible-vault

## Outline

- Part 1 - Ansible Variables

- Part 2 - Ansible Facts

- Part 3 - Working with sensitive data


## Part 0 - Install Ansible


- Spin-up 3 Amazon Linux 2 instances and name them as:
    1. control node
    2. node1 ----> (SSH PORT 22, HTTP PORT 80)
    3. node2 ----> (SSH PORT 22, HTTP PORT 80)


- Connect to the control node via SSH and run the following commands.

```bash
sudo yum update -y
sudo amazon-linux-extras install ansible2
```

### Confirm Installation

- To confirm the successful installation of Ansible, run the following command.

```bash
$ ansible --version
```
Stdout:
```
ansible 2.9.12
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/ec2-user/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 2.7.18 (default, Aug 27 2020, 21:22:52) [GCC 7.3.1 20180712 (Red Hat 7.3.1-9)]
```
- Explain the lines above:
    1. Version Number of Ansible
    2. Path for the Ansible Config File
    3. Modules are searched in this order
    4. Ansible's Python Module path
    5. Ansible's executable file path
    6. Ansible's Python version with GNU Compiler Collection for Red Hat

### Configure Ansible on the Control Node

- Connect to the control node for building a basic inventory.

- Edit ```/etc/ansible/hosts``` file by appending the connection information of the remote systems to be managed.

- Along with the hands-on, public or private IPs can be used.

```bash
$ sudo su
$ cd /etc/ansible
$ ls
$ vim hosts
[webservers]
node1 ansible_host=<node1_ip> 

[dbservers]
node2 ansible_host=<node2_ip> 

[all:vars]
ansible_user=ec2-user
ansible_ssh_private_key_file=/home/ec2-user/<pem file>
```

- Explain what ```ansible_host```, ```ansible_user``` and ansible_ssh_key_file parameters are. For this reason visit the Ansible's [inventory parameters web site](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#connecting-to-hosts-behavioral-inventory-parameters).

- Explain what an ```alias``` (node1 and node2) is and where we use it.

- Explain what ```[webservers] and [all:vars]``` expressions are. Elaborate the concepts of [group name](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#inventory-basics-formats-hosts-and-groups), [group variables](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#assigning-a-variable-to-many-machines-group-variables) and [default groups](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html#default-groups). 

- Visit the above links for helping to understand the subject. 

- Copy your pem file to the /home/ec2-user directory. First, go to your pem file directory on your local PC and run the following command.

```bash
$ scp -i <pem file> <pem file> ec2-user@<public DNS name of Control Node>:/home/ec2-user
```
- Check if the file is transferred to the remote machine. 

- As an alternative way, create a file on the control node with the same name as the <pem file> in ```/etc/ansible``` directory. 

- Then copy the content of the pem file and paste it in the newly created pem file on the control node.

- To make sure that all our hosts are reachable, we will run various ad-hoc commands that use the ping module.

```bash
$ chmod 400 <pem file>
```

```bash
$ ansible all -m ping -o
# hata alirsan once ansible dbservers -m ping -o sonra ansible all -m ping -o yaz.
```

## Part 1 - Ansible Variables

In Ansible a value is assigned to a variable that can be then referenced in a playbook or on command line during playbook runtime. Variables can be used in playbooks, inventories, and at the command line as we have just mentioned.

Variables in Playbooks

var1.yaml

```bash
---
- hosts: all
  vars:
    greetings: Hello everyone!

  tasks:
  - name: Ansible Simple Variable Example Usage
    debug:
      msg: "{{ greetings }}, Let’s learn Ansible variables"
```

var2.yaml

```bash
---
- hosts: all
  vars:
    students:
      - Alice
      - Mark
      - Peter

  tasks:
  - name: Ansible Array Usage Example
    debug:
      msg: "{{ students }}"
```

var3.yaml

```bash
---
- hosts: all
  tasks:
    - name: Create new users
      user:
        name: '{{ item }}'
        state: present

      loop:
        - mike
        - sandra
```

- variables can be assigned using external files

varsfile.yaml

```bash
  username: johnwayne
  password: wayne123
```

var4.yaml

```bash
---
- hosts: all
  vars_files:
    - ~/varsfile.yaml
  tasks:
  - name: user name and password from external var file
    debug:
      msg: "{{ username}}, {{ password }}"
```

## Part 2 - Ansible Facts

- Gathering Facts:

```bash
$ ansible node1 -m setup
```
```
ec2-34-201-69-79.compute-1.amazonaws.com | SUCCESS => {
    "ansible_facts": {
        "ansible_all_ipv4_addresses": [
            "172.31.20.246"
        ],
        "ansible_all_ipv6_addresses": [
            "fe80::88c:37ff:fe8f:3b71"
        ],
        "ansible_apparmor": {
            "status": "disabled"
        },
        "ansible_architecture": "x86_64",
        "ansible_bios_date": "08/24/2006",
        "ansible_bios_vendor": "Xen",
        "ansible_bios_version": "4.2.amazon",
        "ansible_board_asset_tag": "NA",
        "ansible_board_name": "NA",
        "ansible_board_serial": "NA",
```
- create a playbook named "facts.yml"

```yml
- name: show facts
  hosts: all
  tasks:
    - name: print facts
      debug:
        var: ansible_facts
```
- run the play book

```bash
$ ansible-playbook facts.yml
```

- create a playbook named "ipaddress.yml"

```yml
- hosts: all
  tasks:
  - name: show private IP address
    debug:
      msg: >
       This host uses private IP address {{ ansible_facts.default_ipv4.address }}

```
- run the playbook

```bash
ansible-playbook ipaddress.yml 
```

- create another yaml file for another fact

```yaml
- hosts: all
  tasks:
  - name: show architecture
    debug:
      msg: >
       This host uses {{ ansible_facts.architecture }} architecture
```






- dump the facts of a target host

```bash
ansible -m setup node1
```

- the result has 3 types of data

- dictionary
- list
- ansibleunsafetext

- dictionary 
"ansible_all_ipv4_addresses": [
            "172.31.95.236"
        ], 

- list or array
"ansible_apparmor": {
            "status": "disabled"
        }, 

- ansibleunsafetext
"ansible_architecture": "x86_64", 
"ansible_bios_date": "08/24/2006", 
"ansible_bios_version": "4.11.amazon",



- now let's create another yaml file to get those facts from the remote host

facts2.yaml

```yaml
---
- name: Ansible Variable Example Playbook
  hosts: node1
  tasks:


    # display the variable data type
    - debug:
        msg: 
          - " Data type of 'ansible_architecture'  is {{ ansible_architecture | type_debug }} "
          - " Data type of 'ansible_apparmor' is {{ ansible_apparmor | type_debug }} "
          - " Data type of 'ansible_all_ipv4_addresses' is {{ ansible_all_ipv4_addresses | type_debug }} "

    # Simply printing the value of fact which is Ansible UnSafe Text type
    - debug:
        msg: "{{ ansible_architecture }}"


    # Accessing an element of dictionary
    - debug:
        msg: "{{ansible_apparmor.status}}"

    # Accessing the list
    - debug:
        msg: "{{ansible_all_ipv4_addresses}}"

    # Accessing the Second Element of the list
    - debug:
        msg: "{{ansible_all_ipv4_addresses[0]}}"

```


- this exercise shows how to parse through a variable dictionary and how to run a command on a specific host

- parse.yaml

```yaml
---
- name: Ansible Variable Example Playbook
  hosts: node1
  tasks:

    # Print the Dictionary
    - debug:
        msg: "{{ansible_mounts}}"

    # Parsing through Variable Dictionary
    - debug:
        msg: "Mount Point {{item.mount}} is at {{item.block_used/item.block_total*100}} percent "
      loop: "{{ansible_mounts}}"

    # Execute Host based task using variable
    - name: Execute the command only node2 server
      become: yes
      become_user: root 
      shell: "uname -a"
      when: "{{ ansible_hostname == 'node2'}}"
```


## Part 3 - Working with sensitive data

- Create encypted variables using "ansible-vault" command

```bash
ansible-vault create secret.yml
```

New Vault password: xxxx
Confirm New Vault password: xxxx

```yml
username: tony
password: 123456a
```

- look at the content

```bash
$ cat secret.yml
```
```
33663233353162643530353634323061613431366332373334373066353263353864643630656338
6165373734333563393162333762386132333665353863610a303130346362343038646139613632
62633438623265656330326435646366363137373333613463313138333765366466663934646436
3833386437376337650a636339313535323264626365303031366534363039383935333133306264
61303433636266636331633734626336643466643735623135633361656131316463
```
- how to use it:

- create a file named "create-user"

```bash
$ nano create-user.yml

```

```yml
- name: create a user
  hosts: all
  become: true
  vars_files:
    - secret.yml
  tasks:
    - name: creating user
      user:
        name: "{{ username }}"
        password: "{{ password }}"
```

- run the plaaybook

```bash
ansible-playbook create-user.yml
```
```bash
ERROR! Attempting to decrypt but no vault secrets found
```
- Run the playbook with "--ask-vault-pass" command:

```bash
$ ansible-playbook --ask-vault-pass create-user.yml
```
Vault password: xxxx

```
PLAY RECAP ******************************************************************************************
node1                      : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
node2                      : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

- To verify it

```bash
ansible all -b -m command -a "grep tony /etc/shadow"
```
```
node1 | CHANGED | rc=0 >>
tony:99abcd:18569:0:99999:7:::
```

- Create another encypted variables using "ansible-vault" command but this time use SHA (Secure Hash Algorithm) for your password:

```bash
ansible-vault create secret-1.yml
```

New Vault password: xxxxx
Confirm Nev Vault password: xxxxx

```yml
username: Erling
pwhash: 06dmpnr
```

- look at the content

```bash
$ cat secret-1.yml
```
```
33663233353162643530353634323061613431366332373334373066353263353864643630656338
6165373734333563393162333762386132333665353863610a303130346362343038646139613632
62633438623265656330326435646366363137373333613463313138333765366466663934646436
3833386437376337650a636339313535323264626365303031366534363039383935333133306264
61303433636266636331633734626336643466643735623135633361656131316463
```
- how to use it:

- create a file named "create-user-1"

```bash
$ nano create-user-1.yml

```

```yml
- name: create a user
  hosts: all
  become: true
  vars_files:
    - secret-1.yml
  tasks:
    - name: creating user
      user:
        name: "{{ username }}"
        password: "{{ pwhash | password_hash ('sha512') }}"     
``` 

- run the plaaybook


```bash
$ ansible-playbook --ask-vault-pass create-user-1.yml
```
Vault password: xxxxx

```
PLAY RECAP ******************************************************************************************
node1                      : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
node2                      : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

- to verrify it:

```bash
ansible all -b -m command -a "grep Erling /etc/shadow"
```
```
node1 | CHANGED | rc=0 >>
tyler:#665fffgkg6&fkg689##2£6466?%^^+&%+:18569:0:99999:7:::
```

# Hands-on Ansible-04: Working with Dynamic Inventory Using EC2 Plugin

The purpose of this hands-on training is to give students the knowledge of using dynamic inventory.

## Learning Outcomes

At the end of this hands-on training, students will be able to;

- Explain what is dynamic inventory
- Explain how to use dynamic inventory with EC2 plugin.


## Outline

- Part 1 - Build the Infrastructure

- Part 2 - Install Ansible on the Controller Node

- Part 3 - Pinging the Target Nodes with static inventory

- Part 4 - Working with dynamic inventory


## Part 1 - Build the Infrastructure

- Get to the AWS Console and spin-up 3 EC2 Instances with ```Amazon Linux 2``` AMI.

- Configure the security groups as shown below:

    - Controller Node ----> Port 22 SSH

    - Target Node1 -------> Port 22 SSH, Port 80 HTTP

    - Target Node2 -------> Port 22 SSH, Port 80 HTTP

## Part 2 - Install Ansible on the Controller Node

- Connect to your ```Controller Node```.

- Optionally you can connect to your instances using VS Code.

                    -------------------- OPTIONAL BELOW ----------------------

- You can also connect to the Controller Node via VS Code's ```Remote SSH``` Extension. 

- Open up your VS Code editor. 

- Click on the ```Extensions``` icon. 

- Write down ```Remote - SSH``` on the search bar. 

- Click on the first option on the list.

- Click on the install button.

- When the extension is installed, restart your editor.

- Click on the green button (```Open a Remote Window``` button) at the most bottom left.

- Hit enter. (```Connect Current Window to Host...```)

- Enter a name for your connection on the input field and click on ```Add New SSH Host``` option.

- Enter your ssh connection command (```ssh -i <YOUR-PEM-FILE> ec2-user@<YOUR SERVER IP>```) on the input field and hit enter.

- Hit enter again.

- Click on the ```connect``` button at the bottom right.

- Click on ```continue``` option.

- Click on the ```Open Folder``` button and then click on the ```Ok``` button.

- Lastly, open up a new terminal on the current window.

                    -------------------- OPTIONAL ABOVE ----------------------


## Part 3 - Pinging the Target Nodes with static inventory


- Make a directory named ```dynamic-inventory``` under the home directory and cd into it.

```bash 
$ mkdir dynamic-inventory
$ cd dynamic-inventory
```

- Create a file named ```inventory.txt``` with the command below.

```bash
$ nano inventory.txt
```

- Paste the content below into the inventory.txt file.

- Along with the hands-on, public or private IPs can be used.

```txt
[servers]
db_server   ansible_host=<YOUR-DB-SERVER-IP>   ansible_user=ec2-user  ansible_ssh_private_key_file=~/<YOUR-PEM-FILE>
web_server  ansible_host=<YOUR-WEB-SERVER-IP>  ansible_user=ec2-user  ansible_ssh_private_key_file=~/<YOUR-PEM-FILE>

- Create file named ```ansible.cfg``` under the the ```dynamic-inventory``` directory.

```bash
$ nano ansible.cfg
```

```cfg
[defaults]
host_key_checking = False
inventory=/etc/ansible/hosts
interpreter_python=auto_silent
private_key_file=~/<pem file>
```


- Create a file named ```ping-playbook.yml``` and paste the content below.

```bash
chmod 400 /home/ec2-user/deneme.pem
$ nano ping-playbook.yml
```

```yml
- name: ping them all
  hosts: all
  tasks:
    - name: pinging
      ping:
```

- Run the command below for pinging the servers.

```bash
$ ansible-playbook ping-playbook.yml
```

- Explain the output of the above command.

- Change the inventory's value in ansible.cfg file to inventory.txt. 'inventory=/home/ec2-user/dynamic-inventory/inventory.txt'

- Run the command below for pinging the servers.

```bash
$ ansible-playbook ping-playbook.yml
```
## Part4 - Working with dynamic inventory

- First, let's check some plugins about inventory by entering this on the command line:

```bash
ansible-doc -t inventory -l
```
- you wil get a result list like tihs:

advanced_host_list                                      Parses a 'host list' with ranges                      
amazon.aws.aws_ec2                                      EC2 inventory source                                  
amazon.aws.aws_rds                                      rds instance source                                   
auto                                                    Loads and executes an inventory plugin specified in a ...
awx.awx.controller                                      Ansible dynamic inventory plugin for the Automation Pl...
azure.azcollection.azure_rm                             Azure Resource Manager inventory plugin               
cloudscale_ch.cloud.inventory                           cloudscale.ch inventory source                        
community.digitalocean.digitalocean                     DigitalOcean Inventory Plugin                         
community.dns.hetzner_dns_records                       Create inventory from Hetzner DNS records             
community.dns.hosttech_dns_records                      Create inventory from Hosttech DNS records            
community.docker.docker_containers                      Ansible dynamic inventory plugin for Docker containers
community.docker.docker_machine                         Docker Machine inventory source                       
community.docker.docker_swarm                           Ansible dynamic inventory plugin for Docker swarm node...
community.general.cobbler                               Cobbler inventory source                              
community.general.gitlab_runners                        Ansible dynamic inventory plugin for GitLab runners   
community.general.icinga2                               Icinga2 inventory source                              
community.general.linode                                Ansible dynamic inventory plugin for Linode           
community.general.lxd                                   Returns Ansible inventory from lxd host               
community.general.nmap                                  Uses nmap to find hosts to target                     
community.general.online                                Scaleway (previously Online SAS or Online.net) invento...
community.general.opennebula                            OpenNebula inventory source                           
community.general.proxmox                               Proxmox inventory source                              
community.general.scaleway                              Scaleway inventory source                             
community.general.stackpath_compute                     StackPath Edge Computing inventory source             
community.general.virtualbox                            virtualbox inventory source                           
community.general.xen_orchestra                         Xen Orchestra inventory source                        
community.hrobot.robot                                  Hetzner Robot inventory source                        
community.kubevirt.kubevirt                             KubeVirt inventory source                             
community.libvirt.libvirt                               Libvirt inventory source                              
community.okd.openshift                                 OpenShift inventory source                            
community.vmware.vmware_host_inventory                  VMware ESXi hostsystem inventory source               
community.vmware.vmware_vm_inventory                    VMware Guest inventory source                         
community.zabbix.zabbix_inventory                       Zabbix Inventory Plugin                               
constructed                                             Uses Jinja2 to construct vars and groups based on exis...
generator                                               Uses Jinja2 to construct hosts and groups from pattern...
google.cloud.gcp_compute                                Google Cloud Compute Engine inventory source          
hetzner.hcloud.hcloud                                   Ansible dynamic inventory plugin for the Hetzner Cloud
host_list                                               Parses a 'host list' string                           
infoblox.nios_modules.nios_inventory                    Infoblox inventory plugin                             
ini                                                     Uses an Ansible INI file as inventory source          
kubernetes.core.k8s                                     Kubernetes (K8s) inventory source                     
netbox.netbox.nb_inventory                              NetBox inventory source                               
ngine_io.cloudstack.instance                            Apache CloudStack instance inventory source           
ngine_io.vultr.vultr                                    Vultr inventory source                                
openstack.cloud.openstack                               OpenStack inventory source                            
ovirt.ovirt.ovirt                                       oVirt inventory source                                
script                                                  Executes an inventory script that returns JSON        
servicenow.servicenow.now                               ServiceNow Inventory Plugin                           
t_systems_mms.icinga_director.icinga_director_inventory Returns Ansible inventory from Icinga                 
theforeman.foreman.foreman                              Foreman inventory source                              
toml                                                    Uses a specific TOML file as an inventory source      
yaml                                                    Uses a specific YAML file as an inventory source 

- See that there is amazon.aws.aws_ec2 as EC2 inventory source

- To check whether it is installed, run 

```bash
ansible-galaxy collection list. 
```

- To install it, use: 
```bash
ansible-galaxy collection install amazon.aws
```

- To use it in a playbook, specify: 

plugin: aws_ec2

- The below requirements are needed on the local controller node that executes this inventory.
python >= 3.6
boto3 >= 1.16.0
botocore >= 1.19.0

- go to AWS Management Consol and select the IAM roles:

- click the  "create role" then create a role with "AmazonEC2FullAccess"

- go to EC2 instance Dashboard, and select the control-node instance

- select actions -> security -> modify IAM role

- select the role thay you have jsut created for EC2 full access and save it.

- install "boto3 and botocore"

```bash
$ sudo yum install pip3
$ pip3 install --user boto3 botocore
```

- Create another file named ```inventory_aws_ec2.yml``` in the project directory.

```bash
$ nano inventory_aws_ec2.yml
```

```yml
plugin: aws_ec2
regions:
  - "us-east-1"
keyed_groups:
  - key: tags.Name
filters:
  instance-state-name: running
compose:
  ansible_host: public_ip_address

```
- WARNING !! the file should end as ...aws_ec2.yml or yaml, otherwise you get errors!!

- see the inventory

```bash
$ ansible-inventory -i inventory_aws_ec2.yml --graph
```

```
@all:
  |--@aws_ec2:
  |  |--ec2-34-201-69-79.compute-1.amazonaws.com
  |  |--ec2-54-234-17-41.compute-1.amazonaws.com
  |--@ungrouped:
```
- Change the inventory's value in ansible.cfg file from inventory.txt to 'inventory=/home/ec2-user/dynamic-inventory/inventory_aws_ec2.yml'


- To make sure that all our hosts are reachable with dynamic inventory, we will run various ad-hoc commands that use the ping module.

```bash
$ ansible all -m ping --key-file "~/<pem file>"
```

- create a playbook name "user.yml"

```yml
---
- name: create a user using a variable
  hosts: all
  become: true
  vars:
    user: lisa
    ansible_ssh_private_key_file: "/home/ec2-user/<pem file>"
  tasks:
    - name: create a user {{ user }}
      user:
        name: "{{ user }}"
```
- run the playbook

```bash
$ ansible-playbook user.yml -i inventory_aws_ec2.yml
```

```bash
$ ansible all -m shell -a "tail -2 /etc/passwd"
$ ansible all -a "tail -2 /etc/passwd"
```