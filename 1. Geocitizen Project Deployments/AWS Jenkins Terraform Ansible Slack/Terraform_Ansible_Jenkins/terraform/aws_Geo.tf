provider "aws" {
  shared_config_files      = ["/home/ubuntu/Jenkins/.aws/config"]
  shared_credentials_files = ["/home/ubuntu/Jenkins/.aws/credentials"]
  profile = "Personal"
  region = "eu-north-1"	
}
resource "aws_instance" "App_Ubuntu_Terraform" {
  ami                    = "ami-000e50175c5f86214"
  instance_type          = "t3.micro"
  key_name               = "ATC"
  vpc_security_group_ids = [aws_security_group.sg_app.id]
  credit_specification {
    cpu_credits = "standard"
  }
  tags = {
    Name    = "App_Ubuntu_Terraform"
    Owner   = "***********"
    Project = "Geocitizen"
  }
}
resource "aws_instance" "DB_Amazon_Linux_Terraform" {
  ami                    = "ami-0e3f1570eb0a9bc7f"
  instance_type          = "t3.micro"
  key_name               = "ATC"
  vpc_security_group_ids = [aws_security_group.sg_db.id]
  credit_specification {
    cpu_credits = "standard"
  }
  tags = {
    Name    = "App_Amazon_Linux_Terraform"
    Owner   = "***********"
    Project = "Geocitizen"
  }
}

resource "aws_security_group" "sg_app" {
  name = "sg_app"
  ingress {
    from_port   = "8080"
    to_port     = "8080"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = "22"
    to_port     = "22"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  tags = {
    Name = "App_Geo_Terraform"
  }
}
resource "aws_security_group" "sg_db" {
  name = "sg_db"
  ingress {
    from_port   = "5432"
    to_port     = "5432"
    protocol    = "tcp"
    cidr_blocks = ["${aws_instance.App_Ubuntu_Terraform.public_ip}/32"]
  }
  ingress {
    from_port   = "22"
    to_port     = "22"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  tags = {
    Name = "DB_Geo_Terraform"
  }
}

#IP of aws instances copied to a file hosts file in local system
resource "local_file" "hosts_file" {
  content  = <<EOT
[app_server]
app_host ansible_host=${aws_instance.App_Ubuntu_Terraform.public_ip}
[db_server]
db_host ansible_host=${aws_instance.DB_Amazon_Linux_Terraform.public_ip}
EOT  
  filename = "../config/hosts"
}

#IP of aws instances copied to a file hosts file in local system
resource "local_file" "hosts_file_ip" {
  content  = <<EOT
#!/bin/bash

server_ip='${aws_instance.App_Ubuntu_Terraform.public_ip}'
db_server_ip='${aws_instance.DB_Amazon_Linux_Terraform.public_ip}'
EOT  
  filename = "../config/hosts_geo"
}


