import csv
import sqlite3
import pandas as pd

# remember to pip install pandas openpyxl

def xlsx_to_csv(xlsx_file, csv_file):
    # Read the Excel file
    df = pd.read_excel(xlsx_file)

    # Write the DataFrame to a CSV file
    df.to_csv(csv_file, index=False)


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

    def select_all_data(self, table_name, column_name):
        self.cur.execute(f"SELECT {column_name} FROM {table_name}")
        return self.cur.fetchall()

    def update_data(self, table_name, column_name, new_value, condition):
        self.cur.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE {condition}", (new_value,))
        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":

    # xlsx_file = 'sample.xlsx'  # your xlsx file
    csv_file = 'sample.csv'  # the output csv file
    # xlsx_to_csv(xlsx_file, csv_file)

    db_manager = DatabaseManager('my_database.db')
    db_manager.create_table_from_csv('sample.csv', 'my_table')

    # Test cases
    # Get population of China
    data = db_manager.select_data('my_table', 'Population', "Country = 'China'")
    print('Population of China:', data)

    # Get all data for USA
    data = db_manager.select_data('my_table', '*', "Country = 'USA'")
    print('Data for USA:', data)

    # Update population density of Indonesia
    db_manager.update_data('my_table', 'Population_Density_PerSqKm', '150', "Country = 'Indonesia'")

    # Check if the update has been successful
    data = db_manager.select_data('my_table', 'Population_Density_PerSqKm', "Country = 'Indonesia'")
    print('Updated Population Density for Indonesia:', data)

    db_manager.close()
