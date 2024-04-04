import hashlib
import os
import binascii
import json

class User:
    def __init__(self, name, email, password, salt=None, password_hash=None, tags=None):
        self.name = name
        self.email = email
        if salt is None or password_hash is None:
            self.encrypt_password(password)
        else:
            self._salt = salt
            self._password_hash = password_hash
        self.tags = tags if tags else []
        

    @property
    def salt(self):
        return self._salt


    @salt.setter
    def salt(self, value):
        raise AttributeError('salt: Not writable.')


    @property
    def password_hash(self):
        return self._password_hash


    @password_hash.setter
    def password_hash(self, value):
        raise AttributeError('password_hash: Not writable.')


    def encrypt_password(self, password):
        self._salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), self._salt, 100000)
        self._password_hash = binascii.hexlify(key).decode()


    def verify_password(self, password):
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), self._salt, 100000)
        return self._password_hash == binascii.hexlify(key).decode()


    def to_json(self):
        return {
            self.name: {
                'email': self.email,
                'salt': binascii.hexlify(self._salt).decode(),
                'password_hash': self._password_hash,
                'tags': self.tags
            }
        }
    

    @classmethod
    def from_json(cls, name, data):
        email = data['email']
        salt = binascii.unhexlify(data['salt'])
        password_hash = data['password_hash']
        tags = data['tags']
        return cls(name, email, salt, password_hash, tags)
        


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
        self.data = self.read_file()


    def read_file(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: file {self.file_path} not found")
        

    def write_file(self, data):
        with open(self.file_path, 'w') as file:
            json.dump(data, file, indent=4)


    def add_object(self, obj):
        json_obj = obj.to_json()
        self.data.update(json_obj)
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def get_user_object(self, name):
        user_data = self.data[name]
        user_object = User.from_json(name, user_data)
        return user_object




def main():
    file_manipulation = FileManipulation("data/users.json")
    user = file_manipulation.get_user_object("Bob")
    print(user.verify_password("mellon"))


if __name__ == "__main__":
    main()
