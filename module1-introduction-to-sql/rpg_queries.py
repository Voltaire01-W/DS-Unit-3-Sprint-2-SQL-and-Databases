import os
import sqlite3

# construct a path to wherever your database exists
#DB_FILEPATH = "chinook.db"
# DB_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "rpg_db.sqlite3")
DB_FILEPATH = 'rpg_db.sqlite3'

connection = sqlite3.connect(DB_FILEPATH)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR", cursor)


query1 = "SELECT COUNT() FROM charactercreator_character"
chars = cursor.execute(query1).fetchone()[0]
print(f"There are {chars} total characters.")

print(f"Subclasses:")

query2 = "SELECT COUNT() FROM charactercreator_cleric"
clerics = cursor.execute(query2).fetchone()[0]
print(f"    Cleric: {clerics}")

query3 = "SELECT COUNT() FROM charactercreator_fighter"
fighters = cursor.execute(query3).fetchone()[0]
print(f"    Fighter: {fighters}")

query4 = "SELECT COUNT() FROM charactercreator_thief"
thieves = cursor.execute(query4).fetchone()[0]
print(f"    Thieves: {thieves}")

query5 = "SELECT COUNT() FROM charactercreator_necromancer"
necros = cursor.execute(query5).fetchone()[0]
print(f"    Necromancer: {necros}")

query6 = "SELECT COUNT() FROM charactercreator_mage"
magi = cursor.execute(query6).fetchone()[0] - necros
print(f"    Mage: {magi}")

query7 = "SELECT COUNT() FROM armory_item"
items = cursor.execute(query7).fetchone()[0]
print(f"There are {items} total items.")

query8 = "SELECT COUNT() FROM armory_weapon"
weapons = cursor.execute(query8).fetchone()[0]
print(f"{weapons} items are weapons.")
non_weapons = items - weapons
print(f"{non_weapons} items are non-weapons.")

characters = range(1, 21)
total_items = 0
total_weapons = 0
for character in characters:
    query1 = "SELECT COUNT() " \
             "FROM charactercreator_character_inventory " \
             "WHERE character_id = " + str(character)
    items = cursor.execute(query1).fetchone()[0]
    total_items += items
    print(f"Character {character} has {items} items.")
    query2 = "SELECT character_id " \
             "FROM charactercreator_character_inventory cursor " \
             "WHERE character_id = " + str(character) + " AND " \
             "EXISTS(SELECT item_ptr_id " \
             "FROM armory_weapon " \
             "WHERE item_ptr_id = cursor.item_id)"
    weapons = len(cursor.execute(query2).fetchall())
    total_weapons += weapons
    print(f"Character {character} has {weapons} weapons.")

avg_items = total_items / 20
avg_weapons = total_weapons / 20
print(f"On average, characters 1-20 have {avg_items} items.")
print(f"On average, characters 1-20 have {avg_weapons} weapons.")

connection.close()