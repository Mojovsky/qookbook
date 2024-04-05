import unittest
from data_manipulation import User

class TestUser(unittest.TestCase):
    def test_name_validation(self):
        with self.assertRaises(ValueError):
            user = User('', 'test@test.com', 'password1')
        with self.assertRaises(ValueError):
            user = User('ab', 'test@test.com', 'password1')
        with self.assertRaises(ValueError):
            user = User('abcdefghijk', 'test@test.com', 'password1')

    def test_email_validation(self):
        with self.assertRaises(ValueError):
            user = User('name', 'invalid_email', 'password1')

    def test_password_validation(self):
        with self.assertRaises(ValueError):
            user = User('name', 'test@test.com', 'pwd')

    def test_verify_password_true(self):
        user = User('name', 'test@test.com', 'password1')
        user.password = user.hash_password('password1')
        self.assertTrue(user.verify_password('password1'))
        
    def test_verify_password_false(self):
        user = User('name', 'test@test.com', 'password1')
        user.password = user.hash_password('password1')
        self.assertFalse(user.verify_password('2password'))

if __name__ == '__main__':
    unittest.main()