# DOCKER COMPOSE

## Docker Compose
* Bir adet EC2 ayaga kaldiralim. User Data:

```bash
#! /bin/bash

yum update -y
amazon-linux-extras install docker -y
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user
newgrp
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

* Networking:
```bash
 SSH 22 Anywhere
 HTTP 80 Anywhere
 Custom TCP 5000 Anywhere
 Custom TCP 8080 Anywhere
 MYSQL 3306 Anywhere
```


```bash
# Bakalim hangi versiyonu kurmusuz
docker-compose version

# Bu ornek icin nginx'i kullanacagiz. Bu yuzden
docker run -d nginx

# docker compose dosyasini olusturup icini su sekilde dolduralim
#dosya olusturma
cat > docker-compose.yml # cikmak icin crtl + d

# Icini doldurma
version: '2' #(1)

#(2)
services:
    server_a:
        image: nginx:latest
        ports:
            - "80:80"

    server_b:
        image: nginx:latest
        ports:
            - "8080:80"
```

* Örnek bir compose dosyası oluşturduk. Dosyamız içerisinde kullandığımız version ve servicetanımları var. server_? kısımları servislere verdiğimiz alias isimlendirmelerdir. Örneğimizde 2 adet nginx tanımı yaptık. Bunlara isimler verdik ve port tanımlarını yaptık.

Artık çalıştırmaya başlayabiliriz. Sadece `docker-compose up` komutunu verelim ve sonucu görelim.

```bash
# Once bi ls'leeyim bakalim docker-compose.yml'imiz directory'mizde mi
ls
docker-compose.yml

# Guzeel, icerdeyiz. Kaldiralim ayaga
docker-compose up -d #detached modda calistiralim; hata alirsan ubuntu for windows kaynaklidir, yeniden baslat duzelir
```
* 2 adet nginx server ayağa kalktı. 80 ve 8080 portlarına giderek kontrol edebiliriz.

* `docker-compose up` komutu compose ile console bağlanmış(attached) şekilde çalıştırır. Arka planda çalıştırmak için detached mode ile çalıştırılmalıdır. Şöyle ki;
```bash



# bakalim compose ile olusturdugumuz container'larimiz calisiyor mu
sudo docker ps
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS          PORTS                                   NAMES
5e6e5462036d   nginx:latest   "/docker-entrypoint.…"   7 minutes ago   Up 24 seconds   0.0.0.0:8001->80/tcp, :::8001->80/tcp   talfik_server_a_1
ed823bed7600   nginx:latest   "/docker-entrypoint.…"   7 minutes ago   Up 24 seconds   0.0.0.0:8003->80/tcp, :::8003->80/tcp   talfik_server_b_1

# Containerlari durduralim
docker-compose stop
Stopping talfik_server_a_1 ... done
Stopping talfik_server_b_1 ... done
```
* Shutdown/Clean up komutları ise şöyle;

    * `docker-compose down` : Containerları sil.
    * `docker-compose down –volumes` : Containerları volumeleri ile birlikte kaldır. Bu aşamadan sonra containerın datalarına ulaşamayacağız.

* Not: compose da kullanabileceğiniz tüm komutların listesini docker-compose komutunu kullanarak görebilirsiniz.
--------------------------------------------------------------------

--------------------------------------------------------------------

## Homework: Docker Compose

1. First create a `redis` database container called redis, image `redis:alpine`.

if you are unsure, check the hints section for the exact commands.

```bash
Run the command: `docker run --name redis -d redis:alpine`
```

2. Next, create a `docker-compose.yml` with the 2 services as follows:

    * Name the first service as `server_a`. image should be redis(latest) and ports should be 8085:80

    * Name the second service as `server_b`. image should be nginx:latest and ports should be 8002:80

```bash
cat > docker-compose.yml

version: '2' #(1)

#(2)
services:
    server_a:
        image: redis:latest
        ports:
            - "8085:80"

    server_b:
        image: nginx:latest
        ports:
            - "8002:80"
```

3. run the docker-compose file.

```bash
sudo docker-compose run
```

4. Let's clean up the actions carried out in previous steps. Delete the `redis`  container.

```bash
To stop the containers: `sudo docker stop <CONTAINER-NAME>`
To delete the containers: `sudo docker rm <CONTAINER-NAME>`
```