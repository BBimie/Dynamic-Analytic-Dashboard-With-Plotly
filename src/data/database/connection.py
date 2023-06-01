import sqlite3
from sqlite3 import Error
import pandas as pd
import csv
from src.data.database.statements import DatabaseSetup

class Database:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name

    def create_db(self,):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.db_name)
            print('SQLITE VERSION',sqlite3.version)
            return conn
        except Error as e:
            print(e)

    def connect(self):
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except Error as e:
            print(e)


    def create_tables(self):
        conn = self.create_db()
        cursor = conn.cursor()

        for table in DatabaseSetup().all_tables():
            create_statement: str = table.get('create_query')
            data_file: str = f"src/data/raw_data/{table.get('file')}"
            insert_statement: str = table.get('insert_query')

            # Creating the table into the database
            cursor.execute(create_statement, '')

            # Opening the asscociated file
            data = open(data_file)
            contents = csv.reader(data, )
            next(contents)

            # Importing the contents of the file the associated table
            cursor.executemany(insert_statement, contents)
            
            table_name = data_file.replace('.csv', '').replace('src/data/raw_data/', '')
            try:
                select_all = f"SELECT * FROM {table_name} LIMIT 5"
                cursor.execute(select_all).fetchall()
                print(f"==== {table_name} successfully created and data inserted ===")
            except Exception as e:
                print(f"=== {e} ==")

            

        # Committing the changes
        conn.commit()
            
        # closing the database connection
        conn.close()


#Database('ecommerce').create_tables()
