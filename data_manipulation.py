import hashlib
import json
import re


def main(): ...
    #data_manipulation = DataManipulation("data/users.json")
    #user = data_manipulation.get_user_object("Dan")
    #print(user.verify_password("prettylittlewords"))
    #user = User("AD", "ad.com", "ad")
    #data_manipulation.add_object(user)


class User:
    def __init__(self, username, email, password, tags=None):
        self.username = username
        self.email = email
        self.password = password
        self.tags = tags if tags else []


    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        if not username:
            raise ValueError("Username cannot be empty")
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(username) > 10:
            raise ValueError("Username must be less than 10 characters long")
        self._username= username

    @property
    def email(self):
        return self._email

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
        if not re.match(r"^(?=.*[0-9A-Za-z]).{4,}$", password):
            raise ValueError("Password must be at least 4 characters long and contain at least 1 number or special character")
        self._password = password


    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()


    def verify_password(self, password):
        return self._password == self.hash_password(password)


    def to_json(self):
        return {
            self.username: {
                'email': self.email,
                'password': self.hash_password(self._password),
                'tags': self.tags
            }
        }
    


class Recipe:
    def __init__(self, title, url, image, tags=None, users=None, rating=None):
        self.title = title
        self.url = url
        self.image = image
        self.tags = tags if tags else []
        self.users = users if users else []
        self.rating = rating if rating else 0


    def to_json(self):
        return {
            self.title: {
            "url": self.url,
            "image": self.image,
            "tags": self.tags,
            "users": self.users,
            "rating": self.rating
            }
        }
    


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


    def get_user_object(self, username):
        user_data = self.data[username]
        return User(username, **user_data)
    

    def get_recipe_object(self, title):
        recipe_data = self.data[title]
        return Recipe(**recipe_data)
    

    def get_fav_recipe_list(self, username):
        fav_list = []
        for title in self.data:
            if username in self.data[title]['users']:
                recipe_data = self.data[title]
                recipe = self.get_recipe_object(recipe_data)
                fav_list.append(recipe)
        return fav_list
        



if __name__ == "__main__":
    main()
