import os
import unittest
import requests
import pymysql
if os.path.exists('env.py'):
    import env


class TestBackend(unittest.TestCase):
    """
        Description:
            Test different behaviours from the REST API app and database.

        Class Properties:
            * API_BASE_URL - Base REST API url from where the others routes can be accessed.

        Methods:
            * setUp - Set up any common resources needed for the tests.
            * test_A_post_request_user - Test if the REST API POST request returns a successful response.
            * test_B_get_request_user - Test if the REST API GET request returns a successful response.
            * test_C_database_stored_data - Test if the database has stored the expected data.

        Class Methods:
            * tearDownClass - Clean up the test environment at the end of the all test.
    """

    API_BASE_URL = "http://127.0.0.1:5000/"

    def setUp(self):
        # Create a DB Connection
        self.connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME")
        )

    def test_A_post_request_user(self):
        # Create new user on DB to test the REST API POST request
        post_payload = {"user_name": "Anamim"}
        response_post = requests.post(f"{self.API_BASE_URL}/users/2", json=post_payload)
        self.assertEqual(response_post.status_code, 200)

    def test_B_get_request_user(self):
        # Read the new user from DB to test the REST API GET request
        response_get = requests.get(f"{self.API_BASE_URL}/users/2")
        self.assertEqual(response_get.status_code, 200)

    def test_C_database_stored_data(self):
        # Read the new user from DB to test if the DB has properly stored the data.
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
