import api_edamam
import hashlib
import json
import uuid
import re



class User:
    """User class for creating user objects"""
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
        """Hashes the password using sha256 algorithm"""
        return hashlib.sha256(password.encode()).hexdigest()


    def verify_password(self, password):
        """Verifies the password by comparing the hashed password with the provided password"""
        return self._password == self.hash_password(password)


    def to_json(self):
        """Converts user object to json format"""
        return {
            self.id: {
                'username': self.username,
                'password': self.hash_password(self._password)
            }
        }
    


class Recipe:
    """Recipe class for creating recipe objects"""
    def __init__(self, id, title, url, users=None):
        self.id = id
        self.title = title
        self.url = url
        self.users = users if users else []


    def to_json(self):
        """Converts recipe object to json format"""
        return {
            self.id: {
            "title": self.title,
            "url": self.url,
            "users": self.users,
            }
        }
    


class DataManipulation:
    """Class for reading and writing data to json files"""
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
    

    def get_recipe_object(self, id):
        recipe_data = self.data[id]
        return Recipe(id, **recipe_data)



class UserInteraction:
    """Class for user interaction with the application"""
    def __init__(self):
        self.user_manipulation = DataManipulation("data/users.json")
        self.recipe_manipulation = DataManipulation("data/recipes.json")



    def create_user(self, username, password):
        """Creates a new user object and adds it to the users.json file"""
        data = self.user_manipulation.read_file()
        for id, user_data in data.items():
            if username == user_data["username"]:
                raise ValueError("Username already taken")
        id = str(uuid.uuid4())
        user = User(id, username, password)
        self.user_manipulation.add_object(user)
        return user
            

    def login(self, username, password):
        """Logs in a user by verifying the username and password"""
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
    

    def add_fav_recipe(self, user_id, title, url):
        """Adds a recipe to a user's favorite list"""
        data = self.recipe_manipulation.read_file()
        for recipe_id, recipe_data in data.items():
            if recipe_data['title'] == title:
                if user_id not in recipe_data['users']:
                    recipe_data['users'].append(user_id)
                self.recipe_manipulation.write_file(data)
                break
        else:
            id = str(uuid.uuid4())
            recipe = Recipe(id, title, url, [user_id])
            self.recipe_manipulation.add_object(recipe)


    def get_fav_recipes(self, user_id):
        """Retrieves user's favorite recipes"""
        data = self.recipe_manipulation.read_file()
        fav_list = []
        for recipe in data:
            if user_id in data[recipe]['users']:
                recipe_obj = self.recipe_manipulation.get_recipe_object(recipe)
                fav_list.append(recipe_obj)
        return fav_list
        
    
    def search_recipes(self, ingridients):
        """Searches for recipes based on the ingridients provided by the user"""
        url = api_edamam.get_recipe_url(ingridients)
        data = api_edamam.api_response(url)
        recipe_data = api_edamam.extract_recipe_data(data)
        return recipe_data
