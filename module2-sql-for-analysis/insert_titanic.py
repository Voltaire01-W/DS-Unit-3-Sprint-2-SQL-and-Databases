import os
from dotenv import load_dotenv
import psycopg2
import sqlite3
import pandas as pd

df = pd.read_csv('titanic.csv')
df['Name'] = df['Name'].str.replace("'", "", regex=True)
df.head()

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PW")
DB_HOST= os.getenv("DB_HOST")

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
curs = conn.cursor()
curs.execute('DROP TABLE titanic_table')
conn.commit()

curs.execute('''CREATE TABLE titanic_table (
                   id SERIAL PRIMARY KEY,
                   survived INT,
                   pclass INT,
                   name VARCHAR(100),
                   sex VARCHAR(10),
                   age FLOAT,
                   sibs_spouse INT,
                   par_child INT,
                   fare FLOAT);
                ''')
conn.commit()
 
sl_conn = sqlite3.connect('titantic_temp.sqlite3')
sl_curs = sl_conn.cursor()

df.to_sql('titanic_temp', sl_conn)

passengers = sl_curs.execute('SELECT * FROM titanic_temp;').fetchall()

for passenger in passengers:
    curs.execute("INSERT INTO titanic_table VALUES" + str(passenger) + ";")

conn.commit()