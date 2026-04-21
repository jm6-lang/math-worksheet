import subprocess, os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

repo_name = "resource-nav"

# 创建 GitHub 仓库（私有）
print("创建 GitHub 仓库...")
result = subprocess.run(
    ["gh", "repo", "create", repo_name, "--public", "--source=.", "--push", "--description", "资源导航站 - 海量免费资源下载"],
    cwd="C:\\resource-nav",
    capture_output=True, text=True
)
print(result.stdout)
print(result.stderr)

# 等待一下
import time
time.sleep(2)

# 启用 GitHub Pages
print("\n启用 GitHub Pages...")
result2 = subprocess.run(
    ["gh", "repo", "edit", repo_name, "--enable-pages"],
    capture_output=True, text=True
)
print(result2.stdout)
print(result2.stderr)

# 创建 GitHub Actions workflow
workflow_dir = "C:\\resource-nav\\.github\\workflows"
os.makedirs(workflow_dir, exist_ok=True)

workflow = '''name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build VitePress site
        run: npm run docs:build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs/.vitepress/dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
'''

with open(f"{workflow_dir}\\deploy.yml", "w", encoding="utf-8") as f:
    f.write(workflow)

print("GitHub Actions workflow 创建完成")

# 提交并推送 workflow
subprocess.run(["git", "add", ".github/"], cwd="C:\\resource-nav")
subprocess.run(["git", "commit", "-m", "Add GitHub Actions workflow for auto deploy"], cwd="C:\\resource-nav")
subprocess.run(["git", "push", "origin", "main"], cwd="C:\\resource-nav", capture_output=True)

print("\n✅ 部署配置完成!")
print(f"\n访问地址: https://jm6-lang.github.io/{repo_name}/")
print("\n约2分钟后自动部署生效")
