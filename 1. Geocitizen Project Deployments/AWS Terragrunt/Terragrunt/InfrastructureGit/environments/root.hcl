locals {
  root_deployments_dir       = get_parent_terragrunt_dir()
  relative_deployment_path   = path_relative_to_include()
  deployment_path_components = compact(split("/", local.relative_deployment_path))
  env = reverse(local.deployment_path_components)[0]
}

terraform {
  source = "git@github.com:idanylyuk/terragrunt_test.git//modules?ref=v0.0.2"
}

remote_state {
  backend = "s3"
  config = {
    bucket         = "igeocitizen-terraform-state"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "eu-north-1"
    encrypt        = true
    dynamodb_table = "igeocitizen-lock-table-${path_relative_to_include()}"
  }
}
inputs = {
  environment = local.env
  root_path   = "${get_parent_terragrunt_dir()}/../ansible/environments/${path_relative_to_include()}"
}