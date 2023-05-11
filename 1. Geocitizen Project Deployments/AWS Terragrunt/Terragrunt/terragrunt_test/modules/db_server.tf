resource "aws_instance" "DB_Amazon_Linux_Terraform" {
  ami                    = "ami-0e3f1570eb0a9bc7f"
  instance_type          = "t3.micro"
  key_name               = "ATC"
  vpc_security_group_ids = [aws_security_group.sgh_db.id]
  credit_specification {
    cpu_credits = "standard"
  }
  tags = {
    Name    = "Db_${var.environment}"
    Owner   = "Ivan Danyliuk"
    Project = "Geocitizen"
  }
}
resource "aws_security_group" "sgh_db" {
  name = "db_${var.environment}"
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
    Name = "DB_Geo_${var.environment}"
  }
}
