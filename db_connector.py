import os
import pymysql
if os.path.exists('env.py'):
    import env


class ConnectDB:
    """
        Description:
            Creates database connection and test if it is working.

        Class Parameters:
            * username (type: string) - Username to access the database.
            * password (type: string) - Password to access the database.

        Object Properties:
            * self.db_host - Host to access the database.
            * self.db_user - Username to access the database, assigned by the class parameter 'username'.
            * self.db_password - Password to access the database, assigned by the class parameter 'password'.
            * self.db_name - Database's name to access the database.

        Methods:
            * setUp - Set up any common resources needed for the tests.
            * connect_db - Create a database connections based on the credentials provided.
            * Check_DB_conn - Check if database connection is working properly.
    """
    def __init__(self, username: str, password: str):
        self.db_host = os.getenv("DB_HOST")
        self.db_user = username
        self.db_password = password
        self.db_name = os.getenv("DB_NAME")

    def connect_db(self):
        return pymysql.connect(
                    host=self.db_host,
                    user=self.db_user,
                    password=self.db_password,
                    db=self.db_name,
                )

    def Check_DB_conn(self):
        try:
            conn = self.connect_db()
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")  # Execute a simple query to check connection

            return True

        except pymysql.Error as e:
            return f"Database connection failed: {e}"
