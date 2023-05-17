import csv
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('my_database.db')
cur = conn.cursor()

# Read CSV file
with open('data.csv', 'r') as f:
    dr = csv.DictReader(f)  # comma is default delimiter
    headers = dr.fieldnames  # get the headers

    # Create table based on CSV file
    cur.execute(f"DROP TABLE IF EXISTS my_table")
    cur.execute(f"CREATE TABLE my_table ({', '.join(headers)})")

    # Insert CSV data into the table
    for row in dr:
        cur.execute(f"INSERT INTO my_table VALUES ({', '.join('?' * len(headers))})", list(row.values()))

# Commit changes and close connection
conn.commit()
conn.close()
