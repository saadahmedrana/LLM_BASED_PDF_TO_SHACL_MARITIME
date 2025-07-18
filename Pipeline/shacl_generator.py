# Step 1: Import the necessary tools
import google.generativeai as genai
import os
from dotenv import load_dotenv

def load_text_file(file_path: str) -> str:
    """Reads the content of a text file."""
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'")
        return None
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

    # Step 3: Define file paths
    PDF_FILE_PATH = "TRAFICOM.pdf"
    FEW_SHOT_EXAMPLES_PATH = "few_shot.txt"

    # Step 4: Get interactive input from the user
    # THIS IS THE NEW INTERACTIVE PART
    user_request = input("▶ Please enter your request (e.g., 'Generate SHACL for the user address section'):\n")
    if not user_request:
        print("Error: No request entered. Exiting.")
        return

    # Step 5: Load the few-shot examples from the external file
    few_shot_examples = load_text_file(few_shot.txt)
    if not few_shot_examples:
        return # Stop if the examples file couldn't be loaded

    # Step 6: Construct the final dynamic prompt
    final_prompt = f"""
You are an expert system that generates W3C SHACL code from technical specifications.
Your task is to analyze the provided PDF file and follow the user's instruction precisely. The output must ONLY be the SHACL code itself, enclosed in a turtle code block.

---
**USER'S INSTRUCTION:**
{user_request}
---
**HIGH-QUALITY EXAMPLES FOR GUIDANCE:**
{few_shot_examples}
---

**Generated SHACL (based only on the user's instruction and the PDF content):**
"""

    # Step 7: Upload the PDF to Google
    if not os.path.exists(PDF_FILE_PATH):
        print(f"Error: PDF file not found at '{PDF_FILE_PATH}'")
        return
        
    print(f"\nUploading {PDF_FILE_PATH} to Google... This might take a moment.")
    uploaded_file = genai.upload_file(path=PDF_FILE_PATH, display_name="TRAFICOM Specification")
    print(f"File uploaded successfully: {uploaded_file.name}")

    # Step 8: Ask the Gemini model to generate the code
    print("\n🤖 Asking Gemini to generate the SHACL code...")
    model = genai.GenerativeModel(model_name='models/gemini-1.5-pro-latest')
    response = model.generate_content([final_prompt, uploaded_file])

    # Step 9: Print the final result!
    print("\n--- YAYYY! Generated SHACL Output ---")
    print(response.text)
    print("---------------------------------------\n")

    # Step 10: Clean up and delete the file from Google's server
    print(f"Cleaning up... Deleting {uploaded_file.name} from the server.")
    genai.delete_file(uploaded_file.name)
    print(" Done!")

if __name__ == "__main__":
    main()