Network Day-7
Hands-on Lab

25th June 2022

The basic network commands in Linux will be practised in this hands-on exercise.
For the network infrastructure and subnetting, AWS services are used.

********************
--------------------
List of Actions
----------------
Creating private network of 2 sub networks
Creating subnets
Creating 2 clients and 1 web server
Data Transmission inside network
Using basic Linux network commands


Use AWS to

** Create network structure
Click VPC then click create VPC
name as yourname
select 2 public subnets
select 2 Availability Zones

** Create network nodes
Node 1---
Click EC2 and Launch Instance
Free Tier Amazon Linux 2
In the first page of Instance Details
select yourname-vpc as network
select subnet 1a
name tag as Client-1
create a new security group yourname-SG with
ssh 22
tcp 80
Select the keypair name

Note:::ICMP -omit this first, after first ping try, change it

Node 2----
Launch Instance
Free Tier Amazon Linux 2
In the first page of Instance Details
select yourname-vpc as network
select subnet 1b
name tag as Client-2
create a new security group yourname-SG with
ssh 22
tcp 80
Select the keypair name

Node 3-----
Launch Instance
Free Tier Amazon Linux 2
In the first page of Instance Details
select yourname-vpc as network
select subnet 1b
at the bottom of Instace Details first page 
user data field has to be filled with the following:

#!/bin/bash
yum update -y
yum install -y httpd.x86_64
systemctl start httpd.service
systemctl enable httpd.service
echo “Merhaba DevOpscular! bu sunucu: $(hostname -f)” > /var/www/html/index.html

name tag as Web Server
create a new security group yourname-SG with
ssh 22
tcp 80
Select the keypair name

** Connect to Client-1
ssh to client-1
use ifconfig
use
$ ip address show
$ ip a
ifconfig shows private IP, because you are behind a routing service, gateway, you are in private network

use ping
$ ping (client-2 private ip) remove ()
$ ping (server private ip) 

Can you ping? If no, ICMP ports might be closed. Go to Security Groups and find yourname-SG, edit inbound rules and add all ICMP for source all IPv4

Now, if pings are successful
lets do this:
$ sudo nano /etc/hosts
add the lines:
(private-ip) client-2
(private-ip) server
save
exit

view the contents of modified hosts file:
$ cat /etc/hosts

now type ping command with names not IPs

$ ping server
$ ping client-2


try
$ curl server
there is a web server on port 80 we can see it
on EC2 Instances page, copy the Web Server public Ip and paste into a browser and press enter to see the web page.


$ curl client-2
client-2 cannot be reached via port 80
because there is no transmission on port 80

use aws service to find out Public and Private IP addresses of the current instance, Client-1
$ curl http://169.254.169.254/latest/meta-data/local-ipv4
$ curl http://169.254.169.254/latest/meta-data/public-ipv4


** Network Commands -2
$ host public-IP of server
gives the domain
$ host google.com
gives the IP addresses

** Domain Information
$ dig google.com

** to download a file or a web page
$ curl google.com
$ wget google.com
$ curl -O google.com/doodles/childrens-day-2014-multiple-countries
$ wget google.com/doodles/new-years-day-2012

** network statistics
$ netstat

view ports
$ netstat -s

view routes
$ netstat -r

network statistics
$ ss

view TCP IPv4 connections
$ ss -t4

route network traffic
$ traceroute -n google.com
$ tracepath google.com

combination for ping and trace route
$ mtr google.com

view and set the hostname
$ sudo hostname DevOps
and type bash and enter

view and modify routing tables
$route