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
            headers = ["".join([c if c.isalnum() else '_' for c in header.strip()]) for header in headers]
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

            headers_with_types = [header + ' TEXT' for header in headers]  # assuming all columns are of type TEXT

            self.cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.cur.execute(f"CREATE TABLE {table_name} ({', '.join(headers_with_types)})")
            for row in dr:
                row = {key: value.strip() if isinstance(value, str) else value for key, value in row.items()}  # stripping leading/trailing spaces from values
                self.cur.execute(f"INSERT INTO {table_name} VALUES ({', '.join('?' * len(headers))})", list(row.values()))
        self.conn.commit()
        
    def create_country_table_from_csv(self, csv_file, table_name):
        with open(csv_file, 'r') as f:
            dr = csv.DictReader(f)
            headers = dr.fieldnames
            headers = [header.replace(" ", "_").replace("(", "").replace(")", "") for header in headers]
            headers_with_types = [header + ' TEXT' for header in headers] 

            self.cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.cur.execute(f"CREATE TABLE {table_name} (City TEXT, Country TEXT, Salary REAL)")

            inserted_countries = set()  # store inserted countries
            for row in dr:
                row = {key: value.strip() if isinstance(value, str) else value for key, value in row.items()}
                country = row['Country']
                if country not in inserted_countries:
                    self.cur.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?)", (row['City'], row['Country'], row['Salary']))
                    inserted_countries.add(country)  # add the country to the set

            self.conn.commit()
            
    def create_population_table_from_csv(self, csv_file, table_name):
        with open(csv_file, 'r') as f:
            dr = csv.DictReader(f)
            headers = ['Country', 'Population']  # Only include these columns

            # The rest of this method is the same as before...
            headers_with_types = [header + ' TEXT' for header in headers]  # assuming all columns are of type TEXT

            self.cur.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.cur.execute(f"CREATE TABLE {table_name} ({', '.join(headers_with_types)})")

            for row in dr:
                row = {key: value.strip() if isinstance(value, str) else value for key, value in row.items()}  # stripping leading/trailing spaces from values
                self.cur.execute(f"INSERT INTO {table_name} VALUES (?, ?)", (row['Country'], row['Population']))

        self.conn.commit()
        
    def cleanup_obesity_data(self, table_name):
        self.cur.execute(f"SELECT * FROM {table_name}")
        data = self.cur.fetchall()
        cleaned_data = []
        for row in data:
            country, obesity_rate = row
            cleaned_rate = obesity_rate.split(' ')[0]  # retain only the average
            cleaned_data.append((country, cleaned_rate))
        return cleaned_data
    
    def create_cleaned_obesity_table(self, table_name, cleaned_data):
        self.cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.cur.execute(f"CREATE TABLE {table_name} (Country TEXT, Obesity_Rate REAL)")
        self.cur.executemany(f"INSERT INTO {table_name} VALUES (?, ?)", cleaned_data)
        self.conn.commit()







    def select_data(self, table_name, column_name, condition=None):
        if column_name == '*':
            if condition:
                self.cur.execute(f"SELECT * FROM {table_name} WHERE {condition}")
            else:
                self.cur.execute(f"SELECT * FROM {table_name}")
        else:
            if condition:
                self.cur.execute(f"SELECT \"{column_name}\" FROM {table_name} WHERE {condition}")
            else:
                self.cur.execute(f"SELECT \"{column_name}\" FROM {table_name}")
        return self.cur.fetchall()




    def select_all_data(self, table_name, column_name):
        if column_name == '*':
            self.cur.execute(f"SELECT * FROM {table_name}")
        else:
            self.cur.execute(f"SELECT \"{column_name}\" FROM {table_name}")
        return self.cur.fetchall()


    def update_data(self, table_name, column_name, new_value, condition):
        self.cur.execute(f"UPDATE {table_name} SET \"{column_name}\" = ? WHERE {condition}", (new_value,))
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
            
    def select_data_by_year(self, table_name, new_table_name, year):
        self.cur.execute(f"DROP TABLE IF EXISTS {new_table_name}")
        self.cur.execute(f"CREATE TABLE {new_table_name} AS SELECT * FROM {table_name} WHERE Year = {year}")
        self.conn.commit()

    def select_data_by_sex(self, table_name, new_table_name, sex):
        self.cur.execute(f"DROP TABLE IF EXISTS {new_table_name}")
        self.cur.execute(f"CREATE TABLE {new_table_name} AS SELECT * FROM {table_name} WHERE Sex = '{sex}'")
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
    #data = db_manager.select_data('my_table', 'Population', "Country = 'China'")
    #print('Population of China:', data)

    # Get all data for USA
    #data = db_manager.select_data('my_table', '*', "Country = 'USA'")
    #print('Data for USA:', data)

    # Update population density of Indonesia
    #db_manager.update_data('my_table', 'Population_Density_PerSqKm', '150', "Country = 'Indonesia'")

    # Check if the update has been successful
    #data = db_manager.select_data('my_table', 'Population_Density_PerSqKm', "Country = 'Indonesia'")
    #print('Updated Population Density for Indonesia:', data)
    
    # Remove columns from the table, tested working
    
    #db_manager.remove_column('my_table', 'Population_Density_PerSqKm')
    
    #data = db_manager.select_data('my_table', 'Population', "Country = 'Indonesia'")
    #print('Updated Population Density for Indonesia:', data)
    
    db_manager.create_population_table_from_csv('population_by_country_2020.csv', 'Population')
    #print(db_manager.select_data('Population', '*', "Country = 'China'"))
    #print(db_manager.select_data('Population', 'Population', "Country = 'China'"))
    
    
    db_manager.create_table_from_csv('obesity-cleaned.csv', 'obesity1')  
    db_manager.select_data_by_year('obesity1', 'obesity2', '2016')
    db_manager.select_data_by_sex('obesity2', 'obesity3', 'Both sexes')
    #print(db_manager.select_data('obesity1', '*', "Country = 'Afghanistan'")) 
    #print(db_manager.select_data('obesity2', '*', "Country = 'Afghanistan'")) 
    #print(db_manager.select_data('obesity3', '*', "Country = 'Afghanistan'")) 
    db_manager.remove_column('obesity3', 'Year')
    db_manager.remove_column('obesity3', 'Rank')
    db_manager.remove_column('obesity3', 'Sex')
    
    #print(db_manager.select_data('obesity3', 'Obesity', "Country = 'Afghanistan'"))   
    #data = db_manager.select_data('obesity3', 'Obesity', "Country = 'China'")
    #print(data)
        
    db_manager.create_country_table_from_csv('cost-of-living_v2.csv', 'Salary')
    db_manager.remove_column('Salary', 'City')
    
    data = db_manager.select_data('Salary', '*', "Country = 'China'")
    print(data)
    
    data = db_manager.select_data('Salary', 'Country', "Salary = '471.75'")
    print(data)
    
    #data = db_manager.select_all_data('Salary', '*')
    #print(data)
    
    #prints all data from the table
    #data = db_manager.select_all_data('population', '*')
    #print(data)
    
    #data = db_manager.select_data('Population', 'Population', "Country = 'China'")
    #print(data)

    #data = db_manager.select_all_data('Obesity', '*')
    #print(data)
    
    # Cleanup obesity data and create a new table with the cleaned data
    cleaned_data = db_manager.cleanup_obesity_data('obesity3')
    db_manager.create_cleaned_obesity_table('Obesity', cleaned_data)
    
    db_manager.update_data('Salary', 'Country', 'United States of America', "Country = 'United States'")
    data = db_manager.select_data('Salary', '*', "Country = 'United States of America'")
    print(data)
    # Now you can test the cleaned table:
    #data = db_manager.select_all_data('Obesity', '*')
    #print(data)

    

    
    

    db_manager.close()
