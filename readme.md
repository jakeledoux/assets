# Assets

A simple Python module for easy handling, parsing, and updating of CSV-like data.

Example usage:
```python3
from assets import Asset 

weapons = Asset('weapons.csv', update=True)
for weapon in weapons:
    print(f'{weapon.name}: ({weapon.damage} dmg, {weapon.value} gold)')
```

Example `weapons.csv`:
```csv
#version=1
#url=https://pastebin.com/raw/DAGHFB7E
#type=Weapon
@name:str, damage:int, value:int
Wood Sword, 1, 2
Stone Sword, 5, 10
Iron Sword, 10, 50
Gold Sword, 10, 200
Diamond Sword, 30, 500
```
'\#' denotes a header variable. You can use as many as you like, but there are
a few built-in ones with special utility:

* version
    * Denotes version of file, which is compared when updating.
* url 
    * URL of file to update from.
* type 
    * Name to be used for the `namedtuple` that contains each row.

Syntax also requires one line starting with '@', which defines the column names
and types. The amount of columns must be constant. Valid types:

* `int`
* `float`
* `str`
* `bool`
