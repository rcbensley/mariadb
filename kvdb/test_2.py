from datetime import datetime as dt
from datetime import timedelta as td
from time import sleep

import kvdb

db = kvdb.db(history=True)
db.setup()
db.set('red', {'rgb': [254, 0, 0]})
print(db.get('red'))
sleep(5)

print("Now:")
db.set('red', {'rgb': [255, 0, 0]})
print(db.get('red'))

then = dt.now - td(seconds=10)
print("Then:")
print(db.get('red', when=then))
