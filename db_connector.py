import os
import pymysql
if os.path.exists('env.py'):
    import env

class ConnectDB:
    def __init__(self):
        self.db_host = os.getenv("DB_HOST")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")

    def connect_db(self):
        return pymysql.connect(
                    host=self.db_host,
                    user=self.db_user,
                    password=self.db_password,
                    db=self.db_name,
                )

    def test_DB_conn(self):
        try:
            conn = self.connect_db()
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")  # Execute a simple query to check connection

            return True

        except pymysql.Error as e:
            return f"Database connection failed: {e}"
