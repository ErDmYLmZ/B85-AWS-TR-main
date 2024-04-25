## 1. What is Docker?

* Docker is an open-source lightweight containerization technology. It has gained widespread popularity in the cloud and application packaging world. It allows you to automate the deployment of applications in lightweight and portable containers.

## 2. What are the advantages of using Docker container?
* Here, are a major advantage of using Docker.

    Offers an efficient and easy initial set up
    Allows you to describe your application lifecycle in detail
    Simple configuration and interacts with Docker Compose.
    Documentation provides every bit of information.

## 3. What are the important features of Docker?

* Here are the essential features of Docker:

    Easy Modeling
    Version control
    Placement/Affinity
    Application Agility
    Developer Productivity
    Operational Efficiencies

## 4. What are the main drawbacks of Docker?

* Some notable drawbacks of Docker are:

    Doesn’t provide a storage option
    Offer a poor monitoring option.
    No automatic rescheduling of inactive Nodes
    Complicated automatic horizontal scaling set up

## 5. What is Docker image?

* The Docker image help to create Docker containers. You can create the Docker image with the build command. Due to this, it creates a container that starts when it begins to run. Every docker images are stored in the Docker registry.

## 6. What is Docker Engine?

* Docker daemon or Docker engine represents the server. The docker daemon and the clients should be run on the same or remote host, which can communicate through command-line client binary and full RESTful API.

## 7. Explain Registries

* There are two types of registry is

    Public Registry
    Private Registry

## 8. What command should you run to see all running container in Docker?

```bash
$ docker ps
```

## 9. Write the command to stop the docker container

```bash
$ sudo docker stop container name
```

## 10. What is the command to run the image as a container?

```bash
$ sudo docker run -i -t alpine /bin/bash
```

## 11. What are the common instruction in Dockerfile?

* The common instruction in Dockerfile are: FROM, LABEL, RUN, and CMD.

## 12. Explain Docker Swarm.

* Docker Swarm is native gathering for docker which helps you to a group of Docker hosts into a single and virtual docker host. It offers the standard docker application program interface.

## 13. What the states of Docker container?

* Important states of Docker container are:

    Running
    Paused
    Restarting
    Exited

## 14. What is Docker hub?

* Docker hub is a cloud-based registry that which helps you to link to code repositories. It allows you to build, test, store your image in Docker cloud. You can also deploy the image to your host with the help of Docker hub.

## 15. What is Virtualization?

* Virtualization is a method of logically dividing mainframes to allow multiple applications to run simultaneously.

* However, this scenario changed when companies and open source communities were able to offer a method of handling privileged instructions. It allows multiple OS to run simultaneously on a single x86 based system.

## 16. Where the docker volumes are stored?

```bash
/var/lib/docker/volumes
```

## 17. What are the command to control Docker with Systemd?

```bash
systemctl start/stop docker
service docker start/stop
```

## 18. How to use JSON instead of YAML compose file?

```bash
docker-compose -f docker-compose.json up
```

## 19. What is the command you need to give to push the new image to Docker registry?

```bash
docker push myorg/img
```

## 20. What is the method for creating a Docker container?

* You can use any of the specific Docker images for creating a Docker container using the below command.

```bash
docker run -t -i command name
```
* This command not only creates the container but also start it for you.

## 21. How can you run multiple containers using a single service?

* By using docker-compose, you can run multiple containers using a single service. All docker-compose files uses yaml language.

## 22. Can you lose data when the container exits?

* No, any data that your application writes to disk get stored in container. The file system for the contain persists even after the container halts.

## 23. What are a different kind of volume mount types available in Docker?

* Bind mounts- It can be stored anywhere on the host system

## 24. What is a DockerFile?
* It is a text file that has all commands which need to be run for building a given image.

## 25. What is the docker command that lists the status of all docker containers?

```bash
docker ps -a
```

## 25. What is docker image registry?
* A Docker image registry, in simple terms, is an area where the docker images are stored. Instead of converting the applications to containers each and every time, a developer can directly use the images stored in the registry.
* This image registry can either be public or private and Docker hub is the most popular and famous public registry available

## 26. How many Docker components are there?
* There are three docker components, they are - Docker Client, Docker Host, and Docker Registry.

1. Docker Client: This component performs “build” and “run” operations for the purpose of opening communication with the docker host.
2. Docker Host: This component has the main docker daemon and hosts containers and their associated images. The daemon establishes a connection with the docker registry.
3. Docker Registry: This component stores the docker images. There can be a public registry or a private one. The most famous public registries are Docker Hub and Docker Cloud.

![image](images/docker_components.png)

## 27. Differentiate between virtualization and containerization.

* The question indirectly translates to explaining the difference between virtual machines and Docker containers.

## 28. Differentiate between COPY and ADD commands that are used in a Dockerfile?

- Both the commands have similar functionality, but COPY is more preferred because of its higher transparency level than that of ADD.
COPY provides just the basic support of copying local files into the container whereas ADD provides additional features like remote URL and tar extraction support.

## 29. Can a container restart by itself?

* Yes, it is possible only while using certain docker-defined policies while using the docker run command. Following are the available policies:

1. Off: In this, the container won’t be restarted in case it's stopped or it fails.
2. On-failure: Here, the container restarts by itself only when it experiences failures not associated with the user.
3. Unless-stopped: Using this policy, ensures that a container can restart only when the command is executed to stop it by the user.
4. Always: Irrespective of the failure or stopping, the container always gets restarted in this type of policy.

* These policies can be used as:
`docker run -dit — restart [restart-policy-value] [container_name]`

## 30. What is the purpose of the volume parameter in a docker run command?

* The syntax of docker run when using the volumes is: `docker run -v host_path:docker_path <container_name>`
* The volume parameter is used for syncing a directory of a container with any of the host directories. Consider the below command as an example: `docker run -v /data/app:usr/src/app myapp`
* The above command mounts the directory  /data/app in the host to the usr/src/app directory. We can sync the container with the data files from the host without having the need to restart it.
* This also ensures data security in cases of container deletion. This ensures that even if the container is deleted, the data of the container exists in the volume mapped host location making it the easiest way to store the container data

## 31. Can you tell the difference between CMD and ENTRYPOINT?
* CMD ile yazilan komutlar degistirilebilirken Entryoint’le yazilanlar sonradan degistirilemez.
* CMD ile Entrypoint beraber kullanilir ki degistirilemeyen komutlar Entrypoint’e degistirilemeyenler CMD’ye degistirilebilenler yazilir.

## 32. How will you ensure that a container 1 runs before container 2 while using docker compose?

* Docker-compose does not wait for any container to be “ready” before going ahead with the next containers. In order to achieve the order of execution, we can use:

* The `depends_on` which got added in version 2 of docker-compose can be used as shown in a sample docker-compose.yml file below:


```bash
version: "2.4"
services:
 backend:
   build: .
   depends_on:
     - db
 db:
   image: postgres
```