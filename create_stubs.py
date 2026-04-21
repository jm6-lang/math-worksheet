import os

# Create stub pages for missing directories
base = "C:\\resource-nav\\docs"
missing = ["media", "education", "design", "fitness", "music"]

stub_content = """# {title}

> 正在整理资源中，敬请期待...

## 敬请期待

更多资源整理中，稍后上线。

[← 返回资源总览](/resources)
"""

files_to_create = [
    ("media/index.md", "🎬 影视资源"),
    ("education/index.md", "🎓 在线教育"),
    ("design/index.md", "🎨 设计素材"),
    ("fitness/index.md", "🏋️ 健身运动"),
    ("music/index.md", "🎵 音乐学习"),
]

for path, title in files_to_create:
    full = os.path.join(base, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(stub_content.replace("{title}", title))
    print(f"Created: {path}")

print("Done!")
