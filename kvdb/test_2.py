import kvdb

db = kvdb.db()
db.set('red', {'rgb': [255, 0, 0]})

print(db.get('red'))

