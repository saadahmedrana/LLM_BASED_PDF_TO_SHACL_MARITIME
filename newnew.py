import os, time, json, requests, zipfile

APP_ID  = os.getenv("MATHPIX_APP_ID")
APP_KEY = os.getenv("MATHPIX_APP_KEY")
if not APP_ID or not APP_KEY:
    raise RuntimeError("Set MATHPIX_APP_ID and MATHPIX_APP_KEY")

BASE_URL  = "https://api.mathpix.com/v3/pdf"
HEADERS   = {"app_id": APP_ID, "app_key": APP_KEY}

# 1) Submit PDF with conversion_formats for md.zip and tex.zip
options = {
    "conversion_formats": {
        "md.zip": True,
        "tex.zip": True,
        
    }
}

with open("test_image.pdf","rb") as f:
    resp = requests.post(
        BASE_URL,
        headers=HEADERS,
        data={"options_json": json.dumps(options)},
        files={"file": f}
    )
resp.raise_for_status()
pdf_id = resp.json()["pdf_id"]
print("Submitted, pdf_id =", pdf_id)

# 2) Poll for completion
status_url = f"{BASE_URL}/{pdf_id}/status"
while True:
    r = requests.get(status_url, headers=HEADERS)
    r.raise_for_status()
    status = r.json().get("status")
    print("Status:", status)
    if status == "completed":
        break
    if status == "failed":
        raise RuntimeError("Mathpix OCR failed")
    time.sleep(5)

# 3) Download the two ZIP archives
for suffix in ("md.zip", "tex.zip"):
    url = f"{BASE_URL}/{pdf_id}.{suffix}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    out = f"{pdf_id}.{suffix}"
    with open(out, "wb") as f:
        f.write(r.content)
    print(f" Saved {out}")

# 4) Download the lines.json and then zip it locally
lines_url = f"{BASE_URL}/{pdf_id}.lines.json"
r = requests.get(lines_url, headers=HEADERS)
r.raise_for_status()
json_name = f"{pdf_id}.lines.json"
with open(json_name, "w", encoding="utf-8") as f:
    f.write(r.text)
print(" Saved", json_name)

# zip it yourself
zip_name = f"{pdf_id}.lines.zip"
with zipfile.ZipFile(zip_name, "w", compression=zipfile.ZIP_DEFLATED) as zp:
    zp.write(json_name, arcname=os.path.basename(json_name))
print(" Created", zip_name)
