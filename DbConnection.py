import sqlite3

class DbConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn    = None

    def execute_query(self, *query):
        self.connect()
        c = self.conn.cursor()
        # Execute query
        c.execute(*query)
        records = c.fetchall()
        self.close()
        return records

    def connect(self):
        # Connect to the database
        self.conn = sqlite3.connect(self.db_name)

        
    def close(self):
        # Close database connection
        self.conn.close()

    
    def get_table_fields(self, table_name):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        fields = [row[1] for row in cursor.fetchall()]
        self.close()
        return fields