import unittest
from main import create_app
from dotenv import load_dotenv
import os

# Load the environment variable manually
load_dotenv()

# Set the FLASK_ENV to testing
os.environ["FLASK_ENV"]="testing"

class TestPharmacies(unittest.TestCase):

    def setUp(self):
        "This function runs before each test to prepare for them"
        # create app instance to test
        self.app = create_app()
        # the test_client function generates an imaginary browser that can make requests
        self.client = self.app.test_client()

    def test_pharmacy_index(self):
        "Use the client to make a request"
        response = self.client.get("/pharmacies/")
        data = response.get_json()
        
        # Now to perform tests on the response
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
    
    def test_create_bad_pharmacy(self):
        response = self.client.post("/pharmacies/", json={"pharmacy_name": ""})
        self.assertEqual(response.status_code, 400)


# Reminder, to run the test use command: 
# python -m unittest discover -s tests -v
# within the inner my_app folder where the test folder belongs 
# otherwise an error will be generated due to import issues

# We can also run the following command from the OUTER my_app using:
# python -m unittest discover -s my_app/tests -v
# However, we will need to reconfigure the .flasenv file and replace:
# FLASK_APP=my_app/main:create_app 
# with:
# FLASK_APP=main:create_app