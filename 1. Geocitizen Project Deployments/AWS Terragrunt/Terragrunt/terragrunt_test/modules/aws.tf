provider "aws" {
  profile = "Personal"
  region  = "eu-north-1"
}
terraform {
  backend "s3" {}
}
