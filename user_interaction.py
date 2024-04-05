import api_edamam
from data_manipulation import User, Recipe, DataManipulation



def create_user(username, email, password):
    data = DataManipulation("data/users.json")
    user = User(username, email, password)
    data.add_object(user)
    return user


def login(username, password):
    data = DataManipulation("data/users.json")
    user = data.get_user_object(username)
    if user.verify_password(password):
        return user
    else:
        return None


def search_recipes(ingridients):
    url = api_edamam.get_recipe_url(ingridients)
    data = api_edamam.api_response(url)
    recipe_data = api_edamam.extract_recipe_data(data)
    return recipe_data


def display_recipes(recipe_data):
    for i, recipe in enumerate(recipe_data):
        return recipe['title'], recipe['url'], recipe['image']


def add_fav_recipe(username, recipe, tags=None):
    data = DataManipulation("data/recipes.json")
    recipe = Recipe(**recipe)
    recipe.users.append(username)
    if tags: recipe.tags.extend(tags)
    data.add_object(recipe)


def add_custom_tags(user_obj, recipe_obj, tags):
    recipe_data = DataManipulation("data/recipes.json")
    user_data = DataManipulation("data/users.json")
    user_obj.tags.extend(tags)
    recipe_obj.tags.extend(tags)
    user_data.write_file(user_obj.to_json())
    recipe_data.write_file(recipe_obj.to_json())
