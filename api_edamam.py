import requests
import os
from dotenv import load_dotenv
from utils import shorten_url

load_dotenv()

class InvalidIngredients(Exception):
    def __init__(self, message="No match found. Please try again with different ingredients."):
        self.message = message
        super().__init__(self.message)



def get_recipe_url(ingridients):
    app_id = os.getenv("app_id")
    app_key = os.getenv("app_key")
    base_url = "https://api.edamam.com/api/recipes/v2"
    query = "%2C%20".join(ingridients)
    url = f"{base_url}?type=public&q={query}&app_id={app_id}&app_key={app_key}"
    return url


def api_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")


def extract_recipe_data(data):
    if data["count"] == 0:
        raise InvalidIngredients()
    extracted_recipe_data = []
    for recipe in data["hits"]:
        extracted_recipe_data.append(
            {
                "title": recipe["recipe"]["label"],
                "url": recipe["recipe"]["url"],
                "image": recipe["recipe"]["image"],
            }
        )
    return extracted_recipe_data