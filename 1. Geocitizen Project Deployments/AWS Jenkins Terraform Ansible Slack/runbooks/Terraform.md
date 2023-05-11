### 1. Install Terraform

Terraform AWS Docs
https://learn.hashicorp.com/collections/terraform/aws-get-started

Download
https://www.terraform.io/downloads

```
cd ~
mkdir terraform
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform
```

### 2. Create / copy *.tf to terraform folder

### 3. Create AWS user with AdministratorAccess. Remember security credentials (access_key, secret_key)

### 4. Add AWS credentials

```
$ aws cli install
```
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install
```

```
$ aws configure
```

add credentials to *.tf

1) Bad idea
```
provider "aws" {  
    access_key = "********************"
    secret_key = "****************************************"
    region = "eu-north-1"
}
```

2) move to file ~/.aws/credentials with command

```
$ aws configure
```

file credentials consists of 

```
[Personal]
aws_access_key_id = ********************
aws_secret_access_key = ****************************************
```

.tf file 

```
provider "aws" {
    profile = "Personal"
    region = "eu-north-1"
}
```

3)[!!!SAFEST!!!] move credentials to environment variables

```
export AWS_ACCESS_KEY_ID=********************
export AWS_SECRET_ACCESS_KEY=****************************************
export AWS_DEFAULT_REGION=eu-north-1
```

CREDENTIALS IN SESSION!!!

For futher automation 2 variant was selected.

### 5. Test run configuration
terraform plan

### 6. Run configuration
terraform apply

### 7. Destroy all previously created
terraform destroy
