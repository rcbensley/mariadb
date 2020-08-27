DROP DATABASE IF EXISTS sales;
CREATE DATABASE IF NOT EXISTS sales;
USE sales;

CREATE TABLE IF NOT EXISTS sales.orders(
order_id BIGINT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
order_date DATETIME NOT NULL,
INDEX idx_order_date (order_date)) ENGINE=InnoDB;

CREATE TABLE sales.orders_archive LIKE sales.orders;
ALTER TABLE orders_archive ENGINE=S3;


CREATE TABLE orders_archive (
  order_id int,
  order_date datetime
) ENGINE=S3;