import google.generativeai as genai
import os
from dotenv import load_dotenv


def main():
    # Load secret API key
    load_dotenv()
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY not found in .env file.")
        return
    genai.configure(api_key=GOOGLE_API_KEY)

    # Directly specify the image URI
    uri = "https://cdn.mathpix.com/cropped/2025_07_16_9a385908f6e70ba0f1fdg-19.jpg?height=254&width=173&top_left_y=795&top_left_x=531"
    image_markdown = f"![]({uri})"

    # Construct the system and user messages using correct Gemini content format
    system_message = {
        "role": "system",
        "parts": [
            {
                "text": (
                    "You are an expert image analyst. The user will provide a URI to an image using Markdown format.\n\n"
                    "Your task is to:\n"
                    "1. Fetch the image at the URI.\n"
                    "2. Describe exactly what you see: all objects, text, shapes, figures, colors, spatial relationships, labels, and annotations.\n"
                    "3. After the detailed description, provide a concise summary of the image's overall content.\n"
                    "If the image cannot be accessed or viewed, state that clearly."
                )
            }
        ]
    }

    user_message = {
        "role": "user",
        "parts": [
            {"text": image_markdown}
        ]
    }

    # Send to Gemini
    print("\nAsking Gemini to analyze the image…")
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")
    response = model.generate_content([system_message, user_message])

    # Output the result
    print("\n--- Image Analysis ---")
    print(response.text)
    print("----------------------\n")


if __name__ == "__main__":
    main()
