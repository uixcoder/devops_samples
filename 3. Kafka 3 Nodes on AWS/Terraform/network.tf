resource "aws_internet_gateway" "kafka-igw" {
  vpc_id = aws_vpc.kafka-vpc.id

  tags = {
    Name = "${var.env}-kafka-igw"
  }
}

resource "aws_route_table" "kafka-public-crt" {
  vpc_id = aws_vpc.kafka-vpc.id

  route {
    cidr_block = "0.0.0.0/0" //CRT uses this IGW to reach internet
    gateway_id = aws_internet_gateway.kafka-igw.id
  }

  tags = {
    Name = "${var.env}-public-crt"
  }
}

resource "aws_route_table_association" "crta-public-subnet" {
  subnet_id      = aws_subnet.kafka-subnet.id
  route_table_id = aws_route_table.kafka-public-crt.id
}

resource "aws_security_group" "kafka-sg" {
  vpc_id = aws_vpc.kafka-vpc.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 2181
    to_port     = 2181
    protocol    = "tcp"
    cidr_blocks = ["10.1.1.0/28"]
  }

  ingress {
    from_port   = 2888
    to_port     = 2888
    protocol    = "tcp"
    cidr_blocks = ["10.1.1.0/28"]
  }

  ingress {
    from_port   = 3888
    to_port     = 3888
    protocol    = "tcp"
    cidr_blocks = ["10.1.1.0/28"]
  }

  ingress {
    from_port   = 9092
    to_port     = 9092
    protocol    = "tcp"
    cidr_blocks = ["10.1.1.0/28"]
  }

  tags = {
    Name = "${var.env}-kafka-sg"
  }
}
