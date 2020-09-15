-- vars
SELECT @@hostname, @@port,
    @@local_infile, @@have_symlink,
    @@bind_address, @@secure_file_priv

-- Users
SELECT @@hostname, @@port,concat(user, '@', host) AS "has_no_password"
	FROM mysql.user
	WHERE password='';
SELECT concat(user, '@', host) AS "has_remote_super_priv"
	FROM mysql.user
	WHERE super_priv='Y' and host='%';
SELECT concat(user, '@', host) AS "has_super_priv"
	FROM mysql.user
	WHERE super_priv='Y';



