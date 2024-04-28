import sqlite3
import csv

db_name = 'regex_database.db'

# Function to create database and table
def create_database():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS regex (
                 id INTEGER PRIMARY KEY,
                 short_description TEXT,
                 search_regex TEXT,
                 replacement_regex TEXT
                 )''')
    
    # Save (commit) the changes
    conn.commit()
    conn.close()

# Function to fill the table with records from CSV
def fill_table():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    
    with open('regex_to_load.csv', 'r') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Skip header
        for row in reader:
            c.execute("INSERT INTO regex (short_description, search_regex, replacement_regex) VALUES (?, ?, ?)", row)
    
    # Save (commit) the changes
    conn.commit()
    conn.close()

# Create database and table
create_database()

# Fill the table with records from CSV
fill_table()
