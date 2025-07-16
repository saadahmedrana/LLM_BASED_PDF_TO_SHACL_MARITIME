import requests
import json

options = {
    "conversion_formats": {"docx": True, "tex.zip": True},
    "math_inline_delimiters": ["$", "$"],
    "rm_spaces": True
}
r = requests.post("https://api.mathpix.com/v3/pdf",
    headers={
        "app_id":aaltouniversity_904e02_50e2ec
        "app_key":3b031e50881ca70948d80bb2cd528af985ec7d0aab8e18965fb34e694441ff82
    },
    data={
        "options_json": json.dumps(options)
    },
    files={
        "file": open("page9.pdf","rb")
    }
)
print(r.text.encode("utf8"))