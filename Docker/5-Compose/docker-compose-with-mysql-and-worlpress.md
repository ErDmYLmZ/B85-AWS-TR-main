# Hands-on Docker-Compose : Compose and WordPress

- Purpose of the this hands-on  use Docker Compose to easily run WordPress in an isolated environment built with Docker containers. This hands-on demonstrates how to use Compose to set up and run WordPress. Before starting, make sure you have Compose installed.

## Learning Outcomes

At the end of the this hands-on training, students will be able to;

- explain what Docker Compose is.

- install docker-compose-cli

- explain what the `docker-compose.yml` is.

- build a `wordpress` and `MYSQL Database`  application running on Docker Compose.

## Outline

- Part 1 - Launch a Docker Machine Instance and Connect with SSH

- Part 2 - Installing Docker Compose

- Part 3 - Building a Wordpress Web Application using Docker Compose

## Part 1 - Launch a Docker Machine Instance and Connect with SSH

- Launch a Docker machine on Amazon Linux 2 AMI with security group allowing SSH connections using.

- Connect to your instance with SSH.

- Security Groups:

```bash
(SSH)TCP 22 Anywhere
HTTP 80 Anywhere
Custom TCP 8000 Anywhere
```

```bash
ssh -i "key.pem" ec2-user@<PUBLIC_IP_ADDRESS>
```

## Part 2 - Installing Docker Compose

- For Linux systems, after installing Docker, you need install Docker Compose separately. But, Docker Desktop App for Mac and Windows includes `Docker Compose` as a part of those desktop installs.

- Download the current stable release of `Docker Compose` executable.

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" \
-o /usr/local/bin/docker-compose
```

- Apply executable permissions to the binary:

```bash
sudo chmod +x /usr/local/bin/docker-compose
```

- Check if the `Docker Compose`is working. Should see something like `docker-compose version 1.26.2, build 1110ad01`

```bash
docker-compose --version
```

## Part 3 - Building a WordPress application in an isolated environment built with Docker containers

- Create an empty project directory.
  
```bash
mkdir my_wordpress/
```

- Change into your project directory.

```bash
cd my_wordpress/
```
- Create a docker-compose.yml file that starts your WordPress blog and a separate MySQL instance with volume mounts for data persistence:

```yaml
version: "3.9"
    
services:
  db:
    image: mysql:5.7
    volumes:
      - db_data:/var/lib/mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: somewordpress
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
    
  wordpress:
    depends_on:
      - db
    image: wordpress:latest
    volumes:
      - wordpress_data:/var/www/html
    ports:
      - "8000:80"
    restart: always
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpress
      WORDPRESS_DB_NAME: wordpress
volumes:
  db_data: {}
  wordpress_data: {}
```
- `docker-compose.yml` in aciklamasi:TR

```yaml
version: "3.9"
    
services: # iki adet servisimiz var
  db: # iki servisimizden biri DB
    image: mysql:5.7 # image olarak mysql kullanmisim
    volumes:
      - db_data:/var/lib/mysql # Olusturdugumuz DB deki veriler kaybolmasin diye bir tane de volume olusturmusum.
    restart: always
    environment: # Zorunlu mysql image tanimlamalarini wordpress icin yaptim
      MYSQL_ROOT_PASSWORD: somewordpress
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpress
    
  wordpress:
    depends_on: # once db'i kur
      - db
    image: wordpress:latest # wordpress'in en son imajini cekiyor
    volumes:
      - wordpress_data:/var/www/html
    ports:
      - "8000:80"
    restart: always
    environment:
      WORDPRESS_DB_HOST: db:3306 #hostname'i mysql'dan alacagim
      WORDPRESS_DB_USER: wordpress # mysql'e tanimladigimiz degiskenler
      WORDPRESS_DB_PASSWORD: wordpress # mysql'e tanimladigimiz degiskenler
      WORDPRESS_DB_NAME: wordpress # mysql'e tanimladigimiz degiskenler
volumes: # volume tanimlamak icin
  db_data: {}
  wordpress_data: {}

# Gordugunuz gibi hicbir dosyam veya uygulamam yok; her seyi docker hub'tan cekecek.
```

- The docker volumes ```db_data``` and ```wordpress_data``` persists updates made by WordPress to the database, as well as the installed themes and plugins.

- WordPress Multisite works only on ports ```80 and 443```.

## Part 4 - Building the project


- Now, run `docker-compose up -d` from your project directory.

```bash
docker-compose up -d
```

- This runs docker-compose up in detached mode, pulls the needed Docker images, and starts the `wordpress` and `MYSQL database` containers.


## Part 5 - Bringing up WordPress in a web browser

- At this point, WordPress should be running on port 8000 of your Docker Host, and you can complete the “famous five-minute installation” as a WordPress administrator.

- If you are using Docker Machine, you can run the command docker-machine ip MACHINE_VM to get the machine address, and then open http://MACHINE_VM_IP:8000 in a web browser.

- If you are using Docker Desktop for Mac or Docker Desktop for Windows, you can use http://localhost as the IP address, and open http://localhost:8000 in a web browser.

- If you are using AWS EC2 instance, enter `http://ec2-host-name:8000` in a browser to see the application running.

## Part 6 - Shuting down and cleanup

- The command docker-compose down removes the containers and default network, but preserves your WordPress database.

```bash
docker-compose down
```
- The command docker-compose down --volumes removes the containers, default network, and the WordPress database.

```bash
docker-compose down --volumes
```