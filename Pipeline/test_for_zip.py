import google.generativeai as genai
import os
from dotenv import load_dotenv
from pathlib import Path


def upload_files_and_prepare_prompt(md_path: str, image_dir: str, section_number: str, shacl_task: str) -> tuple:
    """Uploads the markdown and image files, and prepares the full prompt."""

    print("🔼 Uploading markdown...")
    uploaded_md = genai.upload_file(path=md_path, display_name="PDF Markdown")
    print(f"✅ Uploaded markdown: {uploaded_md.name}")

    image_files = list(Path(image_dir).glob("*.png"))
    uploaded_images = []

    for img_path in image_files:
        print(f"🔼 Uploading image: {img_path.name}")
        uploaded = genai.upload_file(path=str(img_path), display_name=img_path.name)
        uploaded_images.append(uploaded)
    print(f"✅ Uploaded {len(uploaded_images)} images.")

        # Step 5: Load the few-shot examples from the external file
    few_shot_examples = load_text_file(FEW_SHOT_EXAMPLES_PATH)
    if not few_shot_examples:
        return # Stop if the examples file couldn't be loaded

    # Prepare your final instruction prompt
    prompt = f"""
You are an expert in W3C SHACL conversion from natural language / markdown files. 
You are provided with a markdown file derived from a regulation document, which includes image references like ![desc](images/example.png).
Each image mentioned is provided separately and corresponds by filename.

You have been provided with a few examples in {few_shot_examples}

Your task is:
1. Parse the markdown document.
2. Automatically resolve each image reference with the uploaded image file.
3. Interpret the combined context to extract regulatory constraints.
4. {shacl_task} ONLY for section {section_number}.
5. Output only the SHACL code in a ```turtle block```.
"""

    parts = [
        genai.types.Part.from_text(prompt),
        genai.types.Part.from_file(uploaded_md.name),
    ]
    for image_file in uploaded_images:
        parts.append(genai.types.Part.from_file(image_file.name))

    return parts


def main():
    load_dotenv()
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY not found.")
    genai.configure(api_key=GOOGLE_API_KEY)

    # --- Define file paths ---
    markdown_file = "2025_07_17_c228c7dcda39f9eee55eg.zip"  # your markdown file
    images_folder = "images"  # folder containing all referenced images

    # --- Define prompt/task ---
    section = "3"
    shacl_instruction = "Generate SHACL constraints"

    # Upload and construct content
    parts = upload_files_and_prepare_prompt(markdown_file, images_folder, section, shacl_instruction)

    # Use Gemini 2.5 Pro
    model = genai.GenerativeModel("models/gemini-2.5-pro-latest")
    print(" Generating SHACL output...")
    response = model.generate_content(parts)

    print("\n--- GENERATED SHACL ---")
    print(response.text)
    print("---------DONE SIRE---------------")


if __name__ == "__main__":
    main()
