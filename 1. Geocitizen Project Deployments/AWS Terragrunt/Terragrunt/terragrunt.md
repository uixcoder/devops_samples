## Install terraform

[Install](https://learn.hashicorp.com/tutorials/terraform/install-cli) from [downloads](https://www.terraform.io/downloads).

`$ wget https://releases.hashicorp.com/terraform/1.1.8/terraform_1.1.8_linux_amd64.zip`

`$ unzip terraform_1.1.8_linux_amd64.zip`

`$ mv terraform /usr/local/bin/terraform`

## Install terragrunt

Go to the [Releases Page](https://github.com/gruntwork-io/terragrunt/releases).

Downloading the binary for your operating system:

`$ wget https://github.com/gruntwork-io/terragrunt/releases/download/v0.36.7/terragrunt_linux_amd64`

Rename the downloaded file to terragrunt.

`$ mv terragrunt_linux_amd64 terragrunt`

Add execute permissions to the binary.

`$ chmod u+x terragrunt`

Put the binary somewhere on your PATH.

`$ mv terragrunt /usr/local/bin/terragrunt`
