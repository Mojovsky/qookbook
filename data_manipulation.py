import hashlib
import os
import binascii
import json

class User:
    def __init__(self, name, email, password, tags=None):
        self.name = name
        self.email = email
        self._salt = os.urandom(32)  # Store the salt
        self._password_hash = self._hash_password(password)
        self.tags = tags if tags is not None else [] # Store the tags associated with the user
    
    @property
    def salt(self):
        raise AttributeError('salt: Not readable.')

    @salt.setter
    def salt(self, value):
        raise AttributeError('salt: Not writable.')

    @property
    def password_hash(self):
        raise AttributeError('password_hash: Not readable.')

    @password_hash.setter
    def password_hash(self, value):
        raise AttributeError('password_hash: Not writable.')

    def _hash_password(self, password):
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), self.salt, 100000)
        return binascii.hexlify(key).decode()  # Store the hashed password as hexadecimal string

    def verify_password(self, password):
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), self.salt, 100000)
        return self.password_hash == binascii.hexlify(key).decode()

    def change_password(self, new_password):
        self._salt = os.urandom(32)  # Generate a new salt
        self._password_hash = self._hash_password(new_password)  # Hash the new password

    def to_json(self):
        return json.dumps({
            'name': self.name,
            'email': self.email,
            'salt': binascii.hexlify(self.salt).decode(),
            'password_hash': self.password_hash,
            'tags': self.tags
        })

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        user = cls(data['name'], data['email'], '', data.get('tags', []))
        user.salt = binascii.unhexlify(data['salt'])
        user.password_hash = data['password_hash']
        return user


class Recipe:
    def __init__(self, title, link, id, image, tags, rating:None):
        self.title = title
        self.link = link
        self.id = id
        self.image = image
        self.tags = tags
        self.rating = rating

    def to_json(self):
        return json.dumps({
            'title': self.title,
            'link': self.link,
            'id': self.id,
            'image': self.image,
            'tags': self.tags,
            'rating': self.rating
        })

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(data['title'], data['link'], data['id'], data['image'], data['tags'], data['rating'])


class FileManipulation:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: file {self.file_path} not found")

    def write_file(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)