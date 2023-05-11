### Create pipeline item 

#### Add pipeline script

```
node {
    stage('Delete AWS VMs with Terraform') {
        sh script: '''
            chdir /home/ubuntu/Jenkins/terraform
            terraform destroy --auto-approve
        '''    
    }
}
```