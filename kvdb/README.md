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
