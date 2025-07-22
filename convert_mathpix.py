import os, time, json, requests
from datetime import datetime, timedelta

# ✅ Set your Mathpix credentials as environment variables
APP_ID = os.getenv("MATHPIX_APP_ID")
APP_KEY = os.getenv("MATHPIX_APP_KEY")
if not APP_ID or not APP_KEY:
    raise RuntimeError("Set MATHPIX_APP_ID and MATHPIX_APP_KEY")

BASE_URL = "https://api.mathpix.com/v3/pdf"
QUERY_URL = "https://api.mathpix.com/v3/pdf-results"
HEADERS = {"app_id": APP_ID, "app_key": APP_KEY}

# ✅ Conversion options: request both mmd.zip and md.zip for local image links
options = {
    "conversion_formats": {
        "mmd.zip": True,
        "md.zip": True
    }
}

# ✅ Submit PDF
pdf_path = "TRAFICOM.pdf"  # Change this to your file path
with open(pdf_path, "rb") as f:
    resp = requests.post(BASE_URL, headers=HEADERS,
                         data={"options_json": json.dumps(options)},
                         files={"file": f})
resp.raise_for_status()
pdf_id = resp.json().get("pdf_id")
print("Submitted, pdf_id =", pdf_id)

# ✅ Poll for processing completion
status_url = f"{QUERY_URL}/{pdf_id}/status"
while True:
    resp = requests.get(status_url, headers=HEADERS)
    if resp.status_code != 200 or not resp.text.strip():
        time.sleep(5); print(".", end="", flush=True); continue
    status = resp.json().get("status")
    print("\nStatus =", status)
    if status == "done": break
    if status == "failed":
        raise RuntimeError("OCR failed")
    time.sleep(5)

# ✅ Download mmd.zip
mmd_zip_url = f"{BASE_URL}/{pdf_id}.mmd.zip"
resp = requests.get(mmd_zip_url, headers=HEADERS)
resp.raise_for_status()
with open(f"{pdf_id}.mmd.zip", "wb") as f:
    f.write(resp.content)
print(f"Saved {pdf_id}.mmd.zip")

# ✅ Download md.zip
md_zip_url = f"{BASE_URL}/{pdf_id}.md.zip"
resp = requests.get(md_zip_url, headers=HEADERS)
resp.raise_for_status()
with open(f"{pdf_id}.md.zip", "wb") as f:
    f.write(resp.content)
print(f"Saved {pdf_id}.md.zip")
