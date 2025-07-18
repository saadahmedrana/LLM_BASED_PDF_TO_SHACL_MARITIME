import os, json
import google.generativeai as genai
from dotenv import load_dotenv

# —— Configuration ——
ZIP_PATH     = "traficom_md_images.zip"
DISPLAY_NAME = "TRAFICOM_MD_Images"
CACHE_FILE   = "gemini_upload_cache.json"

# 1) Load your API key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY in .env")
genai.configure(api_key=API_KEY)

# 2) Retrieve (or upload) and cache the file ID
def get_cached_file_id(zip_path, display_name):
    # load existing cache if present
    if os.path.exists(CACHE_FILE):
        cache = json.load(open(CACHE_FILE))
        if cache.get("zip_path") == zip_path and cache.get("file_id"):
            print("🔁 Reusing cached file ID:", cache["file_id"])
            return cache["file_id"]

    # otherwise upload once
    print("⬆️  Uploading ZIP to Gemini…")
    uploaded = genai.upload_file(path=zip_path, display_name=display_name)
    fid = uploaded.name
    # save to cache
    with open(CACHE_FILE, "w") as f:
        json.dump({"zip_path": zip_path, "file_id": fid}, f)
    print("✅ Uploaded and cached file ID:", fid)
    return fid

file_id = get_cached_file_id(ZIP_PATH, DISPLAY_NAME)

# 3) Build your prompt
prompt = """
You are an expert in translating technical specifications (text, tables, images, math)
into W3C SHACL shapes. The uploaded file contains:
- A Markdown file with LaTeX formulas.
- An images/ folder alongside it.

**USER REQUEST:** Generate ONLY the SHACL Turtle code for Section 3.2.2 “New ships”.
Begin and end your answer with triple-backticks (```turtle …```).
"""

# 4) Invoke Gemini, passing the prompt and the existing file ID
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
response = model.generate_content([prompt, file_id])

# 5) Print out the Turtle
print("\n```turtle")
print(response.text.strip())
print("```")
