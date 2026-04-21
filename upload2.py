import os, base64, json, urllib.request, urllib.error

import subprocess
result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
token = result.stdout.strip()

REPO = "jm6-lang/resource-nav"

def api_get(path):
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/contents/{path}")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())

def api_put(path, content):
    encoded = base64.b64encode(content.encode('utf-8')).decode('ascii')
    data = {"message": f"Update {path}", "content": encoded, "branch": "main"}
    try:
        existing = api_get(path)
        data["sha"] = existing["sha"]
    except urllib.error.HTTPError:
        pass
    body = json.dumps(data).encode()
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/contents/{path}",
        data=body, method="PUT"
    )
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = json.loads(e.read())
        print(f"    ERROR {e.code}: {err.get('message', err)[:100]}")
        return None

def upload_file(rel_path, content):
    try:
        result = api_put(rel_path, content)
        if result:
            print(f"  OK {rel_path}")
        else:
            print(f"  FAIL {rel_path}")
    except Exception as e:
        print(f"  EXC {rel_path}: {e}")

base = "C:\\resource-nav"

print("Uploading workflow...")
with open(f"{base}\\.github\\workflows\\deploy.yml", "r", encoding="utf-8") as f:
    upload_file(".github/workflows/deploy.yml", f.read())

print("Uploading config...")
with open(f"{base}\\docs\\.vitepress\\config.mts", "r", encoding="utf-8") as f:
    upload_file("docs/.vitepress/config.mts", f.read())

print("Uploading README...")
upload_file("README.md", "# 资源导航站\n\nhttps://jm6-lang.github.io/resource-nav/")

print("Uploading package.json...")
with open(f"{base}\\package.json", "r", encoding="utf-8") as f:
    upload_file("package.json", f.read())

print("Uploading .gitignore...")
with open(f"{base}\\.gitignore", "r", encoding="utf-8") as f:
    upload_file(".gitignore", f.read())

print("Uploading markdown files...")
count = 0
for root, dirs, files in os.walk(f"{base}\\docs"):
    if 'cache' in root:
        continue
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            rel = filepath.replace(f"{base}\\docs\\", "").replace("\\", "/")
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    upload_file(f"docs/{rel}", f.read())
                count += 1
            except Exception as e:
                print(f"  ERROR {rel}: {e}")

print(f"\nUploaded {count} markdown files")
print("\nDone!")
