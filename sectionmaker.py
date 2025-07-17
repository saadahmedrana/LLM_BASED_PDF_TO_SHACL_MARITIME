import json
import re

DATA = "2025_07_16_9a385908f6e70ba0f1fdg.lines.json"
with open(DATA, encoding="utf-8") as f:
    doc = json.load(f)

# Print any line whose text begins with a digit
for page in doc["pages"]:
    for ln in page["lines"]:
        txt = (ln.get("text_display") or ln.get("text") or "").strip()
        if re.match(r'^\d+', txt):
            print(f"P{page['page']:02d}:", repr(txt))
