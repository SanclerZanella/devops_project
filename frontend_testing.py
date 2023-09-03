import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestDisplayUserRoute(unittest.TestCase):
    """
        Description:
            Test different behaviours from the WEB API app.

        Class Properties:
            * WEB_BASE_URL - Base WEB API url from where the others routes can be accessed.

        Methods:
            * setUp - Set up any common resources needed for the tests.
            * tearDown - Clean up environment after each test case concludes.
            * test_A_display_user_route - Test if the expected elements are present in the browser.
    """

    WEB_BASE_URL = "http://127.0.0.1:5001"

    def setUp(self):
        # Create an instance of the Chrome WebDriver
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_A_display_user_route(self):
        user_id = "1"
        expected_user_name = "John"

        # GET request to the WEB API.
        self.driver.get(f"{self.WEB_BASE_URL}/users/get_user_data/{user_id}")

        # Retrieve HTML element text content by ID
        user_element = self.driver.find_element(By.ID, "user")
        actual_user_name = user_element.text

        # Check if the expected elements are present in the browser
        self.assertEqual(actual_user_name, expected_user_name)


if __name__ == "__main__":
    unittest.main()
