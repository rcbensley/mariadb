CREATE DATABASE my;
USE my;
CREATE TABLE cnf (section char(16) flag=1,
	VARIABLE_NAME varchar(64) flag=2,
	VARIABLE_VALUE varchar(2048))
	engine=CONNECT table_type=INI file_name='/usr/local/Cellar/mariadb/10.1.9/my.cnf'
	option_list='Layout=Row';