import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is not set in the .env file.")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

# Path to the ZIP file (contains Markdown + images/ folder)
ZIP_FILE_PATH = "2025_07_17_c228c7dcda39f9eee55eg.md.zip"

if not os.path.exists(ZIP_FILE_PATH):
    raise FileNotFoundError(f"ZIP file not found: {ZIP_FILE_PATH}")

# Upload ZIP archive (Gemini treats this as a file bundle)
print(f"Uploading ZIP file: {ZIP_FILE_PATH}")
uploaded_zip = genai.upload_file(path=ZIP_FILE_PATH, display_name="Spec Bundle")
print("Uploaded successfully:", uploaded_zip.name)

# Instruction to let the model understand embedded image paths
user_prompt = """
You are a system that reads teh pdf and images and explains them as you see them . The text as it is and summary of what you saw in image.
"""

# Run Gemini model
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
response = model.generate_content([user_prompt, uploaded_zip])

print("\n--- SHACL Output ---\n")
print(response.text)
print("\n----------DONE SIRE------------\n")
