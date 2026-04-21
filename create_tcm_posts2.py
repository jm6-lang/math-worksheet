import os, subprocess, base64

base = r"C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs\chinese-traditional"

# post_001: fix the wrong quark link (a0662457b41e -> 0c74d5077d75)
post_001 = open(os.path.join(base, "post_001.md"), "r", encoding="utf-8").read()
post_001_fixed = post_001.replace("a0662457b41e", "0c74d5077d75")
open(os.path.join(base, "post_001.md"), "w", encoding="utf-8").write(post_001_fixed)
print("post_001.md: link fixed (a0662457b41e -> 0c74d5077d75)")

# new posts
posts = [
    ("post_002.md", "中华玄学文化书系", "https://pan.quark.cn/s/0e7cc71c170e"),
    ("post_003.md", "民间秘术大全", "https://pan.quark.cn/s/e0235f7937f2"),
    ("post_004.md", "风水学", "https://pan.quark.cn/s/79eba9118e5e"),
]

tmpl = '''---
title: "{title}"
description: "点击免费下载 {title}。小二郎资源分享站深度整理，分类：传统文化 / 国学精粹。"
keywords: "传统文化, 国学精粹, 周易易经, 风水命理, 文化传承, {title}"
---

# {title}

<Badge type="tip" text="Quark" /> <Badge type="warning" text="精品资源" />

## 📋 资源介绍
欢迎访问小二郎资源分享站！本页面提供 **{title}** 的免费下载链接。该资源经过深度整理，旨在为您提供优质的学习与研究素材。

## 📥 资源详情
- **资源名称**: {title}
- **所属分类**: 传统文化 / 国学精粹
- **更新日期**: 2026-04-17
- **直达链接**: <a href="{url}" target="_blank" rel="noopener noreferrer" class="download-link">🔗 点击获取网盘资源</a>

---
### 🛡️ 申明与反馈
- **版权申明**: 本资源均收集自互联网，版权归原作者所有。仅供个人学习研究，请于下载后24小时内删除。
- **链接失效**: 如果您发现下载链接已失效，请联系管理员核实。

---
💡 **更多资源**: 返回 [小二郎资源分享站](/)
'''

for fname, title, url in posts:
    content = tmpl.format(title=title, url=url)
    open(os.path.join(base, fname), "w", encoding="utf-8").write(content)
    print(f"Created {fname}: {title}")

print("\nAll done.")
