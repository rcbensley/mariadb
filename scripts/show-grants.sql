DELIMITER $$

DROP PROCEDURE IF EXISTS show_grants$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `show_grants`()

LANGUAGE SQL
SQL SECURITY DEFINER
COMMENT 'Show grants for all users.'

BEGIN
DECLARE v_user_host CHAR(141);
DECLARE done INT DEFAULT FALSE;
DECLARE users CURSOR FOR select concat("'",user,"'@'",host,"'") from mysql.user;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
OPEN users;
users_loop: LOOP
	FETCH users INTO v_user_host;
	IF done THEN
		LEAVE users_loop;
	END IF;
	SET @q = CONCAT("SHOW GRANTS FOR ", v_user_host);
	PREPARE grant_q FROM @q;
	EXECUTE grant_q;
END LOOP;
CLOSE users;
END $$
DELIMITER ;
