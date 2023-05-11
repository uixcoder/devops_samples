# Geocitizen project

### 1. Requirements to Host PC
`Host PC with Oracle VM VirtualBox and SSH client installed.`

### 2. Create 2 VitrualBox VMs:
**VM1 (Apache Tomcat Server)** (1-2 Gb RAM): 

***Ubuntu 16.04 Server*** [Configuration details](TomcatServer.md)

    - Open SSH Server
    - Oracle Java SDK 8
    - Apache Tomcat/9.0.58
    - Apache Maven 3.3.9

**VM2 (PostgreSQL Database Server)** (1 Gb RAM): 

***CentOS 7.9.2009*** [Configuration details](PostgreSQL.md)

    - Open SSH Server
    - PostgreSQL 9.2.24
### 3. Application fixing / deployment

#### - Released on GitHub application have some [bugs](AppBugs.md). They are fixed automatically by deploy application script (see below).

#### - Get IP adresses of Apache Tomcat Server and PostgreSQL Database Server. You may use commands

`$ ifconfig -a`

or

`$ ip a`

#### - Download [deploy application script](deploy) to Host.

#### - You have to add your data to script - correct variables with your server adresses, database and gmail credantials.

          server_ip='10.1.1.112'
          db_server_ip='10.1.1.110'
          db_name='db_name'
          db_user='db_user'
          db_password='db_password'
          gmail_user='gmail_user'
          gmail_password='gmail_user_password'

#### - Upload modified file `deploy` to Apache Tomcat Server on VM1.
            
Login to Apache Tomcat Server via SSH. Create new file in user home directory
            
`$ nano deploy`
       
Copy text from modified script to SSH console with opened file `deploy` (`Ctrl+Shift+V` shortcut or right key of mouse -> insert). Save file and exit.

Give execute rights to file

`$ chmod u+x deploy`

and run it

`$ ./deploy`
        
Enter sudo user password (if needed). Wait Tomcat server to deploy application.

        
### 4. Run application on Host web browser

Enter in browser adress line

`http://server_ip:8080/citizen`

where `server_ip` is ip-adress of Apache Tomcat Server and start using application.

