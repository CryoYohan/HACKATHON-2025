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
    
    def get_volunteers_by_post(self, post_id: int):
        """Fetches all volunteers who have joined a specific post."""
        query = '''
            SELECT pp.id, pp.user_id, u.name, u.profileicon 
            FROM Post_Participation pp
            JOIN user u ON pp.user_id = u.id
            WHERE pp.post_id = ?
        '''
        print(f"Executing query: {query} with post_id={post_id}")
        return self.getprocess(query, (post_id,))

    def getall_records(self, table: str) -> list:
        """Retrieves all records from a specified table."""
        query = f"SELECT * FROM {table}"
        return self.getprocess(query)
    
    def getall_records_with_user(self, table: str) -> list:
        """Retrieves all records from the specified table and joins with the user table to get user names."""
        # Define the query to join 'post' and 'user' tables
        query = f'''
            SELECT p.id, p.title, p.content, 
                p.category, p.type, p.event_date, p.status, 
                p.created_at, p.location, p.picture, u.name, u.email,u.profileicon
            FROM {table} p
            JOIN user u ON p.user_id = u.id
        '''
        return self.getprocess(query)
    
    def find_record_with_user(self, table: str, id: int):
        """Finds a specific post record by user email, joining with the user table."""
        query = f'''
            SELECT p.id, p.title, p.content, 
                p.category, p.type, p.event_date, p.status, 
                p.created_at, p.location, p.picture,u.id as user_id, 
                u.name, u.email, u.profileicon
            FROM {table} p
            JOIN user u ON p.user_id = u.id
            WHERE p.id = ?
        '''
        print(f"Executing query: {query} with id={id}")
        return self.getprocess(query, (id,))


    def find_record(self, table: str, email: str):
        """Finds a specific record by email."""
        sql = f"SELECT * FROM {table} WHERE email = ?"
        print(f"Executing query: {sql} with email={email}")
        return self.getprocess(sql, (email,))
    
    def find_record_by_user_post(self, table: str, user_id: int, post_id: int):
        """Finds a specific record based on user_id and post_id."""
        sql = f'''
            SELECT * FROM {table} 
            WHERE user_id = ? AND post_id = ?
        '''
        print(f"Executing query: {sql} with user_id={user_id}, post_id={post_id}")
        return self.getprocess(sql, (user_id, post_id))


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