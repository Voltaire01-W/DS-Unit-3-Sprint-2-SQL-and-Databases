import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import json
import numpy as np

psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
load_dotenv()
csv = os.path.join(os.path.dirname(__file__), "..", "module2-sql-for-analysis", "titanic.csv")
df = pd.read_csv(csv)
df.index += 1
x = list(df.to_records(index=True))

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PW")
DB_HOST= os.getenv("DB_HOST")

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
curs = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS passengers (
    id SERIAL PRIMARY KEY,
    survived integer,
    pclass integer,
    name varchar NOT NULL,
    sex varchar NOT NULL,
    age float,
    sib_spouse_count integer,
    parent_child_count integer,
    fare float
);
"""
curs.execute(query)

tuples = x
insert_query = "INSERT INTO passengers (id, survived, pclass, name, sex, age, sib_spouse_count, parent_child_count, fare) VALUES %s"
execute_values(curs, insert_query, tuples)
conn.commit()
curs.close()
conn.close()