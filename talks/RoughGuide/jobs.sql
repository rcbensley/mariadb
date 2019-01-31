CREATE DATABASE IF NOT EXISTS jobs;
USE jobs;

DROP TABLE IF EXISTS `dailies`;
CREATE TABLE `dailies` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `job_name` varchar(1024) NOT NULL,
  `source` text NOT NULL,
  `target` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

INSERT INTO `dailies` VALUES (1,'exp_titles','SELECT * FROM employees.titles','/tmp/titles.csv'),
(2,'exp_employees','SELECT * FROM employees.employees','/tmp/employees.csv');
