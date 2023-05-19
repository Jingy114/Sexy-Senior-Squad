import csv
import sqlite3
import pandas as pd

# remember to pip install pandas openpyxl


def xlsx_to_csv(xlsx_file, csv_file):
    # Read the Excel file
    df = pd.read_excel(xlsx_file)

    # Write the DataFrame to a CSV file
    df.to_csv(csv_file, index=False)

# Usage
xlsx_file = 'input.xlsx'  # your xlsx file
csv_file = 'output.csv'  # the output csv file
xlsx_to_csv(xlsx_file, csv_file)

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def create_table_from_csv(self, csv_file, table_name):
        with open(csv_file, 'r') as f:
            dr = csv.DictReader(f)
            headers = dr.fieldnames
            self.cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.cur.execute(f"CREATE TABLE {table_name} ({', '.join(headers)})")
            for row in dr:
                self.cur.execute(f"INSERT INTO {table_name} VALUES ({', '.join('?' * len(headers))})", list(row.values()))
        self.conn.commit()

    def select_data(self, table_name, column_name, condition):
        self.cur.execute(f"SELECT {column_name} FROM {table_name} WHERE {condition}")
        return self.cur.fetchall()

    def update_data(self, table_name, column_name, new_value, condition):
        self.cur.execute(f"UPDATE {table_name} SET {column_name} = {new_value} WHERE {condition}")
        self.conn.commit()

    def close(self):
        self.conn.close()



if __name__ == "__main__":
    db_manager = DatabaseManager('my_database.db')
    db_manager.create_table_from_csv('population_by_country_2020.csv', 'my_table')

    # Example Usage
    # Get all rows from 'my_table' where 'country' is 'USA'
    data = db_manager.select_data('my_table', 'Population', "Country = 'China'")
    print(data)

    # Update 'column_name' in 'my_table' to 'new_value' where 'country' is 'USA'
    #db_manager.update_data('my_table', 'column_name', 'new_value', "country = 'USA'")

    db_manager.close()
