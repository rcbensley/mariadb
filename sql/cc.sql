-- General
SELECT @@hostname,@@port,@@version,@@version_comment;
SELECT @@log_bin, @@binlog_format, @@log_slave_updates, @@expire_logs_days;
SELECT @@innodb_flush_log_at_trx_commit, @@sync_binlog, @@sql_mode;
SELECT @@log_error, @@log_warnings, @@slow_query_log;
SHOW VARIABLES LIKE '%audit%';

-- Replication
SHOW MASTER STATUS;
SHOW SLAVE STATUS\G
SHOW GLOBAL STATUS LIKE 'wsrep_%';

-- Users
SELECT @@hostname, @@port,concat(user, '@', host) AS "has_no_password"
	FROM mysql.user
	WHERE password='';
SELECT concat(user, '@', host) AS "has_remote_super_priv"
	FROM mysql.user
	WHERE super_priv='Y' and host='%';


-- User Tables and their ENIGNES
SELECT @@hostname, @@port, count(*) AS 'count', engine
FROM information_schema.tables
	WHERE table_schema NOT IN ('mysql', 'performance_schema', 'information_schema')
	AND table_type != 'view'
GROUP BY engine;

-- Non-InnoDB tables
SELECT @@hostname, @@port, TABLE_SCHEMA,TABLE_NAME, engine, SUM(DATA_LENGTH + INDEX_LENGTH) AS size, 'is_not_innodb'
FROM information_schema.tables
	WHERE table_schema NOT IN ('mysql', 'performance_schema', 'information_schema')
	AND table_type != 'view'
	AND engine !='InnoDB'
	GROUP BY table_name;


-- Tables without indexes
SELECT @@hostname, @@port, TABLE_SCHEMA,TABLE_NAME, ENGINE, SUM(DATA_LENGTH + INDEX_LENGTH) AS size, 'has_no_index'
FROM INFORMATION_SCHEMA.tables
	WHERE table_schema NOT IN ('mysql', 'performance_schema', 'information_schema')
	AND table_type != 'view'
	  AND TABLE_NAME NOT IN
		(SELECT TABLE_NAME
		 FROM
		   (SELECT TABLE_NAME,
				   index_name
			FROM information_schema.statistics
			WHERE table_schema NOT IN ('mysql', 'performance_schema', 'information_schema')
			GROUP BY TABLE_NAME,
					 index_name) tab_ind_cols
		 GROUP BY TABLE_NAME)
		GROUP BY table_schema, table_name;

-- Top 5 Fragmented Tables
SELECT * FROM
	(SELECT
		t.TABLE_SCHEMA,
		t.TABLE_NAME,
		ROUND(((t.DATA_LENGTH + t.INDEX_LENGTH)/1024/1024), 2) as TABLE_SIZE_MB,
		ROUND(t.DATA_FREE/1024/1024) as DATA_FREE_MB
FROM information_schema.tables t
JOIN (SELECT
		TABLE_SCHEMA,
		TABLE_NAME,
		DATA_FREE,
		(DATA_FREE/(DATA_LENGTH+INDEX_LENGTH)) AS FRAGMENTATION
		FROM information_schema.tables) f ON t.TABLE_SCHEMA = f.TABLE_SCHEMA and t.TABLE_NAME = f.TABLE_NAME
			WHERE t.DATA_FREE > 0
			AND f.DATA_FREE > 0) AS f
ORDER BY f.DATA_FREE_MB DESC
LIMIT 10;

