import json
import os

from dotenv import load_dotenv
from openai import (
    APIConnectionError,
    APIError,
    APIStatusError,
    AuthenticationError,
    OpenAI,
    RateLimitError,
)

load_dotenv()

base_url = os.getenv("url")
api_key = os.getenv("API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
    max_retries=2,
    timeout=30.0
)

def ask_ai(prompt):
    try:
        print("\nAI is generating:\n")

        stream = client.chat.completions.create(
            model="grok-4",
            messages=[
                {"role":"system",
                "content":"you are a helpful, concise AI tutor."},
                {"role":"user", "content":prompt}
            ],
            temperature=0.2,
            max_tokens=200,
            stream=True,
            stream_options={"include_usage": True},
        )

        answer_parts = []
        usage = None #token

        for chunk in stream:
            if chunk.usage is not None:
                usage=chunk.usage
            if not chunk.choices:
                continue

            text = chunk.choices[0].delta.content

            if text is not None:
                print(text, end="", flush=True)
                answer_parts.append(text)

            print("\n\n--- TOKEN USAGE---")
            if usage is not None:
                print("\nInput tokens: ", usage.prompt_tokens) #tokens consumed by the input.
                print("\nOutput tokens: ",usage.completion_tokens) #tokens generated in response.
                print("\nTotal tokens: ",usage.total_tokens)      
            else:
                print("Token usage was not returned.")       

        return "".join(answer_parts),usage

    except AuthenticationError:
        print("\nInvalid API key. Check your .env file.")
        return None

    except RateLimitError as error:
        print("\nRate limit or quota issue:",error)
        return None

    except APIConnectionError:
        print("\nConnection failed.")

    except APIStatusError as error:
        print("\nAPI returned status: ", error.status_code)
        
    except APIError as error:
        print("\nAPI error:", error)

    return None,None

def ask_ai_json(prompt):
    try:
        response=client.chat.completions.create(
            model="grok-4",
            messages=[
                {
                    "role":"system",
                    "content": ("You are a helpgul AI assistant. " 
                    "Return your answer as valid JSON only")
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ],
            temperature=0.2,
            max_tokens=300,
            response_format={"type":"json_object"}
        )
        #get the ai's response as json text
        answer_text = response.choices[0].message.content
        #convert json text into a python dictionary
        data = json.loads(answer_text)
        print("\n---Structures json response---")
        print(json.dumps(data,indent=4))
        print("\n--ACCESSING INDIVIDUAL VALUES---")
        print("topic:",data["topic"])
        print("Difficulty:",data["difficulty"])
        print("\nsteps:")
        for step in data["steps"]:
            print("-",step)
        return data

    except json.JSONDecodeError:
        print("the AI response could not be parsed as json")
    except APIError as error:
        print("OpenAI API error: ",error)

    return None

result = ask_ai_json("Explain how an AI agent works."
"Return a JSON object with these keys: "
"topic (string), steps (array of 4 strings), "
"and difficulty (string)."
)
