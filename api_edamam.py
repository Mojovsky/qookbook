import requests
import os
from dotenv import load_dotenv

load_dotenv()

class InvalidIngredients(Exception):
    """Exception raised for invalid ingredients."""
    def __init__(self, message="No match found. Please try again with different ingredients."):
        self.message = message
        super().__init__(self.message)



def get_recipe_url(ingridients):
    """This function returns the url for the recipe API. It takes a list of ingredients as input and returns the url."""
    app_id = os.getenv("app_id")
    app_key = os.getenv("app_key")
    base_url = "https://api.edamam.com/api/recipes/v2"
    if isinstance(ingridients, (list, tuple)):
        query = "%2C%20".join(ingridients)
    else:
        query = ingridients
    url = f"{base_url}?type=public&q={query}&app_id={app_id}&app_key={app_key}"
    return url


def api_response(url):
    """This function returns the response from the API. It takes the url as input and returns the response."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")


def extract_recipe_data(data):
    """This function extracts the recipe data from the API response. It takes the response data as input and returns the extracted recipe data."""
    if data["count"] == 0:
        raise InvalidIngredients()
    extracted_recipe_data = []
    for recipe in data["hits"]:
        extracted_recipe_data.append(
            {
                "title": recipe["recipe"]["label"],
                "url": recipe["recipe"]["url"],
            }
        )
    return extracted_recipe_data