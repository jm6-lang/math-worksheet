import json
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

import subprocess
result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
token = result.stdout.strip()
print(f"Token OK: {token[:10]}...")

import base64

repo = "jm6-lang/resource-nav"
base = "C:/resource-nav/"

# Write body to file for gh --input
body = {
    "message": "Add .github/workflows/deploy.yml",
    "content": base64.b64encode(open(base + ".github/workflows/deploy.yml", "rb").read()).decode(),
    "branch": "main"
}
body_path = "C:/Temp/wf_body.json"
with open(body_path, "w") as f:
    json.dump(body, f)

print("Body written to", body_path)

# Use gh api with --input
result2 = subprocess.run(
    ["gh", "api", f"repos/{repo}/contents/.github/workflows/deploy.yml", "--input", body_path],
    capture_output=True, text=True, timeout=20
)
print("STDOUT:", result2.stdout[:300])
print("STDERR:", result2.stderr[:300])
print("RC:", result2.returncode)
