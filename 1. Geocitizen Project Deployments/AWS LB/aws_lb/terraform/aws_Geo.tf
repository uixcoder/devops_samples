provider "aws" {
  shared_config_files      = ["/home/ubuntu/aws_lb/.aws/config"]
  shared_credentials_files = ["/home/ubuntu/aws_lb/.aws/credentials"]
  profile = "Personal"
  region = "eu-north-1"	
}
resource "aws_instance" "App_Ubuntu_LB" {
  ami                    = "ami-000e50175c5f86214"
  instance_type          = "t3.micro"
  key_name               = "ATC"
  vpc_security_group_ids = [aws_security_group.sg_app_lb.id]
  credit_specification {
    cpu_credits = "standard"
  }
  tags = {
    Name    = "App_LB"
    Owner   = "Ivan Danyliuk"
    Project = "Geocitizen"
  }
}
resource "aws_instance" "DB_Amazon_Linux_LB" {
  ami                    = "ami-0e3f1570eb0a9bc7f"
  instance_type          = "t3.micro"
  key_name               = "ATC"
  vpc_security_group_ids = [aws_security_group.sg_db_lb.id]
  credit_specification {
    cpu_credits = "standard"
  }
  tags = {
    Name    = "DB_LB"
    Owner   = "**********"
    Project = "Geocitizen"
  }
}

resource "aws_security_group" "sg_app_lb" {
  name = "sg_app_lb"
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
resource "aws_security_group" "sg_db_lb" {
  name = "sg_db_lb"
  ingress {
    from_port   = "5432"
    to_port     = "5432"
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
  #tags = {
  #  Name = "DB_Geo_Terraform"
  #}
}

#IP of aws instances copied to a file hosts file in local system
resource "local_file" "hosts_file" {
  content  = <<EOT
[app_server]
app_host ansible_host=${aws_instance.App_Ubuntu_LB.public_ip}
[db_server]
db_host ansible_host=${aws_instance.DB_Amazon_Linux_LB.public_ip}
EOT  
  filename = "../config/hosts"
}

#IP of aws instances copied to a file hosts file in local system
resource "local_file" "hosts_file_ip" {
  content  = <<EOT
#!/bin/bash

server_ip='${aws_instance.App_Ubuntu_LB.public_ip}'
db_server_ip='${aws_instance.DB_Amazon_Linux_LB.public_ip}'
EOT  
  filename = "../config/hosts_geo"
}


