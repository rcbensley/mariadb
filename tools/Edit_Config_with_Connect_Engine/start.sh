#!/usr/bin/env bash

# mysqld must be in PATH.
MYCLIENT=$(which mysql)
MYSQLD=$(which mysqld)

DATADIR=$PWD/data
MYCNF=$DATADIR/my.cnf
BASEDIR=$(dirname $(which mysqld))
TMPDIR=/tmp
PORT=3310

MYCLIENT="mysql --socket=$DATADIR/mysql.sock"

if [[ -d $DATADIR ]]
then
	if [[ -e $DATADIR/mysql.sock ]]
	then
		$MYCLIENT -ANBe "shutdown;" 
	elif 
	fi
    rm -Rf $DATADIR
fi

mkdir $DATADIR

echo -e "[mysqld]
user = $USER
basedir	= $BASEDIR
tmpdir = $TMPDIR
port = $PORT
datadir = $DATADIR
socket = $DATADIR/mysql.sock
pid_file = $DATADIR/mysql.pid
log_error = $DATADIR/error.log
log_output = TABLE
innodb_buffer_pool_size = 8M
key_buffer_size = 8M
[mariadb]
plugin-load-add = ha_connect.so" > $MYCNF

# Run server with config
$MYSQLD --defaults-file=$MYCNF 2>&1 &
if [[ -e $DATADIR/mysql.pid ]]
then
	echo "mysqld pid:"
	cat $DATADIR/mysql.pid
fi

# Create database and table
DBNAME='my'
TABLENAME='cnf'
CREATE_TABLE_SQL="CREATE TABLE ${DBNAME}.${TABLENAME}
(section char(16) flag=1,
VARIABLE_NAME varchar(64) flag=2,
VARIABLE_VALUE varchar(2048))
engine=CONNECT table_type=INI file_name='${MYCNF}'
option_list='Layout=Row'"
$MYCLIENT -ANBe "create database if not exists ${DBNAME};"
$MYCLIENT $DBNAME -ANBe "DROP TABLE IF EXISTS ${DBNAME}.${TABLENAME};"
$MYCLIENT $DBNAME -ANBe "${CREATE_TABLE_SQL};"