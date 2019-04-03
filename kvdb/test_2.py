import kvdb

db = kvdb.db()
db.setup()
db.set('red', {'rgb': [254, 0, 0]})
print(db.get('red'))
db.set('red', {'rgb': [255, 0, 0]})
print(db.get('red'))

