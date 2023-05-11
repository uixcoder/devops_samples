https://dker.ru/docs/docker-engine/admin-guide/using-supervisor-with-docker/
https://docs.docker.com/samples/postgresql_service/
------------------------------------------------------------------------------


scp configure deploy supervisord.conf ubuntu@10.1.1.60
ssh ubuntu@10.1.1.60

docker run -it --name Geo -p 1022:22 -p 8080:8080 -p 9001:9001  ubuntu:18.04
exit

docker cp configure Geo:configure
docker cp supervisord.conf Geo:supervisord.conf
docker cp deploy Geo:deploy

docker start Geo
docker exec -it Geo /bin/bash

chmod a+x configure
chmod a+x deploy

./configure
./deploy
cp supervisord.conf /etc/supervisor/conf.d/supervisord.conf
rm supervisord.conf
supervisord


-----------------------------------------------------------------
test  on web

supervisor
http://10.1.1.60:9001

tomcat
http://10.1.1.60:8080

citizen
http://10.1.1.60:8080/citizen




