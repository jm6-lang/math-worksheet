# -*- coding: utf-8 -*-
import os
import re
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

music_path = r"C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs\music\index.md"
movies_dir = r"C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs\movies"

with open(music_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract all markdown links
links = re.findall(r'\[([^\]]+)\]\((https://pan\.quark\.cn/s/[^\)]+)\)', content)

# Filter to get unique music resources
music_resources = []
seen_links = set()
for name, link in links:
    if link not in seen_links and 'pan.quark.cn' in link:
        music_resources.append((name.strip(), link))
        seen_links.add(link)

print(f"找到 {len(music_resources)} 个音乐资源")
for i, (name, link) in enumerate(music_resources):
    print(f"  {i+1}. {name}")

# Get max post number in movies
existing_posts = [f for f in os.listdir(movies_dir) if f.startswith("post_") and f.endswith(".md")]
max_num = 0
for p in existing_posts:
    try:
        num = int(p.replace("post_", "").replace(".md", ""))
        max_num = max(max_num, num)
    except:
        pass

print(f"\nmovies/ 当前最大 post 编号: {max_num}")

# Create post files for music resources
start_num = max_num + 1
print(f"\n开始创建 post_{start_num} 到 post_{start_num + len(music_resources) - 1}")

for i, (name, url) in enumerate(music_resources):
    post_num = start_num + i
    post_path = os.path.join(movies_dir, f"post_{post_num:03d}.md")
    
    content = f"""---
title: "{name}"
---

# {name}

| 平台 | 链接 |
| :--- | :--- |
| 夸克网盘 | [点击跳转]({url}) |

::: tip
如链接失效，请联系管理员更新
:::
"""
    
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"创建: post_{post_num:03d}.md")

print(f"\n共创建 {len(music_resources)} 个音乐 post 文件")

# Now add to index.md
index_path = os.path.join(movies_dir, "index.md")
with open(index_path, "r", encoding="utf-8") as f:
    index_content = f.read()

# Add music resources to index
new_lines = []
for i, (name, url) in enumerate(music_resources):
    post_num = start_num + i
    new_lines.append(f"| {name} | Quark | [点击进入](/movies/post_{post_num:03d}) |")

new_content = "\n".join(new_lines)

# Insert before the closing ---
if index_content.rstrip().endswith("---"):
    index_content = index_content.rstrip()[:-3].strip() + "\n" + new_content + "\n\n---"

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index_content)

print(f"\n已更新 movies/index.md，添加 {len(music_resources)} 个音乐资源")