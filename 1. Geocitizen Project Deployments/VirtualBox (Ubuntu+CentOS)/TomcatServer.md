# Install TomCat Server on Ubuntu 16.04 Server
## 1. Install Ubuntu Server 16
[Install source](https://releases.ubuntu.com/16.04/)

Install sequrity updates during install ...

Install Open SSH Server ...

PS. On Ubuntu Server root login is not allowed by default. Login as user and change root password if needed.

## 2. Login to installed server via SSH

`$ ssh user@ip-address`

## 3. Install ORACLE JAVA SDK 8

tar.gz can be dowloaded from [oracle](https://gist.github.com/wavezhang/ba8425f24a968ec9b2a8619d7c2d86a6) without registering

[Download link ](https://javadl.oracle.com/webapps/download/GetFile/1.8.0_321-b07/df5ad55fdd604472a86a45a217032c7d/linux-i586/jdk-8u321-linux-x64.tar.gz) for jdk-8u321-linux-x64.tar.gz

Manual on java install for Ubuntu is available [here](https://serveradmin.ru/ustanovka-oracle-java-na-ubuntu-i-centos/).

*List of commands:*

`$ su root`

`# cd ~`

`# curl -fSSL https://javadl.oracle.com/webapps/download/GetFile/1.8.0_321-b07/df5ad55fdd604472a86a45a217032c7d/linux-i586/jdk-8u321-linux-x64.tar.gz -o jdk-8u321-linux-x64.tar.gz`

`# mkdir /usr/lib/jvm`

`# tar -zxf jdk-8u321-linux-x64.tar.gz -C /usr/lib/jvm`

`update-alternatives --install "/usr/bin/java" "java" "/usr/lib/jvm/jdk1.8.0_321/bin/java" 1500`

`update-alternatives --install "/usr/bin/javaws" "javaws" "/usr/lib/jvm/jdk1.8.0_321/bin/javaws" 1500`

Add to file `/etc/environment` `JAVA_HOME` variable

`JAVA_HOME="/usr/lib/jvm/jdk1.8.0_321"`

Save file and apply changes.

`# source /etc/environment`

Check JAVA version and JAVA_HOME variable

`# java -version`

`# echo $JAVA_HOME`

## 4. Install Tomcat

[Manual](https://www.digitalocean.com/community/tutorials/how-to-install-apache-tomcat-8-on-ubuntu-16-04)

Upgrade certificates first

`# apt update`

`# apt upgrade`

`# dpkg-reconfigure ca-certificates`

Then create a new `tomcat` group

`# groupadd tomcat`

Next, create a new `tomcat` user. We’ll make this user a member of the `tomcat` group, with a home directory of `/opt/tomcat` (where we will install Tomcat), and with a shell of `/bin/false` (so nobody can log into the account):

`# useradd -s /bin/false -g tomcat -d /opt/tomcat tomcat`

Download and install Tomcat 9 from official repository

`# curl -O https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.58/bin/apache-tomcat-9.0.58.tar.gz`

We will install Tomcat to the `/opt/tomcat` directory. Create the directory, then extract the archive to it with these commands:

`# mkdir /opt/tomcat`
`# tar xzvf apache-tomcat-9*tar.gz -C /opt/tomcat --strip-components=1`

Next, we can set up the proper user permissions for our installation.

## 5. Update Permissions

The `tomcat` user that we set up needs to have access to the Tomcat installation. We’ll set that up now.

Change to the directory where we unpacked the Tomcat installation:

`# cd /opt/tomcat`

Give the `tomcat` group ownership over the entire installation directory:

`# chgrp -R tomcat /opt/tomcat`

Next, give the `tomcat` group read access to the `conf` directory and all of its contents, and execute access to the directory itself:

`# chmod -R g+r conf`

`# chmod g+x conf`

Make the `tomcat` user the owner of the `webapps`, `work`, `temp`, and `logs` directories:

`# chown -R tomcat webapps/ work/ temp/ logs/`

Now that the proper permissions are set up, we can create a `systemd` service file to manage the Tomcat process.

## 6. Create a `systemd` Service File

We want to be able to run Tomcat as a service, so we will set up `systemd` service file.

Tomcat needs to know where Java is installed. This path is commonly referred to as `JAVA_HOME`. The easiest way to look up that location is by running this command:

`# update-java-alternatives -l`

OR

`# echo $JAVA_HOME`

With this piece of information, we can create the `systemd` service file. Open a file called `tomcat.service` in the `/etc/systemd/system` directory by typing:

`# nano /etc/systemd/system/tomcat.service`

Paste the following contents into your service file. Modify the value of `JAVA_HOME` if necessary to match the value you found on your system (**add `/jre` to the value of variable!!!**). You may also want to modify the memory allocation settings that are specified in `CATALINA_OPTS`:
`/etc/systemd/system/tomcat.service`

```
[Unit]
Description=Apache Tomcat Web Application Container
After=network.target

[Service]
Type=forking

Environment=JAVA_HOME=/usr/lib/jvm/jdk1.8.0_321/jre
Environment=CATALINA_PID=/opt/tomcat/temp/tomcat.pid
Environment=CATALINA_HOME=/opt/tomcat
Environment=CATALINA_BASE=/opt/tomcat
Environment='CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC'
Environment='JAVA_OPTS=-Djava.awt.headless=true -Djava.security.egd=file:/dev/./urandom'

ExecStart=/opt/tomcat/bin/startup.sh
ExecStop=/opt/tomcat/bin/shutdown.sh

User=tomcat
Group=tomcat
UMask=0007
RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target
```

When you are finished, save and close the file.

Next, reload the systemd daemon so that it knows about our service file:

`# systemctl daemon-reload`

Start the Tomcat service by typing:

`# systemctl start tomcat`

Double check that it started without errors by typing:

`# systemctl status tomcat`

## 7. Adjust the Firewall and Test the Tomcat Server

Now when the Tomcat service is started, we can test to make sure the default page is available.

Before we do that, we need to adjust the firewall to allow our requests to get to the service. If you followed the prerequisites, you will have a `ufw` firewall enabled currently.

Tomcat uses port 8080 to accept conventional requests. Allow traffic to that port by typing:

`# ufw allow 8080`

With the firewall modified, you can access the default splash page by going to your domain or IP address followed by `:8080` in a web browser:

Open in web browser

`http://server_domain_or_IP:8080`

You will see the default Tomcat splash page, in addition to other information. However, if you click the links for the Manager App, for instance, you will be denied access. We can configure that access next.

If you were able to successfully accessed Tomcat, now is a good time to enable the service file so that Tomcat automatically starts at boot:

`# systemctl enable tomcat`

## 8. Configure Tomcat Web Management Interface

In order to use the manager web app that comes with Tomcat, we must add a login to our Tomcat server. We will do this by editing the `tomcat-users.xml` file:

`# nano /opt/tomcat/conf/tomcat-users.xml`

You will want to add a user who can access the `manager-gui` and `admin-gui` (web apps that come with Tomcat). You can do so by defining a user, similar to the example below, between the `tomcat-users` tags. Be sure to change the username and password to something secure:

```
<tomcat-users . . .>
    <user username="admin" password="password" roles="manager-gui,admin-gui"/>
</tomcat-users>
```

Save and close the file when you are finished.

By default, newer versions of Tomcat restrict access to the Manager and Host Manager apps to connections coming from the server itself. Since we are installing on a remote machine, you will probably want to remove or alter this restriction. To change the IP address restrictions on these, open the appropriate `context.xml` files.

For the Manager app, type:

`# nano /opt/tomcat/webapps/manager/META-INF/context.xml`

For the Host Manager app, type:

`# nano /opt/tomcat/webapps/host-manager/META-INF/context.xml`

Inside, comment out the IP address restriction to allow connections from anywhere. Alternatively, if you would like to allow access only to connections coming from your own IP address, you can add your public IP address to the list:

```
<Context antiResourceLocking="false" privileged="true" >
  <!--<Valve className="org.apache.catalina.valves.RemoteAddrValve"
         allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" />-->
</Context>
```

Save and close the files when you are finished.

To put our changes into effect, restart the Tomcat service:

`# systemctl restart tomcat`

## 9. Access the Web Interface

Now that we have create a user, we can access the web management interface again in a web browser. Once again, you can get to the correct interface by entering your server’s domain name or IP address followed on port `8080` in your browser:

`http://server_domain_or_IP:8080`

Tomcat installation is functional, but entirely unencrypted. This means that all data, including sensitive items like passwords, are sent in plain text that can be intercepted and read by other parties on the internet. In order to prevent this from happening, it is strongly recommended that you encrypt your connections with SSL. You can find out how to encrypt your connections to Tomcat by following this [guide](https://www.digitalocean.com/community/tutorials/how-to-encrypt-tomcat-8-connections-with-apache-or-nginx-on-ubuntu-16-04).

## 10. Install Maven

`$ sudo apt install maven`

`$ mvn --version`




