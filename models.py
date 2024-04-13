import api_edamam
import hashlib
import json
import uuid
import re


def main():
    user_interaction = UserInteraction()
    #user_interaction.create_user("test2", "test2")
    #user_interaction.create_user("test", "test@gmail.com", "test")
    #user = user_interaction.login("test", "test")
    #print(user.id)
    #data_manipulation = DataManipulation("data/recipes.json")
    #recipes = user_interaction.search_recipes(["pasta", "mushroom", "tomato"])
    #recipe_obj = user_interaction.temp_recipe_manipulation.get_recipe_object("Pasta Primavera")
    #user_interaction.recipe_manipulation.add_fav_recipe(user.id, recipe_obj)
    #fav_list = user_interaction.get_fav_recipes(user.id)
    #print(fav_list)


class User:
    def __init__(self, id, username, password):
        self.username = username
        self.id = id
        self.password = password


    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


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
            self.id: {
                'username': self.username,
                'password': self.hash_password(self._password)
            }
        }
    


class Recipe:
    def __init__(self, title, url, users=None):
        self.title = title
        self.url = url
        self.users = users if users else []


    def to_json(self):
        return {
            self.title: {
            "url": self.url,
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


    def get_user_object(self, id):
        user_data = self.data[id]
        return User(id, **user_data)
    

    def get_recipe_object(self, title):
        recipe_data = self.data[title]
        return Recipe(title, **recipe_data)
    

    def create_temp_recipes(self, recipes):
        self.file_path = "data/temp_recipes.json"
        self.data = {}
        for recipe in recipes:
            recipe = Recipe(**recipe)
            self.add_object(recipe)


    def add_fav_recipe(self, id, recipe_obj):
        self.file_path = "data/recipes.json"
        recipe_obj.users.append(id)
        self.add_object(recipe_obj)



class UserInteraction:
    def __init__(self):
        self.user_manipulation = DataManipulation("data/users.json")
        self.recipe_manipulation = DataManipulation("data/recipes.json")
        self.temp_recipe_manipulation = DataManipulation("data/temp_recipes.json")



    def create_user(self, username, password):
        data = self.user_manipulation.read_file()
        if username in data:
            raise ValueError("Username already taken")
        id = str(uuid.uuid4())
        user = User(id, username, password)
        self.user_manipulation.add_object(user)
        return user
            

    def login(self, username, password):
        data = self.user_manipulation.read_file()
        user = None
        for id, user_data in data.items():
            if username == user_data["username"]:
                user = self.user_manipulation.get_user_object(id)
                break
        if not user:
            raise ValueError("Invalid username")
        if not user.verify_password(password):
            raise ValueError("Invalid password")
        return user
    

    def get_fav_recipes(self, id):
        data = self.recipe_manipulation.read_file()
        fav_list = []
        for title in data:
            if id in data[title]['users']:
                recipe_obj = self.recipe_manipulation.get_recipe_object(title)
                fav_list.append(recipe_obj)
        return fav_list
        
    
    def search_recipes(self, ingridients):
        url = api_edamam.get_recipe_url(ingridients)
        data = api_edamam.api_response(url)
        recipe_data = api_edamam.extract_recipe_data(data)
        self.temp_recipe_manipulation.create_temp_recipes(recipe_data)
        return recipe_data





if __name__ == "__main__":
    main()
