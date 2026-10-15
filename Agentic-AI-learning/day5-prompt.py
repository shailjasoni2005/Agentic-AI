import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field, ValidationError

load_dotenv()

base_url = os.getenv("url")
api_key = os.getenv("API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

class DocumentAnalysis(BaseModel):
    document_type: str
    amount: float = Field(ge=0)
    summary: str
    needs_review: bool 

document_text = """
Invoice #INV-101
Vendor: ABC Technologies
Total amount: INR 5000
Payment due: 20 October 2026
"""

user_prompt = f""" Analyze this document: {document_text}
Extract its information and return a JSON onject containing:
- document_type: string
- amount: non-negative number
- summary: string
- needs_review: boolean

Use only information supported by the document. If th eamount is missing or uncertain, 
set need_review to true.
Return JSON only, without markdown fences.
"""


try:
    response = client.chat.completions.create(
    model="grok-4",
    messages=[
        {"role": "system", "content":"You extract document information accurately"},
        {"role":"user", "content":user_prompt}
        ],
        temperature=0
    )
    raw_response = response.choices[0].message.content
    print("Raw LLM response:", raw_response)

    data = json.loads(raw_response)
    result= DocumentAnalysis.model_validate(data)

    print("\n validated result: ")

    print(result.model_dump_json(indent=2))

except json.JSONDecodeError as error:
    print("The LLM did not return valid JSON: ", error)

except ValidationError as error:
    print("The JSON did not match our model:", error)

except Exception as error:  # noqa: BLE001
    print("LLM API or other error:", error)


