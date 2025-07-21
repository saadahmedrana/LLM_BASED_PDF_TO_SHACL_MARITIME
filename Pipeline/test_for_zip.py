import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

def load_text_file(file_path: str) -> str:
    """Reads the content of a text file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
    except Exception as e:
        print(f"Error reading file: {e}")
    return None

def main():
    # Step 2: Load secret API key
    load_dotenv()
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not found in .env file.")
        return
    genai.configure(api_key=GOOGLE_API_KEY)

    # Step 3: Define file path
    JSON_FILE_PATH = "newttest.json"

    # Step 4: Load the JSON text
    json_text = load_text_file(JSON_FILE_PATH)
    if not json_text:
        return

    # Step 5: Construct the system prompt
    system_message = json.dumps({
        "role": "system",
        "content": (
            "You are an expert assistant that reads structured JSON content and converts it to "
            "LaTeX format, preserving the content exactly as found in the JSON. When reading the JSON "
            "file:\n\n"
            "- For textual fields, include the text directly as-is in the LaTeX output.\n"
            "- If a field contains an image reference (e.g., Markdown syntax like `![](https://.../image.jpg)`), regardless "
            "of the filename or URL structure:\n"
            "  1. Fetch and analyze the image.\n"
            "  2. Summarize its content in plain, simple English.\n"
            "  3. Insert the summary text in place of the image in the LaTeX document.\n"
            "- Preserve the original JSON key order and nesting structure.\n"
            "- Produce a single, fully compilable LaTeX document, including necessary preamble and package imports "
            "(for example, `\\usepackage{graphicx}` even if images are summarized as text).\n\n"
            "The output must be exactly one LaTeX file that reflects the entire JSON content, with image summaries substituted "
            "for any image references."
        )
    })

    # Step 6: Send JSON text inline with system prompt to Gemini
    print("\nAsking Gemini to convert JSON to LaTeX…")
    model = genai.GenerativeModel(model_name="models/gemini-2.5-pro")
    response = model.generate_content([system_message, json_text])

    # Step 7: Print the result
    print("\n--- Output LaTeX ---")
    print(response.text)
    print("--------------------\n")

if __name__ == "__main__":
    main()
