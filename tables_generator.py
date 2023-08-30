import pymysql

class CreateTables:
    def __init__(self, db=None):
        self.connection = db
        self.table_names = ['users', 'config']

    def create_table(self):
        for table in self.table_names:
            table_name = table

            try:
                check_table_query = f"SHOW TABLES LIKE '{table_name}'"

                with self.connection.cursor() as cursor:
                    cursor.execute(check_table_query)
                    table_exists = cursor.fetchone()

                if table_exists:
                    print(f"{table} already exists")

                else:
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
