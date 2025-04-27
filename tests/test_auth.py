import unittest
from app import app

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_me_unauthenticated(self):
        response = self.client.get("/me")
        self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()
