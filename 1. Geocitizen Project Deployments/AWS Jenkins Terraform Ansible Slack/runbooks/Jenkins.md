### 1. Check java version

```
java -version 
```

### 2. Install java
```
sudo apt-get update
sudo apt-get install openjdk-11-jre
```

### 3. Install Jenkins

https://www.jenkins.io/doc/book/installing/linux/

```
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins
```

### 4. Login to web-interface

Enter user credentials


### 5. Install Locale plugin to enable En language by default.

In Locale settings add "en_US"