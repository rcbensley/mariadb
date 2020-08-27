# Create new local user, using socket authentication

grant all privileges on *.* to 'vagrant'@'localhost' identified via unix_socket;

# Disks plugin!
select * from information_schema.DISKS;

# S3 Tables
source /vagrant/schema.sql

# /vagrant/load.sh

USE sales;

SHOW CREATE TABLE orders\G

SHOW CREATE TABLE orders_archive\G

INSERT INTO orders_archive SELECT * FROM orders WHERE order_date >= CURRENT_DATE - 1 YEAR;

# Columnstore, basic query performance
# ${HOME}/go/bin/brimming 1000000 1 1000 /var/lib/mysql/mysql.sock

USE brim;

CREATE TABLE `cst` (
  `a` bigint(20) NOT NULL,
  `b` int(11) NOT NULL,
  `c` char(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `d` char(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `e` char(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `f` char(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=columnstore;

