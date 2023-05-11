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


