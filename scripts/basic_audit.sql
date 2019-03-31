-- General
SELECT @@hostname,@@port,@@version,@@version_comment,
    @@log_bin, @@binlog_format, @@log_slave_updates, @@expire_logs_days,
    @@innodb_flush_log_at_trx_commit, @@sync_binlog, @@sql_mode,
    @@log_error, @@log_warnings, @@slow_query_log;

-- User Databases, engines and sizes.
SELECT table_schema, engine, 
    ROUND(((DATA_LENGTH + INDEX_LENGTH)/1024/1024), 2) as DB_SIZE_MB,
    ROUND(DATA_FREE/1024/1024) as DATA_FREE_MB
    GROUP BY table_schema, engine
    ORDER BY 3,1,2 DESC;

