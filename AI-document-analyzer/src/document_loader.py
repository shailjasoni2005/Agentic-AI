from pathlib import Path

from pypdf import PdfReader


def load_document(file_path: str) -> str|None:
    print(file_path)
    path = Path(file_path)

    if not path.exists():
        print(f"Error: The file {file_path} was not found")
        return None

    if not path.is_file():
        print(f"This {file_path} is not a file.")
        return None

    extension = path.suffix.lower()

    try:
        if extension == ".txt":
            with path.open("r",encoding="utf-8") as file:
                content = file.read()
                return content 

        elif extension == ".pdf":
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""

            return text

        else:
            print(f"Error: Unsupported file type {extension}.")
            return None

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None

    except PermissionError:
        print(f"Error: Permission denied when reading {file_path}")
        return None

    except UnicodeDecodeError:
        print(f"Error: The file {file_path} does not contain valid UTF-8 text.")
        return None