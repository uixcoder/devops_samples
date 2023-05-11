## Task

![task](img/task.png)

### Infrastructure -- [Terraform files](Terraform)

VPC + Subnet

![tf5](img/tf5.png)

Terraform test run for 3 nodes on AWS t3.micro (free tier).

![tf1](img/tf1.png)

Number of nodes may be changed in [vars.tf](Terraform/vars.tf) file

![tf2](img/tf2.png)

Terraform outputs with ip-addresses moves to file [Ansible/hosts](Ansible/hosts) to provide correct Ansible run for created AWS nodes with ansible names 0 - N.

![tf3](img/tf3.png)

### Configuration -- [Ansible files](Ansible)

**Configuration for all nodes:**

1. Add 1G swap space to AWS Nodes
2. Install Java
3. Create kafka group/user
4. Create Zookeper data directory "/zookeeper"
5. Create Kafka log directory "/kafka"
6. Add zookeeper myid file to "/zookeeper" directory
7. Update kafka broker.id line / Update kafka zookeeper.connect line
8. Create a Service file for ZooKeeper / Kafka
9. Start ZooKeeper / Kafka services.
10. Validating ZooKeeper / Kafka.

![ans1](img/ans1.png)

.......

![ans2](img/ans2.png)

### Test Install

All brokers in one cluster:

![t3](img/t3.png)

![t2](img/t2.png)

![t1](img/t1.png)

Create topic + read/write:

![tc1](img/tc1.png)

![tc2](img/tc2.png)

![tc3](img/tc3.png)
