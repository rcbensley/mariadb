Key Value Database
------------------

To better understand what these NoSQL kids are on about, let's take a look at a Key Value Database...
In this case, keys are unique strings, and values are Python Dictionaries.

Write a key and value to a database. The key is a colour, red, and the value is the 8bit integer value.

```
import kvdb

db = kvdb.db()
db.set('red', {'rgb': [255, 0, 0]})
```

Get the value back
```
print(db.get('red'))
```

But then, once both tests have been run, and a quick query on a certain local database...
```
mariadb dba@127.0.0.1:test> select * from kvdb;
+----+-------------------------------------+--------------------------------------------------------------------------------------+
| id | _key                                | _value                                                                               |
+----+-------------------------------------+--------------------------------------------------------------------------------------+
| 1  | Do Androids Dream of Electric Sheep | {"format": "Paperback", "pages": "210", "author": "Phillip K. Dick"}                 |
| 2  | Blade Runner                        | {"format": "DVD", "running_time": "117 minutes", "Director": "Ridley Scott"}         |
| 3  | Blade Runner 2049                   | {"format": "Blu-Ray", "running_time": "163 minutes", "Director": "Denis Villeneuve"} |
| 5  | red                                 | {"rgb": [255, 0, 0]}                                                                 |
+----+-------------------------------------+--------------------------------------------------------------------------------------+
4 rows in set
Time: 0.014s
```
