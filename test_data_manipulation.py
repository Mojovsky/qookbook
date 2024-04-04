import unittest
from data_manipulation import User

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User('John Doe', 'john@example.com', 'password123')

    def test_hash_password(self):
        # The hashed password should be a string
        self.assertIsInstance(self.user.password_hash, str)

        # The hashed password should not be the same as the plain password
        self.assertNotEqual(self.user.password_hash, 'password123')

    def test_verify_password(self):
        # The verify_password method should return True for the correct password
        self.assertTrue(self.user.verify_password('password123'))

        # The verify_password method should return False for an incorrect password
        self.assertFalse(self.user.verify_password('wrongpassword'))

if __name__ == '__main__':
    unittest.main()