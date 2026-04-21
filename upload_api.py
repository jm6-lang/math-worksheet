import os, base64, json, urllib.request, time

import subprocess
result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
token = result.stdout.strip()

REPO = "jm6-lang/resource-nav"
API_BASE = f"https://api.github.com/repos/{REPO}"

def api_get(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())

def api_put(path, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(f"https://api.github.com{path}", data=body)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("Content-Type", "application/json")
    req.get_method = lambda: "PUT"
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())

def upload_file(path, content):
    encoded = base64.b64encode(content.encode('utf-8')).decode('ascii')
    data = {"message": f"Add {path}", "content": encoded, "branch": "main"}
    try:
        existing = api_get(f"/contents/{path}")
        data["sha"] = existing["sha"]
        print(f"  PUT   {path}")
    except:
        print(f"  POST  {path}")
    api_put(f"/contents/{path}", data)

base = "C:\\resource-nav"

# Upload workflow first (needed for pages)
print("1. Uploading workflow...")
with open(f"{base}\\.github\\workflows\\deploy.yml", "r", encoding="utf-8") as f:
    upload_file(".github/workflows/deploy.yml", f.read())

# Upload config
print("2. Uploading config...")
with open(f"{base}\\docs\\.vitepress\\config.mts", "r", encoding="utf-8") as f:
    upload_file("docs/.vitepress/config.mts", f.read())

# Upload README
print("3. Uploading README...")
readme = '''# 资源导航站

> 海量免费资源下载导航

## 访问地址

**GitHub Pages**: https://jm6-lang.github.io/resource-nav/

## 如何更新内容

1. 克隆仓库: `git clone https://github.com/jm6-lang/resource-nav.git`
2. 安装依赖: `npm install`
3. 本地预览: `npm run docs:dev`
4. 编辑 `docs/*.md` 文件添加资源
5. 推送到 GitHub 自动部署
'''
upload_file("README.md", readme)

# Upload package.json
print("4. Uploading package.json...")
with open(f"{base}\\package.json", "r", encoding="utf-8") as f:
    upload_file("package.json", f.read())

# Upload .gitignore
print("5. Uploading .gitignore...")
with open(f"{base}\\.gitignore", "r", encoding="utf-8") as f:
    upload_file(".gitignore", f.read())

# Upload all markdown files
print("6. Uploading docs...")
for root, dirs, files in os.walk(f"{base}\\docs"):
    # Skip .vitepress/cache
    if '.vitepress' in root and 'cache' in root:
        continue
    for file in files:
        if file.endswith('.md'):
            filepath = os.path.join(root, file)
            rel = filepath.replace(f"{base}\\docs\\", "").replace("\\", "/")
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                upload_file(f"docs/{rel}", f.read())

print("\n✅ 全部文件上传完成!")

# Enable GitHub Pages
print("\n7. 启用 GitHub Pages...")
pages_data = {
    "source": {
        "branch": "gh-pages",
        "path": "/"
    }
}
# Try via API - might need workflow deployment instead
try:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/pages",
        data=json.dumps({"source": {"branch": "gh-pages", "path": "/"}}).encode(),
        method="POST"
    )
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    resp = urllib.request.urlopen(req, timeout=30)
    print(f"  Pages enabled: {resp.getcode()}")
except Exception as e:
    print(f"  Pages setup: {str(e)[:200]}")
    print("  (Pages will auto-enable when workflow first runs)")

print("\n📍 访问地址: https://jm6-lang.github.io/resource-nav/")
print("⏱️  约2分钟后 GitHub Actions 自动构建并部署")
