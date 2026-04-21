# -*- coding: utf-8 -*-
import os
import re
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Read the music index.md file
music_path = r"C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs\music\index.md"

with open(music_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract table rows from the markdown
rows = re.findall(r'\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|', content)

music_resources = []
for row in rows:
    name = row[0].strip()
    desc = row[1].strip()
    link = row[3].strip()
    if name and link and name not in ['资源名称']:
        music_resources.append((name, desc, link))

print(f"找到 {len(music_resources)} 个音乐资源")

# Now check what post files exist in movies
movies_dir = r"C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs\movies"
existing_posts = [f for f in os.listdir(movies_dir) if f.startswith("post_") and f.endswith(".md")]
max_num = 0
for p in existing_posts:
    try:
        num = int(p.replace("post_", "").replace(".md", ""))
        max_num = max(max_num, num)
    except:
        pass

print(f"movies/ 目录现有最大 post 编号: {max_num}")
print(f"将从 post_{max_num + 1} 开始创建")