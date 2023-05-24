import csv
import sqlite3
#import pandas as pd

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
            # replace special characters or spaces in header names with underscore
            headers = ["".join([c if c.isalnum() else '_' for c in header]) for header in headers]
            # append an underscore to headers that are SQLite keywords
            sqlite_keywords = ['ABORT', 'ACTION', 'ADD', 'AFTER', 'ALL', 'ALTER', 'ANALYZE', 'AND', 'AS', 'ASC',
                            'ATTACH', 'AUTOINCREMENT', 'BEFORE', 'BEGIN', 'BETWEEN', 'BY', 'CASCADE', 'CASE', 'CAST',
                            'CHECK', 'COLLATE', 'COLUMN', 'COMMIT', 'CONFLICT', 'CONSTRAINT', 'CREATE', 'CROSS',
                            'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'DATABASE', 'DEFAULT', 'DEFERRABLE',
                            'DEFERRED', 'DELETE', 'DESC', 'DETACH', 'DISTINCT', 'DROP', 'EACH', 'ELSE', 'END', 'ESCAPE',
                            'EXCEPT', 'EXCLUSIVE', 'EXISTS', 'EXPLAIN', 'FAIL', 'FOR', 'FOREIGN', 'FROM', 'FULL',
                            'GLOB', 'GROUP', 'HAVING', 'IF', 'IGNORE', 'IMMEDIATE', 'IN', 'INDEX', 'INDEXED',
                            'INITIALLY', 'INNER', 'INSERT', 'INSTEAD', 'INTERSECT', 'INTO', 'IS', 'ISNULL', 'JOIN',
                            'KEY', 'LEFT', 'LIKE', 'LIMIT', 'MATCH', 'NATURAL', 'NO', 'NOT', 'NOTNULL', 'NULL', 'OF',
                            'OFFSET', 'ON', 'OR', 'ORDER', 'OUTER', 'PLAN', 'PRAGMA', 'PRIMARY', 'QUERY', 'RAISE',
                            'RECURSIVE', 'REFERENCES', 'REGEXP', 'REINDEX', 'RELEASE', 'RENAME', 'REPLACE',
                            'RESTRICT', 'RIGHT', 'ROLLBACK', 'ROW', 'SAVEPOINT', 'SELECT', 'SET', 'TABLE', 'TEMP',
                            'TEMPORARY', 'THEN', 'TO', 'TRANSACTION', 'TRIGGER', 'UNION', 'UNIQUE', 'UPDATE', 'USING',
                            'VACUUM', 'VALUES', 'VIEW', 'VIRTUAL', 'WHEN', 'WHERE', 'WITH', 'WITHOUT']
            headers = [header if header.upper() not in sqlite_keywords else header + "_" for header in headers]
            
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
    
    def remove_column(self, table_name, column_name):
        self.cur.execute(f"PRAGMA table_info({table_name})")
        columns_info = self.cur.fetchall()
        columns = [column[1] for column in columns_info if column[1] != column_name]

        if len(columns) != len(columns_info):
            self.cur.execute(f"CREATE TABLE temp_table AS SELECT {', '.join(columns)} FROM {table_name}")
            self.cur.execute(f"DROP TABLE {table_name}")
            self.cur.execute(f"ALTER TABLE temp_table RENAME TO {table_name}")
            self.conn.commit()
        else:
            print("Column not found in the table")


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
    
    # Remove columns from the table, tested working
    
    #db_manager.remove_column('my_table', 'Population_Density_PerSqKm')
    
    data = db_manager.select_data('my_table', 'Population', "Country = 'Indonesia'")
    print('Updated Population Density for Indonesia:', data)
    
    db_manager.create_table_from_csv('population_by_country_2020.csv', 'population')
    print(db_manager.select_data('population', '*', "Country = 'China'"))
    print(db_manager.select_data('population', 'Population', "Country = 'Indonesia'"))
    
    
    

    db_manager.close()
