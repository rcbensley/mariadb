DELIMITER $$

DROP PROCEDURE IF EXISTS auth.check_user_access$$
CREATE DEFINER=root@localhost PROCEDURE auth.check_user_access()

LANGUAGE SQL
READS SQL DATA
SQL SECURITY DEFINER

BEGIN
DECLARE v_current_user VARCHAR(256);
DECLARE v_allowed TINYINT(1);
DECLARE v_process_id INT;
SET v_allowed = 0;

SELECT SUBSTRING_INDEX(USER(),'@',1) INTO v_current_user;
SELECT allowed FROM auth.users WHERE username=v_current_user INTO v_allowed;
SELECT CONNECTION_ID() INTO v_process_id;

IF v_allowed = 0 THEN
	SELECT "User is not allowed to connect";
	KILL v_process_id;
END IF;

END $$
DELIMITER ;
