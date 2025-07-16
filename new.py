import os, time, json, requests
from datetime import datetime, timedelta

APP_ID = os.getenv("MATHPIX_APP_ID")
APP_KEY = os.getenv("MATHPIX_APP_KEY")
if not APP_ID or not APP_KEY:
    raise RuntimeError("Set MATHPIX_APP_ID and MATHPIX_APP_KEY")

BASE_URL = "https://api.mathpix.com/v3/pdf"
QUERY_URL="https://api.mathpix.com/v3/pdf-results"
HEADERS = {"app_id": APP_ID, "app_key": APP_KEY}



# Submit PDF
options = {"conversion_formats": {"md": True}}
with open("TRAFICOM.pdf","rb") as f:
    resp = requests.post(BASE_URL, headers=HEADERS,
                         data={"options_json": json.dumps(options)},
                         files={"file": f})
resp.raise_for_status()
pdf_id = resp.json().get("pdf_id")
print("Submitted, pdf_id =", pdf_id)
time.sleep(2)

# Poll
status_url = f"https://api.mathpix.com/v3/converter/{pdf_id}"
while True:
    
    resp = requests.get(status_url, headers=HEADERS)
    print(resp)
    if resp.status_code != 200:
        print(resp.status_code)
        time.sleep(2); print(".", end="", flush=True); continue
    status = resp.json().get("status")
    print("\nStatus =", status)
    if status == "completed": break
    if status == "error": raise RuntimeError("OCR failed")
    time.sleep(2)


#print("Saved Markdown to",out )
FORMATT=".lines.json"
url = "https://api.mathpix.com/v3/pdf/" + pdf_id+ FORMATT
response = requests.get(url, headers=HEADERS)
with open(pdf_id + FORMATT, "w") as f:
    f.write(response.text)