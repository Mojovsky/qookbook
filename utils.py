import requests

def shorten_url(url):
    response = requests.get(f'http://tinyurl.com/api-create.php?url={url}')
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: {response.status_code}")
        return url