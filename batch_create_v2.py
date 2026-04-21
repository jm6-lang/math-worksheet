#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Batch create 23 curriculum post files."""
import subprocess, sys, os, json

write_script = r"E:\Qclaw\resources\openclaw\config\skills\qclaw-text-file\scripts\write_file.py"
output_dir = r"C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs\curriculum"
tmp_dir = os.environ.get("TEMP", "/tmp")

# Load resource data from JSON
json_path = os.path.join(tmp_dir, "resources_data.json")
with open(json_path, "r", encoding="utf-8") as f:
    resources = json.load(f)

start_num = 108

for i, res in enumerate(resources):
    num = start_num + i
    filename = f"post_{num:03d}.md"
    filepath = os.path.join(output_dir, filename)

    title = res["title"]
    url = res["url"]
    category = res["category"]
    intro = res["desc_intro"]
    detail = res["desc_detail"]
    keywords = f"\u4e92\u8054\u7f51\u9879\u76ee, \u8d5a\u94b1\u6559\u7a0b, \u526f\u4e1a\u9879\u76ee, \u6280\u80fd\u63d0\u5347, {title}"

    content = f"""---
title: "{title}"
description: "\u70b9\u51fb\u514d\u8d39\u4e0b\u8f7d {title}\u3002\u5c0f\u4e8c\u90ce\u8d44\u6e90\u5206\u4eab\u7ad9\u6df1\u5ea6\u6574\u7406\uff0c\u5206\u7c7b\uff1a{category}\u3002"
keywords: "{keywords}"
---

# {title}

<Badge type="tip" text="Quark" /> <Badge type="warning" text="\u7cbe\u54c1\u8d44\u6e90" />

## \U0001f4d6 \u8d44\u6e90\u5bfc\u8bfb
{intro}

## \U0001f4cb \u8d44\u6e90\u8be6\u60c5
{detail}

- **\u8d44\u6e90\u540d\u79f0**: {title}
- **\u6240\u5c5e\u5206\u7c7b**: {category}
- **\u66f4\u65b0\u65e5\u671f**: 2026-04-18
- **\u4e0b\u8f7d\u5730\u5740**: <a href="{url}" target="_blank" rel="noopener noreferrer" class="download-link">\U0001f517 \u70b9\u51fb\u83b7\u53d6\u7f51\u76d8\u8d44\u6e90</a>

---
### \U0001f6e1\ufe0f \u7533\u660e\u4e0e\u53cd\u9988
- **\u7248\u6743\u7533\u660e**: \u672c\u7ad9\u6240\u6709\u8d44\u6e90\u5747\u6536\u96c6\u81ea\u4e92\u8054\u7f51\uff0c\u7248\u6743\u5f52\u539f\u4f5c\u8005\u6240\u6709\u3002\u4ec5\u4f9b\u4e2a\u4eba\u5b66\u4e60\u7814\u7a76\uff0c\u8bf7\u4e8e\u4e0b\u8f7d\u540e24\u5c0f\u65f6\u5185\u5220\u9664\u3002
- **\u94fe\u63a5\u5931\u6548**: \u5982\u679c\u60a8\u53d1\u73b0\u4e0b\u8f7d\u94fe\u63a5\u5df2\u5931\u6548\uff0c\u8bf7\u8054\u7cfb\u7ba1\u7406\u5458\u6838\u5b9e\u3002

---
\U0001f4a1 **\u66f4\u591a\u5185\u5bb9**: \u8fd4\u56de [\u5c0f\u4e8c\u90ce\u8d44\u6e90\u5206\u4eab\u7ad9](/) 
"""

    # Write content to temp file with UTF-8 encoding
    tmp_path = os.path.join(tmp_dir, f"_curriculum_post_{num}.txt")
    with open(tmp_path, "w", encoding="utf-8") as tf:
        tf.write(content)

    result = subprocess.run(
        [sys.executable, write_script, "--path", filepath, "--content-file", tmp_path, "--platform", "auto"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    
    if result.returncode == 0:
        print(f"OK: {filename}")
    else:
        print(f"FAIL: {filename} - {result.stderr[:200]}")
    
    try:
        os.remove(tmp_path)
    except:
        pass

print(f"\nDone! Created {len(resources)} files (post_{start_num:03d} to post_{start_num + len(resources) - 1:03d})")
