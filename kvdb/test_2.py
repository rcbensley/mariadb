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

pp('All:')
pp(db.get_versions('red'))

pp('Then:')
pp(db.get_first_version('red'))
