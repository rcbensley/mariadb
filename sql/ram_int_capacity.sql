-- RAM in bytes
SET @RAM=134818111488;

SET @BUFFERS=(SELECT @@key_buffer_size + @@innodb_buffer_pool_size + @@innodb_log_buffer_size + @@query_cache_size);
SET @THREADS=(SELECT @@sort_buffer_size + @@join_buffer_size + @@innodb_sort_buffer_size + @@thread_stack);

SELECT
	@BUFFERS + (@THREADS * @@max_connections) AS REQUIRED_RAM,
	(@RAM - @BUFFERS) / @THREADS AS MAX_CONNECTIONS;


-- Galera Node Count
SET @GCN=3;
-- How many inserts remain for tables with INT as PRIMARY and/or UNIQUE indexes?
SELECT
c.table_schema,
c.table_name,
c.data_type,
t.AUTO_INCREMENT,
CASE
WHEN c.is_signed = 1 THEN IF(t.AUTO_INCREMENT < 0,
						     ABS((2147483648 + t.AUTO_INCREMENT)/@GCN),
						     ABS((2147483647 - t.AUTO_INCREMENT)/@GCN))
ELSE ABS((4294967295 - t.AUTO_INCREMENT)/@GCN)
END AS INT_REMAINDER
FROM
(select table_schema,table_name,column_name,data_type,column_type,column_key,
	CASE
	WHEN COLUMN_TYPE LIKE '%unsigned%' THEN 0
	ELSE 1
	END AS 'is_signed'
	from information_schema.columns
	where COLUMN_KEY IN ('PRI','UNI') and DATA_TYPE ='int'
	and table_schema not in ('mysql','performance_schema','information_schema')) c
JOIN information_schema.tables t ON t.table_name = c.table_name
	and c.table_schema = c.table_schema
WHERE t.AUTO_INCREMENT IS NOT NULL
ORDER BY 5 ASC;
