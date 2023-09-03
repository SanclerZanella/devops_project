import pymysql

class CreateTables:
    """
        Description:
            Creates the necessary database tables for the application.

        Parameters:
            * db - Database connection.

        Object Properties:
            * self.connection - Database connection, assigned by the parameter 'db'.
            * self.table_names - List of strings containing the tables names.

        Methods:
            * create_table - Creates the necessary database tables.
    """
    def __init__(self, db=None):
        self.connection = db
        self.table_names = ['users', 'config']

    def create_table(self):
        # Get each table name in the self.table_names list
        for table in self.table_names:
            table_name = table

            try:
                # Check if table already exists in the database
                check_table_query = f"SHOW TABLES LIKE '{table_name}'"
                with self.connection.cursor() as cursor:
                    cursor.execute(check_table_query)
                    table_exists = cursor.fetchone()

                if table_exists:
                    print(f"{table} already exists")

                else:
                    # Creates table, if tables doesn't exist in the database
                    create_table_query = f'''
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        user_id INT PRIMARY KEY NOT NULL,
                        user_name VARCHAR(50) NOT NULL,
                        creation_date DATETIME
                    )
                    '''
                    with self.connection.cursor() as cursor:
                        cursor.execute(create_table_query)

                    self.connection.commit()
                    print("Table created successfully.")

            except pymysql.Error as e:
                print(f"Error creating table: {e}")
