### Create pipeline item 

#### Add pipeline script

```
node {
    withEnv(["TERRAFORM_FOLDER=/home/ubuntu/Jenkins/terraform",
    "ANSIBLE_FOLDER=/home/ubuntu/Jenkins/ansible"]){

    stage('Terraform Init') {
        slackSend color: "good", message: "Terraform init ..."
        sh script: '''
            chdir ${TERRAFORM_FOLDER}
            terraform init
        '''    
    }
    stage('Create AWS VMs with Terraform') {
        slackSend color: "good", message: "Terraform apply ..."
        sh script: '''
            chdir ${TERRAFORM_FOLDER}
            terraform apply --auto-approve
        '''    
    }
    
    stage('Configure App VM with Ansible') {
        slackSend color: "good", message: "Configure App VM with Ansible ..."
        sh script: '''
            chdir ${ANSIBLE_FOLDER}
            ansible-playbook playbook1.yml
        '''    
    }
    
    stage('Configure Db VM with Ansible') {
        slackSend color: "good", message: "Configure Db VM with Ansible ..."
        sh script: '''
            chdir ${ANSIBLE_FOLDER}
            ansible-playbook playbook2.yml
        '''    
    }
    
    stage('Deploy Geo Application with Ansible') {
        slackSend color: "good", message: "Deploy Geo Application with Ansible ..."
        sh script: '''
            chdir ${ANSIBLE_FOLDER}
            ansible-playbook playbook3.yml
        '''    
    }
    }
}

```


