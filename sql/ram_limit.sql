-- RAM in bytes
SET @RAM=134818111488;


-- Skipping these MyISAM/Aria/MERGE buffers: 
-- - read_buffer_size
-- - read_rnd_buffer_size

-- All global buffers:
-- Including Key_buffer size as system tables are Aria/MyISAM.
SET @BUFFERS=(
	SELECT @@key_buffer_size
	+ @@innodb_buffer_pool_size
	+ @@innodb_log_buffer_size
	+ @@query_cache_size);

-- Per-thread buffers:
SET @THREADS=(
		SELECT @@sort_buffer_size
		+ @@join_buffer_size
		+ @@innodb_sort_buffer_size
		+ @@thread_stack);

SELECT
	@BUFFERS + (@THREADS * @@max_connections) AS REQUIRED_RAM,
	(@RAM - @BUFFERS) / @THREADS AS MAX_CONNECTIONS;
