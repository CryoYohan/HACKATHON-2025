from sqlite3 import connect, Row

class Databasehelper:
    def __init__(self) -> None:
        self.database = 'kapitbisig.db'

    def getdb_connection(self):
        """Establishes and returns a database connection."""
        connection = connect(self.database)
        connection.row_factory = Row  # Ensures results are returned as dictionaries
        return connection

    def getprocess(self, sql: str, params=()):
        """Executes a SELECT query and returns results."""
        connection = self.getdb_connection()
        cursor = connection.cursor()
        cursor.execute(sql, params)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data

    def postprocess(self, sql: str, params=()):
        """Executes an INSERT, UPDATE, or DELETE query."""
        connection = self.getdb_connection()
        cursor = connection.cursor()
        cursor.execute(sql, params)
        connection.commit()
        row_count = cursor.rowcount
        cursor.close()
        connection.close()
        return row_count > 0  # Returns True if at least one row is affected

    def getall_records(self, table: str) -> list:
        """Retrieves all records from a specified table."""
        query = f"SELECT * FROM {table}"
        return self.getprocess(query)

    def find_record(self, table: str, email: str):
        """Finds a specific record by email."""
        sql = f"SELECT * FROM {table} WHERE email = ?"
        print(f"Executing query: {sql} with email={email}")
        return self.getprocess(sql, (email,))

    def add_record(self, table:str, **kwargs):
        """Adds a new record to a table."""
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["?" for _ in kwargs])
        values = tuple(kwargs.values())

        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return self.postprocess(sql, values)

    def update_record(self, table:str, **kwargs):
        """Updates an existing record in a table."""
        keys = list(kwargs.keys())
        values = list(kwargs.values())

        if len(keys) < 2:
            return False  # Ensures there's at least one field to update

        set_clause = ", ".join([f"{key} = ?" for key in keys[1:]])
        sql = f"UPDATE {table} SET {set_clause} WHERE {keys[0]} = ?"

        return self.postprocess(sql, values[1:] + [values[0]])  # Moves ID to the end

    def delete_record(self, table: str, **kwargs):
        """Deletes a record based on the given criteria."""
        keys = list(kwargs.keys())
        values = list(kwargs.values())

        sql = f"DELETE FROM {table} WHERE {keys[0]} = ?"
        return self.postprocess(sql, (values[0],))