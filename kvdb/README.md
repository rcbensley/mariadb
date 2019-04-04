Psst, hey, kid. Got dictionaries?
Wanna store those dictionaries?
Check it out, I got a Key Value Database, or kvdb.

* Store dictionaries.
* Retrieve dictionaries.
* Update dictionaries.
* Delete dictionaries (New for version 2).


### Example

Import and setup.
```
import kvdb

db = kvdb.db()
db.setup()
```

Make and store a dictionary.
```
ice_king_stats = {'name': 'Ice King', 'class': 'Wizard', 'iz_cool': True}
db.set('ice_king', ice_king_stats)
```

Wicked. Now let's read if back!
```
print(db.get('ice_king'))
[{'_key': 'ice_king', '_value': {'name': 'Ice King', 'class': 'Wizard', 'iz_cool': True}}]
>>> fixed_stats = {'iz_cool': False}
```

Something is not quite right. Let's fix that key with the correct values.
```
fixed_stats = {'iz_cool': False}
db.update('ice_king', fixed_stats)

print(db.get('ice_king'))
[{'_key': 'ice_king', '_value': {'name': 'Ice King', 'class': 'Wizard', 'iz_cool': False}}]
```
Fixed!

What if we don't want to do any of that messy updating? Simon says, Wizards Rule!

```
cool_stats = {'Wizards': 'Rule'}
db.set('ice_king', cool_stats)
print(db.get('ice_king'))
[{'_key': 'ice_king', '_value': {'Wizards': 'Rule'}}]
```

### NEW! In v2.

Let's just forget the whole thing.
```
db.delete('ice_king')
```

