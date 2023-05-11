### 1. Initial information

**Docker** - minimal version of VM

***Docker Components***

**Docker Engine**    - Docker App
**Docker Container** - running Docker VM
**Docker Image**     - image of Docker Container
**Docker file**      - for creating Docker images

***Docker workflow***

1. Docker Engine
2. Dockerfile
3. Build -> Docker Image
4. Run   -> Docker Container


Install

[https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

[https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)


### Set up the repository
#### 1. Update the apt package index and install packages to allow apt to use a repository over HTTPS:

`$ sudo apt-get remove docker docker-engine docker.io containerd runc`

`$ sudo apt-get update`

#### 2. Add Docker’s official GPG key:

`$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`

#### 3. Use the following command to set up the stable repository. To add the nightly or test repository, add the word nightly or test (or both) after the word stable in the commands below. Learn about nightly and test channels.

`$ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`

### Install Docker Engine

#### 1. Update the apt package index, and install the latest version of Docker Engine and containerd, or go to the next step to install a specific version:

```
$ sudo apt-get update

$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

#### 2. Verify that Docker Engine is installed correctly by running the hello-world image.


`$ sudo docker run hello-world`


This command downloads a test image and runs it in a container. When the container runs, it prints a message and exits.

Docker Engine is installed and running. The docker group is created but no users are added to it. You need to use sudo to run Docker commands. Continue to Linux postinstall to allow non-privileged users to run Docker commands and for other optional configuration steps.

### Post-installation steps for Linux

`https://docs.docker.com/engine/install/linux-postinstall/`

`$ sudo groupadd docker`
`$ sudo usermod -aG docker $USER`

logout, login again

Verify that you can run docker commands without sudo.

`$ docker run hello-world`

Configure Docker to start on boot

`$ sudo systemctl enable docker.service`
`$ sudo systemctl enable containerd.service`

### General Docker Operations
#### View images

`$ docker images`

#### Search images
On Server
`https://hub.docker.com/_/tomcat`

Via console
`$ docker search tomcat`

#### View running containers

`$ docker ps`

#### View all runned containers previously

`$ docker ps`

#### Download image

`$ docker pull tomcat`

`$ docker run -it -p 1234:8080 tomcat`

-it interactively

-p 1234:8080 map port 1234--->8080 port

`$ docker run -d -p 1234:8080 tomcat
-d daemon`

`$ docker run -d --name appgeo -p 1234:8080 tomcat`

#### Stop/start container
`$ docker stop id`

`$ docker stop appgeo`

`$ docker start appgeo`

#### Remove container

`$ docker rm 46179b8c6a23`

#### Remove image

`$ docker rmi b00440a36b99`

#### Docker file

`$ nano Dockerfile`

```
FROM ubuntu:16.04

RUN apt-get -y update
RUN apt-get -y install apache2

RUN echo 'Hello World from Docker!' > /var/www/html/index.html


CMD ["/usr/sbin/apache2ctl", "-D","FOREGROUND"]
EXPOSE 80
```

`$ docker build -t image:v1`

`$ docker run -d -p 1234:80 image:v1`

#### Tags
`$ docker tag image:v1 image:copy`

(Create copy of image)

#### Login to container

`$ docker exec -it h8w8ew8832 /bin/bash`

#### Create image from existing image
`$ docker commit h8w8ew8832 image:v2`

#### Copy files to / from Docker Container

`https://docs.docker.com/engine/reference/commandline/cp/`

The cp command can be used to copy files.

One specific file can be copied TO the container like:

`$ docker cp foo.txt container_id:/foo.txt`

One specific file can be copied FROM the container like:

`$ docker cp container_id:/foo.txt foo.txt`

For emphasis, container_id is a container ID, not an image ID. (Use docker ps to view listing which includes container_ids.)

Multiple files contained by the folder src can be copied into the target folder using:

```
$ docker cp src/. container_id:/target
$ docker cp container_id:/src/. target
```

### Jenkins + Docker

`https://www.cloudytuts.com/tutorials/jenkins/how-to-create-a-docker-pipeline-with-jenkins/`

#### 1. Install Jenkins plugin "SSH Agent"

#### 2. RSA Key Pair

`https://www.ssh.com/academy/ssh/copy-id`

Create a new key-pair using the ssh-key command. When you are prompted for a passphrase press Enter. Do not file in a passphrase, as the remote connection will not prompt for it. This will cause the connection to fail.

`$ ssh-keygen`

filename: jenkins_id_rsa

Two files will be generated by this command: a private key file and a public key file. Copy the public file to the user account on the remote host Jenkins will connect with. For example, if you have a user named jenkins on your remote Docker host, copy the new public to it’s profile with the ssh-copy-id command.

`$ ssh-copy-id -i jenkins_id_rsa ubuntu@docker.host `

Test connection

`$ ssh -i jenkins_id_rsa ubuntu@docker.host`

#### 3. Jenkins Credential

With the RSA public key installed on your remote Docker host(s), you will now need to add your private key as a Jenkins Credential, which allows you to use the key securely within your pipelines.

#### 4. Create pipeline

