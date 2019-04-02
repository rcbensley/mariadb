import kvdb

db = kvdb.db()

db.setup()

db.set('dvd', {'a': 1})

print(db.get('dvd'))

db.update('dvd', {'a': 2})

print(db.get())
