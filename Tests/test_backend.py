import unittest
import json
import sys
sys.path.append('../backend_server')
from main import app

class TestApp(unittest.TestCase):

    def setUp(self):
        # Create a test client for the app
        self.app = app.test_client()

    def test_test_route(self):
        # Test the '/test' route
        response = self.app.get('/test')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'Server is up')

    def test_signup_route(self):
        # Test the '/signup' route
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.app.post('/signup', json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Username already exists.')

    def test_signin_route(self):
        # Test the '/signin' route
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.app.post('/signin', json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access_token' in data)

    # Add more test cases for other routes as needed

if __name__ == '__main__':
    unittest.main()
