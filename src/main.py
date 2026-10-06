# from src.tools.api_client import get_todo
from src.tools.api_client import post_todo  # noqa: I001
from src.tools.api_client import http_header

title_x = input("Enter TODO title: ")
id_x = input("Enter TODO ID: ")
dict = {
    "title" : title_x,
    "id" : id_x
}

# todo = get_todo(user_id) 
todo,status_code = post_todo(dict)
print("status code: ",status_code)
print("Response: ", todo)

http_res = http_header(dict)