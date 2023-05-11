resource "aws_vpc" "kafka-vpc" {
    cidr_block = "10.1.0.0/16"
    enable_dns_support = "true" #gives you an internal domain name
    enable_dns_hostnames = "true" #gives you an internal host name
    #enable_classiclink = "false"  
    instance_tenancy = "default"    
    
    tags = {
        Name = "${var.env}-kafka-vpc"
    }
}

resource "aws_subnet" "kafka-subnet" {
    vpc_id = "${aws_vpc.kafka-vpc.id}"
    cidr_block = "10.1.1.0/28"
    map_public_ip_on_launch = "true" //it makes this a public subnet
    availability_zone = "eu-north-1a"    

    tags = {
        Name = "${var.env}-kafka-subnet"    
    }
}
