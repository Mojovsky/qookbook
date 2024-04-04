import hashlib
import json
import re

class User:
    def __init__(self, name, email, password, tags=None):
        self.name = name
        self.email = email
        self._password = password
        self.tags = tags if tags else []


    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Username cannot be empty")
        if len(name) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(name) > 10:
            raise ValueError("Username must be less than 10 characters long")
        self.name= name

    @property
    def email(self):
        return self.email

    @email.setter
    def email(self, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        self._email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        if not re.match(r"^(?=.*[0-9A-Za-z]).{4,15}$", password):
            raise ValueError("Password must be between 4 and 15 characters long and contain at least 1 number or special character")
        self._password = password


    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()


    def verify_password(self, password):
        key = hashlib.sha256(password.encode()).hexdigest()
        return self._password == key


    def to_json(self):
        return {
            self.name: {
                'email': self.email,
                'password': self.hash_password(self._password),
                'tags': self.tags
            }
        }
    

    @classmethod
    def from_json(cls, name, data):
        email = data['email']
        password = data['password']
        tags = data['tags']
        return cls(name, email, password, tags)
        


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
    


class DataManipulation:
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
        return User.from_json(name, user_data)





def main():
    data_manipulation = DataManipulation("data/users.json")
    #user = file_manipulation.get_user_object("Dan")
    #print(user.verify_password("prettylittlewords"))
    user = User("Big Joe", "big.joe@gmail.com", "bigjoe")
    data_manipulation.add_object(user)


if __name__ == "__main__":
    main()
