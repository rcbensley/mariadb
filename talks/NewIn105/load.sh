#/usr/bin/env bash

for i in {1..10000}
do
	sudo mariadb -NBe "INSERT INTO sales.orders (order_date) VALUES (curdate() - INTERVAL ${i} DAY);"
done