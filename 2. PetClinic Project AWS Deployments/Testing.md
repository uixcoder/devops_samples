# Testing under load

## Test Docker/Jenkins configuration under load 

### 1 executor on agent1 + 2GB swap area

![ai0](img/ai0.png)

Pipelines uses not so much memory --> swap area decreased to 1GB.

Time for deployment 1

![testb1_1](img/testb1_1.png)

Time for deployment 2

![testb2_2](img/testb2_2.png)

![testb2_1](img/testb2_1.png)

is very dependant on time for creating database in AWS RDS. Sometimes it's too long.

### 2 executors on agent1 + 1GB swap area

Memory consumption is not so big

![test1](img/test1.png)

but when using **maven** for testing or building .war it increases

![test6](img/test6.png)

![test8](img/test8.png)

The total run time of 2 pipelines is not much bigger than 1 alone.

![test9](img/test9.png)

![test10](img/test10.png)

**SUMMARY:** Selected AWS configuration is enough for test deployment and is even good as for free tier aws services.