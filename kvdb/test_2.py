from datetime import datetime as dt
from datetime import timedelta as td
from time import sleep
from pprint import pprint as pp

import kvdb

db = kvdb.db(history=True)
db.setup()

db.set('red', {'rgb': [254, 0, 0]})
sleep(1)
db.set('blue', {'rgb': [0, 0, 255]})
sleep(1)
db.set('green', {'rgb': [0, 255, 0]})
sleep(1)
pp(db.get())

sleep(5)
db.set('red', {'rgb': [255, 0, 0]})
pp('Updated')
pp(db.get('red'))

oldest_row = db._query(
        "select created from kvdb"
        " where _key='red'")
then = oldest_row[0]['created']

pp('Then:')
pp(db.get(when=then))
