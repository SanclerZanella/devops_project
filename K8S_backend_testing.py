import requests
import unittest


# Function to read the Kubernetes service URL from k8s_url.txt
def read_k8s_url():
    try:
        with open("k8s_url.txt", "r") as file:
            url = file.read().strip()
            return url
    except FileNotFoundError:
        return None


# Define a test case class
class TestKubernetesBackend(unittest.TestCase):

    # Set up the test case
    def setUp(self):
        self.k8s_url = read_k8s_url()

    # Define a test method
    def test_backend_functionality(self):
        if self.k8s_url is not None:
            try:
                response = requests.get(self.k8s_url + "/users/1")
                self.assertEqual(response.status_code, 200)
                # You can add more assertions here as needed
            except requests.exceptions.RequestException as e:
                self.fail(f"Test failed. Error: {str(e)}")
        else:
            self.fail("Test cannot be performed due to missing Kubernetes service URL.")


if __name__ == "__main__":
    unittest.main()
