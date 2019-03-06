#!/usr/bin/env sh

SQL_USER="SELECT CONCAT('\'', user, '\'@\'', host, '\'') FROM mysql.user GROUP BY user,host"

for u in $(mysql -NBe "${SQL_USER}")
do
	echo "--Grants for ${u} on ${HOSTNAME}:"
	mysql -NBe "SHOW GRANTS FOR ${u}" | sed -e "s/$/;/g"
	echo ""
done
