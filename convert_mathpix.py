import os, time, json, requests
from datetime import datetime, timedelta

APP_ID = os.getenv("MATHPIX_APP_ID")
APP_KEY = os.getenv("MATHPIX_APP_KEY")
if not APP_ID or not APP_KEY:
    raise RuntimeError("Set MATHPIX_APP_ID and MATHPIX_APP_KEY")

BASE_URL = "https://api.mathpix.com/v3/pdf"
QUERY_URL="https://api.mathpix.com/v3/pdf-results"
HEADERS = {"app_id": APP_ID, "app_key": APP_KEY}
params = {
    "per_page": 50,
    "from_date": (datetime.now() - timedelta(days=1)).isoformat() + "Z"
}


resp = requests.get(QUERY_URL, headers=HEADERS, params=params)
resp.raise_for_status()

data = resp.json()
print(data)
for pdf in data.get("data", []):
    print(pdf["pdf_id"], pdf["status"], pdf["created_at"])
options = {"conversion_formats": {"md": True}}
""" 
# Submit PDF
with open("page9.pdf","rb") as f:
    resp = requests.post(BASE_URL, headers=HEADERS,
                         data={"options_json": json.dumps(options)},
                         files={"file": f})
resp.raise_for_status()
pdf_id = resp.json().get("pdf_id")
print("Submitted, pdf_id =", pdf_id)

# Poll
status_url = f"{QUERY_URL}/{pdf_id}/status"
while True:
    
    resp = requests.get(status_url, headers=HEADERS)
    print(resp)
    if resp.status_code != 200 or not resp.text.strip():
        print(resp.status_code)
        time.sleep(5); print(".", end="", flush=True); continue
    status = resp.json().get("status")
    print("\nStatus =", status)
    if status == "done": break
    if status == "failed": raise RuntimeError("OCR failed")
    time.sleep(5)

# Download only Markdown
url = f"{BASE_URL}/{pdf_id}.md"
r = requests.get(url, headers=HEADERS); r.raise_for_status()
out = f"{pdf_id}.md"
with open(out, "w", encoding="utf-8") as f: f.write(r.text)
print("Saved Markdown to", out)
 """