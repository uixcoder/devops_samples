### 1. Install Ansible

https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-ubuntu

```
$ sudo apt update
$ sudo apt ugrade
$ sudo apt install software-properties-common
$ sudo add-apt-repository --yes --update ppa:ansible/ansible
$ sudo apt install ansible
```

Get Ansible info
```
$ ansible --version
```
### 2. Create Inventory file

Example for local VMs

```
hosts.txt (inventory file)
-----------------------
[main_servers]
test1 ansible_host=10.1.1.109 ansible_user=ubuntu ansible_ssh_private_key_file=/home/test/.ssh/key_VB
[secondary_servers]
test2 ansible_host=10.1.1.105 ansible_user=ubuntu ansible_ssh_private_key_file=/home/test/.ssh/key_VB
test3 ansible_host=10.1.1.110 ansible_user=ubuntu ansible_ssh_private_key_file=/home/test/.ssh/key_VB
```

### 3. Ping hosts

```
ansible -i hosts.txt all -m ping
```

### 4. Create config file to store main config details

```
ansible.cfg
-----------------------
[defaults]
host_key_checking = false
inventory         = ./hosts.txt
-----------------------
```

After defining config file in ansible directory ping all hosts looks much more simpler

```
$ ansible all -m ping
```

### 5. Define ansible playbook

```
#playbook1.yml
#-----------------------
---
- name: Test
  hosts: all
  become: true
  become_user: ubuntu

  tasks:
  - name: ping all servers
    ping:
```

Playbook run

```
$ ansible-playbook playbook1.yml
```

### 6. Move variables from inventory file to group_vars folder files

```
ansible.cfg
[defaults]
host_key_checking = False
inventory         = ../config/hosts

config/hosts
[app_server]
app_host ansible_host=16.170.157.178
[db_server]
db_host ansible_host=13.51.108.55

group_vars/app_server
---
ansible_user                 : ubuntu
ansible_ssh_private_key_file : /home/ubuntu/config/ATC.pem

group_vars/db_server
---
ansible_user                 : ec2-user
ansible_ssh_private_key_file : /home/ubuntu/config/ATC.pem
```

