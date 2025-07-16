import os
import json
import time
import requests
from dotenv import load_dotenv

# --- 1. SETUP ---
# Load environment variables from .env file
load_dotenv()

# Get credentials
app_id = os.getenv("MATHPIX_APP_ID")
app_key = os.getenv("MATHPIX_APP_KEY")
if not app_id or not app_key:
    raise RuntimeError("Mathpix APP_ID and APP_KEY must be set in your .env file")

# Define file paths and API endpoint
pdf_path = "page9.pdf"
base_filename, _ = os.path.splitext(pdf_path)
api_url = "https://api.mathpix.com/v3/pdf"

# --- 2. STEP 1: UPLOAD THE PDF FILE ---
print(f"Submitting '{pdf_path}' for processing...")

# Define the conversion options as a Python dictionary
options = {
    "conversion_formats": {
        "lines.json": True,
        "md": True
    }
}

# The headers contain your authentication keys
headers = {
    "app_id": app_id,
    "app_key": app_key
}

# The `data` payload contains the options, converted to a JSON string
# This is exactly as specified in the documentation.
data = {
    "options_json": json.dumps(options)
}

# Open the file in binary mode and send the request
try:
    with open(pdf_path, "rb") as f:
        # The `files` parameter handles the multipart/form-data encoding
        files = {"file": f}
        response = requests.post(api_url, headers=headers, data=data, files=files)
    
    # Ensure the request was successful
    response.raise_for_status()
    
    # Extract the pdf_id from the response
    response_data = response.json()
    if 'pdf_id' in response_data:
        pdf_id = response_data['pdf_id']
        print(f"✅ PDF submitted successfully. Job ID: {pdf_id}")
    else:
        # Handle cases where submission fails but doesn't raise a HTTP error
        error_message = response_data.get('error', 'Unknown error during submission.')
        raise RuntimeError(f"API Error: {error_message}")

except requests.exceptions.RequestException as e:
    print(f"❌ HTTP Error during submission: {e}")
    # Print the response text for more details if available
    if 'response' in locals() and response.text:
        print(f"Response Body: {response.text}")
    exit()
except FileNotFoundError:
    print(f"❌ Error: The file '{pdf_path}' was not found.")
    exit()
except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
    exit()


# --- 3. STEP 2: POLL FOR RESULTS ---
print("Waiting for processing to complete...")
status_url = f"{api_url}/{pdf_id}"
polling_timeout_seconds = 180
start_time = time.time()

while time.time() - start_time < polling_timeout_seconds:
    try:
        response = requests.get(status_url, headers=headers)
        response.raise_for_status()
        
        result_data = response.json()
        status = result_data.get('status')
        
        if status == 'completed':
            print("✅ Processing complete!")
            # Save the results
            json_output_path = f"{base_filename}.json"
            md_output_path = f"{base_filename}.md"

            # Save the .json file
            with open(json_output_path, "w", encoding="utf-8") as f:
                json.dump(result_data['lines.json'], f, ensure_ascii=False, indent=2)
            print(f"Saved structured JSON to {json_output_path}")

            # Save the .md file
            with open(md_output_path, "w", encoding="utf-8") as f:
                f.write(result_data['md'])
            print(f"Saved Markdown to {md_output_path}")
            
            exit() # Exit successfully
            
        elif status == 'error':
            error_info = result_data.get('error_info', {}).get('message', 'No error details provided.')
            print(f"❌ Processing failed with error: {error_info}")
            exit()
            
        else:
            print(f"Current status: '{status}'. Waiting...")
            time.sleep(5) # Wait for 5 seconds before polling again

    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP Error during polling: {e}")
        time.sleep(5) # Wait before retrying

print(f"❌ Timed out after {polling_timeout_seconds} seconds. Processing did not complete.")