import requests  # noqa: I001
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

headers = {
    "Authorization": f"Bearer{api_key}",
    "content-type": "application/json"
}

def get_todo(todo_id):
    url = f"https://jsonplaceholder.typicode.com/todos/{todo_id}"  #we are using  JSONplaceholder, a public API for testing and learning 
    response = requests.get(url)

    if response.status_code == 200: 
        return response.json()  #return the JSON response if the request was successful
    elif response.status_code == 404:
        print("TODO not found for this ID")
    else:
        print(f"Request failed with status code {response.status_code}") 
    return response.json()

def post_todo(data):
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.post(url,json=data)

    if response.status_code == 201: 
        return response.json(),response.status_code  #return the JSON response if the request was successful
    elif response.status_code == 404:
        print("TODO not found for this ID")
    else:
        print(f"Request failed with status code {response.status_code}") 
    return response.json()

def http_header(data):
        url = "https://jsonplaceholder.typicode.com/posts"
        headers = {
        "content-Type": "application/json"
        }
        response = requests.post(
            url,
            json=data,
            headers=headers
        )
        if response.status_code == 201: 
            return response.json(),response.status_code
        else:
            response.raise_for_status()
    



    

