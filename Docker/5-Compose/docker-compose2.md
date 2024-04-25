# Hands-on Docker-Compose: Docker Compose practice


## Part 1 - Launch a Docker Machine Instance and Connect with SSH

```bash
- Ports: 6379 Anywhere
          5000 Anywhere
```
--------------------------------------------------
- Launch a Docker machine on Amazon Linux 2 AMI with security group allowing SSH connections.
- Connect to your instance with SSH.

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

## Part 3 - Building a Web Application using Docker Compose

- Create a folder for the project:
  
```bash
mkdir docker-test
cd docker-test
```

- Create a file called `app.py` in your project folder and paste the following python code in it. In this example, the application uses the Flask framework and maintains a hit counter in Redis, and  `redis` (redis bir catch DB. Yani bilgisayar acilip kapanana kadar butun bilgileri hafizasinda tutuyor; 6379 da calisir.)is the hostname of the `Redis container` on the application’s network. We use the default port for Redis, `6379`.
```bash
nano app.py
```
- TRWeb sayfasini her refresh ettiginizde sayac artiyor. uygulama bu
```python
import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
```

- Create another file called `requirements.txt` in your project folder, add `flask` and `redis` as package list.
 
- TR`requirements.txt` birden fazla `pip install` komutunun birlestirilip dosya formatina donmus halidir.
```bash
echo '
flask
redis
' > requirements.txt
```

- Create a Dockerfile which builds a Docker image and explain what it does.

```text
The image contains all the dependencies for the application, including Python itself.
1. Build an image starting with the Python 3.7 image.
2. Set the working directory to `/code`.
3. Set environment variables used by the flask command.
4. Install gcc and other dependencies
5. Copy `requirements.txt` and install the Python dependencies.
6. Add metadata to the image to describe that the container is listening on port 5000
7. Copy the current directory `.` in the project to the workdir `.` in the image.
8. Set the default command for the container to flask run.
```

```bash
echo '
FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
' > Dockerfile
```

- TRYukaridaki kodun aciklamasi:

```bash
FROM python:3.7-alpine # Bir adet alpine imaji aliyoruz. Alpine neydi, bilgisayari acip kapatincaya kadarki yapilan islemleri akilda tutan bir gecici(cache) DB
WORKDIR /code # Kod isimli bir klasor olusturduk ve o klasoru directory'miz yaptik
ENV FLASK_APP app.py # FLASK_APP in icerisine app.py i tanimladim
ENV FLASK_RUN_HOST 0.0.0.0 # Host olarak 0.0.0.0'i tanimladim
RUN apk add --no-cache gcc musl-dev linux-headers #  apk add install paketi(yum veya apt-get gibi) gcc, musl-dev ve linux-headers paketlerini kuruyoruz.
COPY requirements.txt requirements.txt # requirements.txt yi aldik ve kopyaladik.
RUN pip install -r requirements.txt # requirements.txt nin icerisindeki dependency'leri kuruyoruz.
EXPOSE 5000 # Uygulamayi 5000 portunda calismak uzere hazirliyorum.
COPY . . # Kalan dosyalari kopyaliyorum
CMD ["flask", "run"] # flask run ile calistiriyorum
```

- Create a file called `docker-compose.yml` in your project folder and define services and explain services.

```text
This Compose file defines two services: web and redis.

### Web service
The web service uses an image that’s built from the Dockerfile in the current directory. It then binds the container and the host machine to the exposed port, 5000. This example service uses the default port for the Flask web server, 5000.

### Redis service
The redis service uses a public Redis image pulled from the Docker Hub registry.
```

```bash
nano docker-compose.yml
```
```bash
version: "3"
services:
  web:
    build: .
    ports:
      - "5000:5000"
  redis:
    image: "redis:alpine"
```

```bash
TR
version: "3"

# Iki adet servis tanimlayacagiz.(Isimleri kendimiz belirliyoruz ancak belirledigimiz isimleri kullanma konusunda tutarli olmaliyiz.)
services:
  web: # Tanimladigimiz ilk servisin ismi
    build: . # Oldugu yerdeki Dockerfile 'i arayacak
    ports:
      - "5000:5000" # web servisimiz 5000 portunda yayin yapiyor. Birinci olan host ikinci olan container'in portu
  redis: # Tanimladigimiz ikinci servisin ismi
    image: "redis:alpine" # redisi imaj olarak dockerhub'tan cekecegiz
```
- Docker Compose Aciklamasi:

- Build and run your app with `Docker Compose` and explains what is happening.

```text
Docker compose pulls a Redis image, builds an image for our the app code,
and starts the services defined. In this case, the code is statically copied into the image at build time.
```

```bash
docker-compose up -d
```

- Enter http://`ec2-host-name`:5000/ in a browser to see the application running.

- Press `Ctrl+C` to stop containers, and run `docker ps -a` to see containers created by Docker Compose.

- Remove the containers with `Docker Compose`.

```bash
docker-compose down
```