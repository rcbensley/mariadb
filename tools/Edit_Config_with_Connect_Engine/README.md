It is not uncommon for the MariaDB server config to be writeable or even owned by the same user in which the mysqld is running (```--user``` or ```user``` in ```/etc/my.cnf```).
Realising this, combined with a lack of being able to [alter system settings](https://mariadb.com/kb/en/library/server-system-variables/#setting-server-system-variables) while a server is running (which would only take affect after a daemon restart) and the awesome [INI Table type](https://mariadb.com/kb/en/mariadb/connect-ini-table-type/) support in the MariaDB CONNECT engine, we can do some absolutely terrifying things right from your favourite SQL client. Like update system settings! Anyone working in DevOps or security should click [this](https://www.youtube.com/results?search_query=kittens+playing) now, and never come back here.


## Setup
Every CONNECT engine table, is a table. We are going to create a table, who's tablespace is the server's config file.
Let's create a new database schema:

```
MariaDB [(none)]> CREATE DATABASE the_horror;
Query OK, 1 row affected (0.01 sec)
MariaDB [(none)]> USE the_horror;
Database changed
```

Now let's create a CONNECT table with a table_type of INI, and point it at the file we want to...alter:
```

MariaDB [my]> CREATE TABLE cnf (section char(16) flag=1,
    -> VARIABLE_NAME varchar(64) flag=2,
    -> VARIABLE_VALUE varchar(2048))
    -> engine=CONNECT table_type=INI file_name='/etc/my.cnf'
    -> option_list='Layout=Row';
Query OK, 0 rows affected (0.02 sec)

MariaDB [my]> show tables;
+--------------+
| Tables_in_my |
+--------------+
| cnf          |
+--------------+
1 row in set (0.00 sec)

MariaDB [my]> select * from my.cnf;
+---------+--------------------------------+----------------------------------------------------------------+
| section | VARIABLE_NAME                  | VARIABLE_VALUE                                                 |
+---------+--------------------------------+----------------------------------------------------------------+
| mysqld  | server-id                      | 1                                                              |
| mysqld  | character-set-server           | utf8                                                           |
| mysqld  | collation-server               | utf8_general_ci                                                |
| mysqld  | default-time-zone              | +00:00                                                         |
| mysqld  | local_infile                   | 1                                                              |
| mysqld  | max_allowed_packet             | 100M                                                           |
| mysqld  | sql_mode                       | STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
| mysqld  | innodb_file_format             | Barracuda                                                      |
| mysqld  | innodb_file_per_table          | 1                                                              |
| mysqld  | innodb_flush_log_at_trx_commit | 1                                                              |
| mysqld  | innodb_flush_method            | O_DIRECT                                                       |
| mysqld  | binlog_format                  | ROW                                                            |
| mysqld  | log-bin                        | db                                                             |
| mysqld  | sync_binlog                    | 1                                                              |
| mysqld  | performance_schema             | 1                                                              |
| mysqld  | userstat                       | 1                                                              |
| mysqld  | log_output                     | TABLE                                                          |
+---------+--------------------------------+----------------------------------------------------------------+
17 rows in set (0.00 sec)
```

A rather modest config.
```
~ $ cat /etc/my.cnf
[mysqld]
server-id=1
character-set-server=utf8
collation-server=utf8_general_ci
default-time-zone='+00:00'
local_infile = 1
max_allowed_packet = 100M
sql_mode = STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
innodb_file_format = Barracuda
innodb_file_per_table = 1
innodb_flush_log_at_trx_commit = 1
innodb_flush_method = O_DIRECT
binlog_format = ROW
log-bin = db
sync_binlog = 1
performance_schema = 1
userstat = 1
log_output = TABLE
```

## Update a value
Now using the new table, let's update some system variables!
```
MariaDB [my]> select @@sql_mode;
+----------------------------------------------------------------+
| @@sql_mode                                                     |
+----------------------------------------------------------------+
| STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+----------------------------------------------------------------+
1 row in set (0.00 sec)

MariaDB [my]> select * from my.cnf where VARIABLE_NAME='sql_mode';
+---------+---------------+----------------------------------------------------------------+
| section | VARIABLE_NAME | VARIABLE_VALUE                                                 |
+---------+---------------+----------------------------------------------------------------+
| mysqld  | sql_mode      | STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
+---------+---------------+----------------------------------------------------------------+
1 row in set (0.01 sec)

MariaDB [my]> update my.cnf set VARIABLE_VALUE='NO_ENGINE_SUBSTITUTION' where VARIABLE_NAME='sql_mode';
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

MariaDB [my]> select * from my.cnf where VARIABLE_NAME='sql_mode';
+---------+---------------+------------------------+
| section | VARIABLE_NAME | VARIABLE_VALUE         |
+---------+---------------+------------------------+
| mysqld  | sql_mode      | NO_ENGINE_SUBSTITUTION |
+---------+---------------+------------------------+
1 row in set (0.01 sec)
```

Did it work?
```
~ $ grep sql_mode /etc/my.cnf
sql_mode=NO_ENGINE_SUBSTITUTION
```
YES IT DID! Beautiful, and scary. Scariful.


Value is updated! Restart the server ...
```
~ $ mysql.server stop
Shutting down MySQL
.. SUCCESS!
~ $ mysql.server start
Starting MySQL
. SUCCESS!

~ $ mysql my -NBe "select @@sql_mode;"
NO_ENGINE_SUBSTITUTION
~ $ mysql my -NBe "select * from my.cnf where VARIABLE_NAME='sql_mode';"
mysqld	sql_mode	NO_ENGINE_SUBSTITUTION

```

Show your friends, and maybe your CTO after a few drinks.
