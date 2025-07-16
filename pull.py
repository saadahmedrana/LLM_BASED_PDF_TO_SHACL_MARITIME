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
    "page":2,
    "per_page": 100,
}
pdf_id = "2025_07_16_9a385908f6e70ba0f1fdg"


resp = requests.get(QUERY_URL, headers=HEADERS, params=params)
resp.raise_for_status()

data = resp.json()
for pdf in data.get("pdfs", []):
    print(pdf["id"])
options = {"conversion_formats": {"md": True}}

#print("Saved Markdown to",out )


FORMATT=".lines.json"
url = "https://api.mathpix.com/v3/pdf/" + pdf_id+ FORMATT
response = requests.get(url, headers=HEADERS)
with open(pdf_id + FORMATT, "w", encoding="utf-8") as f:
    f.write(response.text)
