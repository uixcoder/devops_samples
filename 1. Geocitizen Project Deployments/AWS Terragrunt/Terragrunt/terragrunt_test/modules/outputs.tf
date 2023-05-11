output "Active_Environment" {
  value = var.environment
}

output "AWS_App_Server" {
  value       = aws_instance.App_Ubuntu_Terraform.public_ip
  description = "The public IP address of the web server"
}

output "AWS_Db_Server" {
  value = aws_instance.DB_Amazon_Linux_Terraform.public_ip
}
