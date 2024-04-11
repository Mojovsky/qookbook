import api_edamam
import hashlib
import json
import re


def main():
    user_interaction = UserInteraction()
    data_manipulation = DataManipulation("data/recipes.json")
    recipes = user_interaction.search_recipes(["lettuce", "bacon", "tomato"])
    data_manipulation.create_temp_recipes(recipes)



class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


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
                'password': self.hash_password(self._password)
            }
        }
    


class Recipe:
    def __init__(self, title, url, image, users=None):
        self.title = title
        self.url = url
        self.image = image
        self.users = users if users else []


    def to_json(self):
        return {
            self.title: {
            "url": self.url,
            "image": self.image,
            "users": self.users,
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
    

    def create_temp_recipes(self, recipes):
        self.file_path = "data/temp_recipes.json"
        self.data = {}
        for recipe in recipes:
            recipe = Recipe(**recipe)
            self.add_object(recipe)


    def get_fav_recipe_list(self, username):
        fav_list = []
        for title in self.data:
            if username in self.data[title]['users']:
                recipe_data = self.data[title]
                fav_list.append(recipe_data)
        return fav_list



class UserInteraction:
    def __init__(self):
        self.user_manipulation = DataManipulation("data/users.json")
        self.recipe_manipulation = DataManipulation("data/recipes.json")
        self.temp_recipe_manipulation = DataManipulation("data/temp_recipes.json")



    def create_user(self, username, email, password):
        data = self.user_manipulation.read_file()
        if username in data:
            raise ValueError("Username already exists")
        user = User(username, email, password)
        self.user_manipulation.add_object(user)
        return user
            

    def login(self, username, password):
        user = self.user_manipulation.get_user_object(username)
        if user is None:
            raise ValueError("Invalid username")
        if not user.verify_password(password):
            raise ValueError("Invalid password")
        return user
        
    
    def search_recipes(self, ingridients):
        url = api_edamam.get_recipe_url(ingridients)
        data = api_edamam.api_response(url)
        recipe_data = api_edamam.extract_recipe_data(data)
        self.recipe_manipulation.create_temp_recipes(recipe_data)
        return recipe_data
    

    def add_fav_recipe(self, username, recipe):
        recipe = Recipe(**recipe)
        recipe.users.append(username)
        self.recipe_manipulation.add_object(recipe)




if __name__ == "__main__":
    main()
