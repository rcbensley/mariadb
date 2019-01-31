## Use your MariaDB client config for great good
Chances are, your favourite programming langauge has a database driver which can read parameters from some kind of client config file.

What's the benefit of using a client config? Security and convenience. No hard coded passwords, user credentials can be kept separate from your application core or script in version control.

And let's face it, that list of global constants is growing fast enough as it is.

Something I have seen far too often is a process list full of plain text passwords, and too many unencrypted passwords in version control to count. How embarassing.

I have included a few python examples for MariaDB using PyMYSQL for your enjoyment. You should of course console your driver's API and documentation. I have also included one extra example of connecting to MariaDB using the MariaSQL node.js driver, which in itself is quite interesting as it uses MariaDB's non-blocking client API.

# MariaDB Client Config
Typically located at ```~/.my.cnf``` / ```${HOME}/.my.cnf```. You can also just add sections, such as ```[client]```, to any existing and readable server configs on your system, typically ```/etc/my.cnf```, ```/etc/mysql/my.conf.d/```, etc.

An example of ```~/.my.cnf``` for client usage.

```
[client]
user = IceKing
password = WizardsRule

[mysql]
show-warnings = 1

[biz_dev_vm]
user = henry
password = dubble
host = 127.0.0.1
port = 3306

[biz_uat_db]
user = dba
password = kd93jdmcd93
host = uat.biz_app.domain
port = 3399
```

Don't forget to make this file only readable and writeable by you!
```
chmod 600 ~/.my.cnf
```
You can probably do something similar on Windows which involves right-clicking.