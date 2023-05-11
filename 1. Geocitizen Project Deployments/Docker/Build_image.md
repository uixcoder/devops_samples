### 1. Create Application image 
We can also create image with app inside. 

Create sipmle Dockerfile 

![d1](img/d1.png)

and run

`$ docker build -t geocitizen:v1 .`

![d2](img/d2.png)

Created image:

![d2a](img/d2a.png)

### 2. Create Docker Containers

Database container

`$ docker run -d --name Db_GeoCitizen -e POSTGRES_DB=Geo -e POSTGRES_USER=Geo -e POSTGRES_PASSWORD=GeoCitizenDocker postgres`

Application container

`$ docker run -d --name App_Geo -p 8080:8080 geocitizen:v1`


![d2b](img/d2b.png)

### 3. Check application

![d3](img/d3.png)
