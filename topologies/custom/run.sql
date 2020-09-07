# Edit my.cnf
# Outward table, https://mariadb.com/kb/en/inward-and-outward-tables/
# INI table type, https://mariadb.com/kb/en/connect-ini-table-type/
SHOW CREATE TABLE dba.cnf\G

UPDATE dba.cnf SET variable_value='TABLE' WHERE variable_name='log_output' AND section='mysqld';


# OUTFILE/INFILE
# https://mariadb.com/kb/en/select-into-outfile/
# https://mariadb.com/kb/en/load-data-infile/

USE jam;
DROP TABLE IF EIXSTS jam.new_table;
CREATE TABLE jam.new_table LIKE jam.t_jam_orders;

SELECT * FROM t_jam_orders INTO OUTFILE '/tmp/jam_orders.tsv';

LOAD DATA INFILE '/tmp/jam_orders.tsv' INTO TABLE jam.new_table;

DROP TABLE IF EXISTS jam.new_table;


# Binlog restore

# RESET AND DELETE
mariadb -A jam
select sum(qty) from jam.t_jam_orders;
delete from t_jam_customers; delete from t_jam_orders; delete from t_jam_products;
flush master;
select sum(qty) from jam.t_jam_orders;

#LOAD
python3 pop.py

mariadb -A jam
select sum(qty) from jam.t_jam_orders;

flush logs;

delete from t_jam_customers; delete from t_jam_orders; delete from t_jam_products;

select sum(qty) from jam.t_jam_orders;

cd /mnt/db/data/

mariadb-binlog binlog.000001 --database=jam | mariadb jam

mariadb -A jam
select sum(qty) from jam.t_jam_orders;


# User Access Control with init_connect
# init_file, https://mariadb.com/kb/en/server-system-variables/#init_file
# init_slave, https://mariadb.com/kb/en/replication-and-binary-log-system-variables/#init_slave
# https://mariadb.com/kb/en/server-system-variables/#init_connect

USE auth;
SHOW CREATE PROCEDURE auth.check_user_access\G

UPDATE auth.users SET allowed=1 WHERE username='testuser';

UPDATE auth.users SET allowed=0 WHERE username='testuser';

