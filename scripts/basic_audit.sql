-- General
SELECT @@hostname,@@port,@@version,@@version_comment,
    @@log_bin, @@binlog_format, @@log_slave_updates, @@expire_logs_days,
    @@innodb_flush_log_at_trx_commit, @@sync_binlog, @@sql_mode,
    @@log_error, @@log_warnings, @@slow_query_log\G

-- User Databases, engines and sizes.
SELECT t.*,
    SUM(t.engine_count) AS engine_count
FROM
(SELECT table_schema,
 engine,
    COUNT(engine) AS engine_count,
    ROUND(((DATA_LENGTH + INDEX_LENGTH)/1024/1024), 2) as DB_SIZE_MB,
    ROUND(DATA_FREE/1024/1024) as DATA_FREE_MB
    FROM information_schema.tables
        GROUP BY table_schema, engine) t
GROUP BY t.table_schema, t.engine
ORDER BY t.DB_SIZE_MB DESC;

