#IP of aws instances copied to a file hosts file in local system
resource "local_file" "hosts_file" {
  content = <<EOT
[app_server]
app_host ansible_host=${aws_instance.App_Ubuntu_Terraform.public_ip}
[db_server]
db_host ansible_host=${aws_instance.DB_Amazon_Linux_Terraform.public_ip}
EOT  
  filename = "${var.root_path}/hosts"
}

#IP of aws instances copied to a file hosts file in local system
resource "local_file" "hosts_file_ip" {
  content  = <<EOT
#!/bin/bash

server_ip='${aws_instance.App_Ubuntu_Terraform.public_ip}'
db_server_ip='${aws_instance.DB_Amazon_Linux_Terraform.public_ip}'
EOT  
  filename = "${var.root_path}/hosts_bash"
}
