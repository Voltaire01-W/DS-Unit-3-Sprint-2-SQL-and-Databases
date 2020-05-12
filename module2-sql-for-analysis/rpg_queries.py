import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import json
import numpy as np

load_dotenv()


DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PW")
DB_HOST= os.getenv("DB_HOST")


conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
curs = conn.cursor()
#- How many total Characters are there?
curs.execute("SELECT count(distinct character_id)  FROM charactercreator_character;")
result1 = curs.fetchone()
print("There are", result1[0], "clerics.")

#- How many of each specific subclass?
curs.execute('SELECT count(*) FROM charactercreator_cleric')
result2 = curs.fetchone()
print("There are", result2[0], "clerics.")

curs.execute('SELECT count(*) FROM charactercreator_fighter')
result2 = curs.fetchone()
print("There are", result2[0], "fighters.")

curs.execute('SELECT count(*) FROM charactercreator_mage')
result2 = curs.fetchone()
print("There are", result2[0], "mages.")

curs.execute('SELECT count(*) FROM charactercreator_necromancer')
result2 = curs.fetchone()
print("There are", result2[0], "necromancers.")

curs.execute('SELECT count(*) FROM charactercreator_thief')
result2 = curs.fetchone()
print("There are", result2[0], "thieves.")

#- How many total Items?
curs.execute('SELECT count(distinct item_id) FROM armory_item')
items = curs.fetchone()
print("There are", items[0], "total items.")

#- How many of the Items are weapons? How many are not?
curs.execute('SELECT count(distinct item_ptr_id) FROM armory_weapon')
weapons = curs.fetchone()
print("There are", weapons[0], "items that are weapons.")

nonweapons = items[0] - weapons[0]
print("There are", nonweapons, "items that are not weapons.")
#- How many Items does each character have? (Return first 20 rows)
query1 = '''SELECT 
  charactercreator_character_inventory.character_id
  ,count(distinct charactercreator_character_inventory.item_id) as itemcount
  ,count(distinct armory_weapon.item_ptr_id) as weaponcount
FROM charactercreator_character_inventory
LEFT JOIN armory_item ON charactercreator_character_inventory.item_id = armory_item.item_id
LEFT JOIN armory_weapon ON charactercreator_character_inventory.item_id = armory_weapon.item_ptr_id
GROUP BY charactercreator_character_inventory.character_id 
ORDER BY charactercreator_character_inventory.character_id DESC
LIMIT 20'''
curs.execute(query1)
table1 = curs.fetchall()

for row in table1:
    if row[1] > 1:
        print ("Character", row[0], "has", row[1], "items.")
    else:
        print ("Character", row[0], "has", row[1], "item.")
    
#- How many Weapons does each character have? (Return first 20 rows)
for row in table1:
    if row[2] > 1:
        print ("Character", row[0], "has", row[2], "weapons.")
    else:
        print ("Character", row[0], "has", row[2], "weapon.")
#- On average, how many Items does each Character have?
query = '''SELECT 
  AVG(itemcount)
  ,avg(weaponcount)
FROM (
	SELECT 
  		charactercreator_character_inventory.character_id
 		,count(distinct charactercreator_character_inventory.item_id) as itemcount
  		,count(distinct armory_weapon.item_ptr_id) as weaponcount
		FROM charactercreator_character_inventory
		LEFT JOIN armory_item ON charactercreator_character_inventory.item_id = armory_item.item_id
		LEFT JOIN armory_weapon ON charactercreator_character_inventory.item_id = armory_weapon.item_ptr_id
		GROUP BY charactercreator_character_inventory.character_id 
		ORDER BY charactercreator_character_inventory.character_id DESC
) subq'''
curs.execute(query)
table = curs.fetchone()
print("On avereage each character has", table[0], "items.")
#- On average, how many Weapons does each character have?
print("On avereage each character has", table[1], "weapons.")
conn.commit()
curs.close()
conn.close()