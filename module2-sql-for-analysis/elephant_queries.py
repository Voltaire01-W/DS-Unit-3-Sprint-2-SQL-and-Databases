from dotenv import load_dotenv
import psycopg2

### Connect to ElephantSQL-hosted PostgreSQL
conn = psycopg2.connect(dbname='mzrpkrnp', user='mzrpkrnp',
                        password='tcymMvQEzLBiNfTVyGOSMcQXJT-ZvpMN', host='otto.db.elephantsql.com')
### A "cursor", a structure to iterate over db records to perform queries
cur = conn.cursor()
### An example query
cur.execute('SELECT * from test_table;')
### Note - nothing happened yet! We need to actually *fetch* from the cursor
cur.fetchone()
results = cur.fetchall()
for result in results:
    print("RESULT:", type(result))
    print(result)