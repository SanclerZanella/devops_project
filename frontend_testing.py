import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestDisplayUserRoute(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_A_display_user_route(self):
        user_id = "1"
        expected_user_name = "John"

        self.driver.get(f"http://127.0.0.1:5001/users/get_user_data/{user_id}")

        user_element = self.driver.find_element(By.ID, "user")
        actual_user_name = user_element.text

        self.assertEqual(actual_user_name, expected_user_name)


if __name__ == "__main__":
    unittest.main()
