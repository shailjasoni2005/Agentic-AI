import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ValidationError
from src.document_loader import load_document

load_dotenv()

base_url = os.getenv("url")
api_key = os.getenv("API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

class DocumentAnalysis(BaseModel):
    document_type: str 
    summary: str 
    key_details: list[str]
    suggestions: list[str]


def analyze_document(text, document_type):
    prompts = {
        "resume": """ analyze this resume. 
        Extract skills, education, work experience, and achievements.
        suggest improvements to make the resume stronger.""",

        "invoice": """ Analyze this invoice. 
        Extract the invoice number, vendor name, invoice date, due date, subtotal, tax, 
        and total amount.
        Identify missing or unclear information.""",

        "report": """ Analyze this report. 
        Explain its purpose, summarize key findings, identify important conclusions, 
        and list recommendations."""
    }

    instructions = prompts[document_type]

    response = client.chat.completions.create(
        model="grok-4",
        messages=[
            {"role": "system", "content": ("You are an AI document analysis assistant. "
            "Analyze documents accurately. Do not invent facts that are not present in the document.")
            },
            {"role": "user", "content": f""" Analyze this {document_type}.
            Instruction: {instructions}
            Document content: {text}

            Return a JSON object with exactly thse fields:
            - document_type: string
            -summary: string
            -key_details: array of strings
            -suggestions: array of strings
            Set document_type to "{document_type}".
            Return JSON only, without any extra text.
            """}
        ],
        temperature = 0.2
    )
    response_text = response.choices[0].message.content

    try:
        data = json.loads(response_text)
        analysis = DocumentAnalysis.model_validate(data)
        return analysis

    except (json.JSONDecodeError, ValidationError) as error:
        raise ValueError(f"The AI returned an invalid analysis format: {error}") from error

def main():
    print("\n=== AI Document Analyzer===")
    file_path = "data/sample_resume.pdf"

    print("\nselect document type: ")
    print("1. Resume")
    print("1. invoice")
    print("1. report")

    choice = input("Enter your choice (1-3): ").strip()
    document_types = {
        "1": "resume",
        "2": "invoice",
        "3": "report"
    }

    if choice not in document_types:
        print("Invalid choice. Please select 1,2 or 3.")
        return

    document_type = document_types[choice]

    try:
        text = load_document(file_path)
        if not text or not text.strip():
            print("The document is empty.")
            return 
        
        print("Document loaded successfully!")

        print("\nAnalyzing document...\n")
        result = analyze_document(text, document_type)

        print("===Document analysis===\n")
        print(f"Document Type: {result.document_type}")
        print(f"\nSummary:\n{result.summary}")
        print("\nKey Details:")
        for detail in result.key_details:
            print(f"- {detail}")

        print("\nSuggestions:")
        for suggestion in result.suggestions:
            print(f"- {suggestion}")


    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as error:  # noqa: BLE001
        print(f"An error occured: {error}")

if __name__ == "__main__":
    main()