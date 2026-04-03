import mysql.connector
import os

def setup_database():
    try:
        # Initial connection to create database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="" # Default for many local setups
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS finance_tracker")
        cursor.close()
        conn.close()

        # Connect to the new database to create tables
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="finance_tracker"
        )
        cursor = conn.cursor()

        # Read schema file
        schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        # Execute multiple statements
        for statement in schema_sql.split(';'):
            if statement.strip():
                cursor.execute(statement)
        
        conn.commit()
        print("Database and tables created successfully!")
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        print("Please ensure MySQL is running and update the password in db_setup.py if needed.")

if __name__ == "__main__":
    setup_database()
