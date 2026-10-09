# import tiktoken

# texts = [
#     "hello",
#     "hello, how are you?",
#     """
#     I am building an AI document analyzer. It reads documents and generates summaries.
#     """
# ]

# encoding = tiktoken.encoding_for_model("gpt-4o-mini")
# for text in texts:
#     tokens = encoding.encode(text)
#     print("\nText: ", repr(text))
#     print("Token count: ", len( tokens))
#     print("Token IDs: ", tokens)



#Without os, your Python code mostly works with variables and functions. With os, it can interact with files, folders, paths, and environment variables.
     #dotenv -> package -> The purpose of this package is to read values from a .env file and make them available to your program as environment variables.
     #The OpenAI SDK is the Python package that lets your Python code communicate with OpenAI models.
     
import os
from dotenv import load_dotenv
from openai import OpenAI 

load_dotenv()

base_url = os.getenv("url")
api_key = os.getenv("API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

response = client.chat.completions.create(
    model="grok-4",
    messages=[
        {"role": "user", "content":"Explain what an API is in two bullet points."}
    ]
)
print(response.choices[0].message.content)