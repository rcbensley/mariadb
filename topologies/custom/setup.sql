DROP DATABASE IF EXISTS auth;
CREATE DATABASE IF NOT EXISTS auth;
USE auth;

SET PASSWORD FOR root@localhost=password('dev');

GRANT SELECT ON *.* to 'testuser'@'localhost' IDENTIFIED BY 'trouble';

CREATE TABLE users (username varchar(64) primary key not null, 
	allowed tinyint(1) not null default 0);

INSERT INTO auth.users VALUES ('root', 1), ('vagrant', 1), ('testuser', 0), ('jam', 1);

# UPDATE auth.users SET allowed=0 WHERE username='testuser';
# UPDATE auth.users SET allowed=1 WHERE username='testuser';

DROP DATABASE IF EXISTS dba;
CREATE DATABASE IF NOT EXISTS dba;
USE dba;

CREATE TABLE cnf (section char(16) flag=1,
	VARIABLE_NAME varchar(64) flag=2,
	VARIABLE_VALUE varchar(2048))
	engine=CONNECT table_type=INI file_name='/mnt/db/my.cnf'
	option_list='Layout=Row';

