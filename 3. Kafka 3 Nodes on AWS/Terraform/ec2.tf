resource "aws_instance" "kafka-node" {
  count                  = var.nodes_count
  ami                    = "${var.system_ami}"
  instance_type          = "t3.micro"
  key_name               = "ATC"
  subnet_id = "${aws_subnet.kafka-subnet.id}"
  vpc_security_group_ids = [aws_security_group.kafka-sg.id]
  credit_specification {
    cpu_credits = "standard"
  }
  tags = {
    Name    = "${var.env}-Kafka-NODE-${count.index}"
    Owner   = "idanylyuk"
    Project = "Kafka"
  }

}  

output "node-ip" {
    value = aws_instance.kafka-node.*.public_ip
}
