import os
import unittest
import requests
import pymysql
if os.path.exists('env.py'):
    import env


class TestBackend(unittest.TestCase):

    API_BASE_URL = "http://127.0.0.1:5000/"

    def setUp(self):
        # Set up any common resources needed for the tests
        self.connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME")
        )

    def test_A_post_request_user(self):
        # Step 1: POST new user data
        post_payload = {"user_name": "Anamim"}
        response_post = requests.post(f"{self.API_BASE_URL}/users/2", json=post_payload)
        self.assertEqual(response_post.status_code, 200)

    def test_B_get_request_user(self):
        # Step 2: GET user data
        response_get = requests.get(f"{self.API_BASE_URL}/users/2")
        self.assertEqual(response_get.status_code, 200)

    def test_C_database_stored_data(self):
        # Step 3: Check database for stored data
        with self.connection.cursor() as cursor:
            query = "SELECT user_name FROM users WHERE user_id = 2"
            cursor.execute(query)
            result = cursor.fetchone()
            self.assertEqual(result[0], "Anamim")

    @classmethod
    def tearDownClass(cls):
        # Clean up after the last test
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME")
        )
        with connection.cursor() as cursor:
            delete_query = "DELETE FROM users WHERE user_id = %s"
            cursor.execute(delete_query, (2,))
            connection.commit()
        connection.close()


if __name__ == '__main__':
    unittest.main()
