import requests
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

USERS_API = "https://jsonplaceholder.typicode.com/users"
POSTS_API = "https://jsonplaceholder.typicode.com/posts"

def fetch_data(url):
    """
    Generic function to fetch data from a given URL.
    Returns JSON data if successful, None otherwise.
    """
    try:
        logging.info(f"Fetching data from {url}")
        response = requests.get(url)
        response.raise_for_status()
        logging.info(f"Data fetched successfully from {url}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return None

def get_users():
    """
    Fetches user data from USERS_API.
    """
    return fetch_data(USERS_API)

def get_posts():
    """
    Fetches post data from POSTS_API.
    """
    return fetch_data(POSTS_API)

# Optional: if you want to run this as a standalone test
if __name__ == "__main__":
    users = get_users()
    posts = get_posts()
    print(f"Fetched {len(users)} users and {len(posts)} posts.")
    print(posts)