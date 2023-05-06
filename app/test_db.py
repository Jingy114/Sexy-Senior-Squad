import sqlite3

db_name = "test.db"

db = sqlite3.connect(db_name)
c =  db.cursor()

c.execute("CREATE TABLE country (name TEXT PRIMARY KEY)")
c.execute("CREATE TABLE population (country TEXT PRIMARY KEY, population INTEGER)")

c.execute("INSERT INTO country VALUES ('USA')")
c.execute("INSERT INTO country VALUES ('NYC')")
c.execute("INSERT INTO population VALUES ('USA', 1500)")
c.execute("INSERT INTO population VALUES ('NYC', 500)")

db.commit()
db.close()
