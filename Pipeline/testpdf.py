import google.generativeai as genai
import os
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

    # Step 3: Define PDF path and prompt
    PDF_FILE_PATH = "page9.pdf"
    final_prompt = r"""
You are an expert PDF reader and LaTeX formatter. When processing each page of a technical PDF (with text, math, tables, and figures), follow these rules:

1. **Plain Text & Sections**  
   - Extract all headers, paragraphs, and labels verbatim, preserving their hierarchy (e.g. \section, \subsection).

2. **Mathematical Expressions**  
   - Whenever you encounter a formula or equation, convert it into proper LaTeX math mode (e.g. use `\\[ ... \\]` or `$$ ... $$` for display equations, and `$ ... $` for inline).

3. **Tables**  
   - Recreate any table using a LaTeX `tabular` environment.
   - Preserve row and column structure, cell contents, and any captions.

4. **Figures & Diagrams**  
   - For every figure (images, plots, diagrams), do **not** embed the graphic itself. Instead:
     - Describe the figure in rich detail: list all visible elements (shapes, lines, colors, text labels) and their spatial relationships.
     - Explain how the figure relates to its surrounding text or section.
     - Provide a brief "Figure Caption" in plain English summarizing its purpose.

5. **Consistency & Completeness**  
   - Keep the original page order.
   - Include any footnotes, captions, or annotations exactly as written.
   - Wrap the entire page in a minimal LaTeX document structure (preamble with `\\documentclass{article}`, `\\usepackage{graphicx}`, etc.) so it compiles standalone.

**Output**:  
Return one self‑contained LaTeX document per page processed. Each document should compile cleanly under `pdflatex` and mirror the original PDF’s content, with equations and tables in real LaTeX, and detailed, textual figure descriptions.
"""

    # Step 4: Upload the PDF to Google
    if not os.path.exists(PDF_FILE_PATH):
        print(f"Error: PDF file not found at '{PDF_FILE_PATH}'")
        return
    print(f"\nUploading {PDF_FILE_PATH} to Google... This might take a moment.")
    uploaded_file = genai.upload_file(path=PDF_FILE_PATH, display_name="Technical PDF")
    print(f"File uploaded successfully: {uploaded_file.name}")

    # Step 5: Ask the Gemini model to generate the LaTeX
    print("\nAsking Gemini to convert PDF to LaTeX…")
    model = genai.GenerativeModel(model_name='models/gemini-2.5-pro')
    response = model.generate_content([
        final_prompt,
        {
            "file_data": uploaded_file
        }
    ])

    # Step 6: Print the result
    print("\n--- Output LaTeX ---")
    print(response.text)
    print("--------------------\n")

    # Step 7: Clean up
    print(f"Cleaning up... Deleting {uploaded_file.name} from the server.")
    genai.delete_file(uploaded_file.name)
    print("Done!")

if __name__ == "__main__":
    main()

