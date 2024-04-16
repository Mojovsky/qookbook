import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import User



class TestUser(unittest.TestCase):
    def test_name_validation(self):
        with self.assertRaises(ValueError):
            user = User('123', '', 'password1')
        with self.assertRaises(ValueError):
            user = User('123', 'ab', 'password1')
        with self.assertRaises(ValueError):
            user = User('123', 'abcdefghijk', 'password1')


    def test_password_validation(self):
        with self.assertRaises(ValueError):
            user = User('123', 'name', 'pwd')


    def test_verify_password_true(self):
        user = User('123', 'name', 'password1')
        user.password = user.hash_password('password1')
        self.assertTrue(user.verify_password('password1'))
        

    def test_verify_password_false(self):
        user = User('123', 'name', 'password1')
        user.password = user.hash_password('password1')
        self.assertFalse(user.verify_password('2password'))


    def test_to_json(self):
        user = User('123    ', 'name', 'password1')


    def test_to_json(self):
        user = User(1, 'testuser', 'testpassword')
        expected_output = {
            1: {
                'username': 'testuser',
                'password': user.hash_password('testpassword')
            }
        }
        self.assertEqual(user.to_json(), expected_output)



if __name__ == '__main__':
    unittest.main()