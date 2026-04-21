import os, base64, json, urllib.request, urllib.parse

# Get token from gh
import subprocess
result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
token = result.stdout.strip()
print(f"Token: {token[:10]}...")

REPO = "jm6-lang/resource-nav"
API = f"https://api.github.com/repos/{REPO}"

def api(method, path, data=None):
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.get_method = lambda: method
    if data:
        req.add_header("Content-Type", "application/json")
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())

# Upload files
def upload_file(path, content):
    content_b64 = base64.b64encode(content.encode()).decode()
    data = {
        "message": f"Add {path}",
        "content": content_b64,
        "branch": "main"
    }
    # Check if file exists
    try:
        api("GET", f"/contents/{path}")
        print(f"  Updating: {path}")
        api("PUT", f"/contents/{path}", data)
    except:
        print(f"  Creating: {path}")
        api("PUT", f"/contents/{path}", data)

# Walk docs directory
base = "C:\\resource-nav\\docs"
for root, dirs, files in os.walk(base):
    for file in files:
        filepath = os.path.join(root, file)
        rel = filepath.replace(base, "").replace("\\", "/").lstrip("/")
        if file.endswith(('.md', '.png', '.jpg', '.svg')):
            with open(filepath, "rb") as f:
                content = f.read().decode("utf-8", errors="ignore")
            upload_file(f"docs/{rel}", content)

# Upload root files
for f in ["package.json", ".gitignore", "README.md"]:
    full = f"C:\\resource-nav\\{f}"
    if os.path.exists(full):
        with open(full, "rb") as fh:
            content = fh.read().decode("utf-8", errors="ignore")
        upload_file(f, content)

# Upload workflow
with open("C:\\resource-nav\\.github\\workflows\\deploy.yml", "r") as f:
    wf = f.read()
upload_file(".github/workflows/deploy.yml", wf)

# Upload config
with open("C:\\resource-nav\\docs\\.vitepress\\config.mts", "r") as f:
    cfg = f.read()
upload_file("docs/.vitepress/config.mts", cfg)

print("\n✅ 所有文件上传完成!")
print("访问: https://jm6-lang.github.io/resource-nav/")
