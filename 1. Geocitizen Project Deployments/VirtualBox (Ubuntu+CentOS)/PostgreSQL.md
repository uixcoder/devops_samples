# Install PostgreSQL on CentOS 7.9 Server
## 1. Install CentOS 7.9

[Install source](http://isoredirect.centos.org/centos/7/isos/x86_64/)

## 2. Install Vbox Additions
[Install info](https://www.dev2qa.com/how-to-resolve-virtualbox-guest-additions-kernel-headers-not-found-for-target-kernel-error/)

```
# mount /dev/cdrom /mnt
# yum install "kernel-devel-uname-r == $(uname -r)"
# yum install -y gcc perl kernel-headers kernel-devel
# ./VBoxLinuxAdditions.run
# reboot
```
## 3. Install postgresql
[Install info](https://www.linode.com/docs/guides/how-to-install-postgresql-relational-databases-on-centos-7/)

```
# yum install postgresql-server postgresql-contrib

# postgresql-setup initdb

# systemctl start postgresql

# systemctl enable postgresql

# passwd postgres

# psql
# \password

(or in psql enter "ALTER USER postgres WITH PASSWORD 'newpassword';")

```

## 4. External access to postgresql server
[Install info](https://www.bigbinary.com/blog/configure-postgresql-to-allow-remote-connection)

Show config files location

```
$ psql
postgres=# show hba_file;
postgres=# show config_file;
```
### Configuring `postgresql.conf`

Or simlply find file

`$ find / -name "postgresql.conf"`

Open `postgresql.conf` file and replace line

`listen_addresses = 'localhost'`

with

`listen_addresses = '*'`

### Configuring `pg_hba.conf`

Let's try to connect to remote postgresql server using "psql".

`$ psql -h 10.1.1.110 -U postgres`

In order to fix it, open `pg_hba.conf` and add following entry at the very end.

```
host    all      all      0.0.0.0/0        md5
host    all      all      ::/0             md5
```
Do not get confused by **md5** option mentioned above. All it means is that a password needs to be provided (***do not forget to add it to database with command `'\password'` in `psql` session***). If you want client to allow collection without providing any password then change **md5** to **trust** and that will allow connection unconditionally.

Restart postgresql server

`# systemctl enable postgresql`

```
netstat -nlt
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:5432            0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN
tcp6       0      0 :::22                   :::*                    LISTEN
tcp6       0      0 :::5432                 :::*                    LISTEN
tcp6       0      0 ::1:25                  :::*                    LISTEN
```

Here we can see that `Local Address` for port `5432` has changed to `0.0.0.0`.

## 5. Test connection from Host

`$ psql -h 10.1.1.110 -U postgres`



