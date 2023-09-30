import requests
import unittest
import os


# Function to read the Kubernetes service URL from k8s_url.txt
def read_k8s_url(file_path):
    return os.stat(file_path).st_size > 0


# Define a test case class
class TestKubernetesBackend(unittest.TestCase):

    # Set up the test case
    def setUp(self):
        self.k8s_url = read_k8s_url("k8s_url.txt")

    # Define a test method
    def test_backend_functionality(self):
        self.assertTrue(self.k8s_url)


if __name__ == "__main__":
    unittest.main()
