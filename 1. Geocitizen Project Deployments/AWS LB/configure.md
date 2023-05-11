## 1. Create, run and configure instances on AWS as for single server configuration
 -- with application (Ubuntu)
 -- with database
## 2. Configure ddclient service with no-ip DDNS for database server
 In my case i configured database server ddns name dbgeo.ddns.net
## 3. Create AWS Load balancer

![1](img/1.png)

![2](img/2.png)

![3](img/3.png)

![4](img/4.png)

![5](img/5.png)

![6](img/6.png)

![7](img/7.png)

![8](img/8.png)

![9](img/9.png)

![10](img/10.png)

![11](img/11.png)

![12](img/12.png)

Add DNS name of created Load balancer to deploy script as address of app server and DDNS name of daatabase server

![13](img/13.png)

Deploy Application to App Server

![14](img/14.png)

Partial test of application an database

![15](img/15.png)

Create Image of Instance

![32](img/32.png)

Create Launch Template from Instance

![16](img/16.png)

![17](img/17.png)

![18](img/18.png)

![19](img/19.png)

![21](img/21.png)

![22](img/22.png)

![23](img/23.png)

Create Auto Scaling Group

![24](img/24.png)

![25](img/25.png)

![26](img/26.png)

![27](img/27.png)

![28](img/28.png)

![29](img/29.png)

![30](img/30.png)

And now we see new instance creating

![31](img/31.png)

Stop original instance (source for template)

And now we can connect to instance via load balances DNS.

![33](img/33.png)





