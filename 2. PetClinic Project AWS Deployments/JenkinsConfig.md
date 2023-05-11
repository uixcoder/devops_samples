## Install and Configure Jenkins

### 1. Create EC2 Instance

AWS_REGION = eu-north-1 (Stockholm)

12 GB Disk / 2GB RAM / t3.nano (free tier)

Credit specification - Standard

Ubuntu 18.04 LTS

**Problem:** 8GB disk created as in AMI.

**Solution:** Disk space may be increased later on demand by editing EBS Volumes. So i leave 8 GB size.

![j0](img/j0.png)

![j1](img/j1.png)

![j2](img/j2.png)

### 2. Install Docker

SSH to created EC2 instance via public IP

![j4](img/j4.png)


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

#### Set up the repository

1. Update the apt package index and install packages to allow apt to use a repository over HTTPS:

`$ sudo apt-get update`

`$ sudo apt-get remove docker docker-engine docker.io containerd runc`

2. Add Docker’s official GPG key:

`$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`

3. Use the following command to set up the stable repository. To add the nightly or test repository, add the word nightly or test (or both) after the word stable in the commands below. Learn about nightly and test channels.

`$ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`


#### Install Docker Engine

1. Update the apt package index, and install the latest version of Docker Engine and containerd, or go to the next step to install a specific version:

```
$ sudo apt-get update

$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```

2. Verify that Docker Engine is installed correctly by running the hello-world image.


`$ sudo docker run hello-world`


This command downloads a test image and runs it in a container. When the container runs, it prints a message and exits.

Docker Engine is installed and running. The docker group is created but no users are added to it. You need to use sudo to run Docker commands. Continue to Linux postinstall to allow non-privileged users to run Docker commands and for other optional configuration steps.

#### Post-installation steps for Linux

`https://docs.docker.com/engine/install/linux-postinstall/`

`$ sudo groupadd docker`
`$ sudo usermod -aG docker $USER`

logout, login again

Verify that you can run docker commands without sudo.

`$ docker run hello-world`

Configure Docker to start on boot

`$ sudo systemctl enable docker.service`
`$ sudo systemctl enable containerd.service`

### 3. Start Jenkins container from image jenkins/jenkins:lts-jdk11

`$ docker run -d -v jenkins_home:/var/jenkins_home -p 80:8080 --restart=on-failure jenkins/jenkins:lts-jdk11`

![j5](img/j5.png)

### 4. Login to Jenkins

![0_1](img/1_1.png)

To view file login to container

![j6](img/j6.png)
![j7](img/j7.png)

or view attached volume content

![j8](img/j8.png)
![j9](img/j9.png)

Install plugins

![j10](img/j10.png)

![j11](img/j11.png)

![j12](img/j12.png)

Login.

Fresh install of Jenkins is not secure

![j13](img/j13.png)

It requires removing build executors from Jenkins node and add agents with build executors.

### 5. Generate Docker image for AGENTS

Jenkins agent image allows using SSH to establish the connection. It can be used together with the SSH Build Agents plugin or other similar plugins.

[Dockerfile](Dockerfile)

```
FROM jenkins/ssh-agent:jdk11
#Install Terraform
RUN apt-get update
RUN apt-get install -y apt-utils curl unzip
RUN curl -fSSL https://releases.hashicorp.com/terraform/1.2.4/terraform_1.2.4_linux_amd64.zip -o terraform.zip \
    && unzip terraform.zip \
    && mv terraform /usr/local/bin/terraform \
    && rm terraform.zip
#Install ansible
RUN apt-get install -y python3 python3-pip
RUN pip3 install ansible
```
Build image

`$ docker build -t jenkinsagent .`

![j14](img/j14.png)

![j15](img/j15.png)

Run agent container on 23 port

`$ docker run -p 23:22 -d --name agent1 --init --restart=on-failure -v agent1-workdir:/home/jenkins jenkinsagent "<public key>"`

![j16](img/j16.png)

Add new node 

![j17](img/j17.png)

![j18](img/j18.png)

![j19](img/j19.png)

![j20](img/j20.png)

Successfully connected to agent ...

![j21](img/j21.png)

![j22](img/j22.png)

Now remove 2 executors from built-in node

![j23](img/j23.png)

![j24](img/j24.png)

![j25](img/j25.png)

### 6. Add 1G swap area on Docker EC2 Instance

Add swapfile

```
$ sudo dd if=/dev/zero of=/swapfile bs=1M count=1024
$ sudo chmod 0600 /swapfile
$ sudo mkswap /swapfile
$ sudo swapon /swapfile
```
To activate /swapfile1 after Linux system reboot, add entry to /etc/fstab file. Open this file using a text editor such as nano:

`$ sudo nano /etc/fstab`

Append the following line:

`/swapfile none swap sw 0 0`

Result

![j26](img/j26.png)

![j27](img/j27.png)

### 7. Add permanent DNS Name to Jenkins node

All Steps are described [here](UpdateZoneForEC2.md).

![j28](img/j28.png)

#### 8. Close all unneeded ports, leave open only 22 and 80 port.

![30](img/30.png)

### 9. Fix jenkins location on Jenkins settings

![31](img/31.png)
![32](img/32.png)

### 10. Run all containers after reboot

`$ docker update --restart unless-stopped $(docker ps -q)`

### 11. Add JGit and Maven auto istallation

![j35](img/j35.png)

Jenkins are ready for PipeLines!!!

![j36](img/j36.png)

### 12. Create AMI Image of configured Jenkins




