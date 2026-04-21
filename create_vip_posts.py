# -*- coding: utf-8 -*-
"""
批量创建 tools/ 会员版资源 post 文件
"""

import os
import re
import sys
import io

# 解决 Windows 控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 用户提供的42个资源列表（带链接）
resources = [
    ("Reface一键换脸 v4.5.0 AI换脸工具", "https://pan.quark.cn/s/a54960efcf08"),
    ("上班摸鱼_老板键（软件）", "https://pan.quark.cn/s/19ea6c40d155"),
    ("Listen1（全网音乐免费听））", "https://pan.quark.cn/s/0f19852eab83"),
    ("Autodesk AutoCAD 2024", "https://pan.quark.cn/s/648e797ff85b"),
    ("酒店防窥检测1.26 会员版", "https://pan.quark.cn/s/a55f9d261f02"),
    ("去水印工具", "https://pan.quark.cn/s/24d6f26bb2d0"),
    ("AI Chat", "https://pan.quark.cn/s/3ebb19f720cc"),
    ("驾考题库大全会员版_", "https://pan.quark.cn/s/9394c429b093"),
    ("呐噗助眠", "https://pan.quark.cn/s/8e95a99ab039"),
    ("嗅觉浏览器 ", "https://pan.quark.cn/s/e159f31feb5e"),
    ("扫描全能王 会员版", "https://pan.quark.cn/s/9f1a2cb69dcd"),
    ("洛雪音乐（附最新可用音源）", "https://pan.quark.cn/s/7d199c18f040"),
    ("全新推出的免费音乐听歌软件-尼卡音乐🎵", "https://pan.quark.cn/s/852813bc1eb9"),
    ("车机", "https://pan.quark.cn/s/1828d0268644"),
    ("漫漫漫画 v5.2.43：为广大漫画爱好者打造的追漫神器，去广告版", "https://pan.quark.cn/s/2c9aa2031ed5"),
    ("手机照片恢复管家_7.5.0_VIP版_", "https://pan.quark.cn/s/6eb35751e6d1"),
    ("福昕高级PDF编辑器", "https://pan.quark.cn/s/88398fa94928"),
    ("微信对话生成器", "https://pan.quark.cn/s/e681e222ae6c"),
    ("傻瓜英语VIP会员版", "https://pan.quark.cn/s/0f69354ca70f"),
    ("酷我音乐_会员版 兼容所有机型！带SVIP！支持鸿蒙！", "https://pan.quark.cn/s/2921e8a1b59c"),
    ("Windows系统永久激活最新密钥", "https://pan.quark.cn/s/275d58007c5e"),
    ("畅听FM_2.3.2 可收听全国电台，免费无广告", "https://pan.quark.cn/s/b7046489b6b0"),
    ("Android 健身教练 v1.1.5 免费无广告", "https://pan.quark.cn/s/1826d7020682"),
    ("开发全能工具箱He3", "https://pan.quark.cn/s/44ead176505a"),
    ("情侣飞行棋（先保存，防和谐）", "https://pan.quark.cn/s/e7686d3af590"),
    ("万能格式转换", "https://pan.quark.cn/s/bc01151338ab"),
    ("解析机器人_会员版", "https://pan.quark.cn/s/1a7eb2d5e97c"),
    ("GET漫画v2.1.1绿化版", "https://pan.quark.cn/s/7ecfc9951415"),
    ("任小聊天话术APP", "https://pan.quark.cn/s/b3f5ed71e705"),
    ("视频音频批量格式转换器 v2.0", "https://pan.quark.cn/s/504ba86954a3"),
    ("微信聊天恢复_4.6.0", "https://pan.quark.cn/s/422a8656030e"),
    ("万象聚搜 v1.5 - 增 小说 漫画 -视频去水印等功能", "https://pan.quark.cn/s/e5d3418ec0c1"),
    ("风云录屏大师-VIP版（无水印无广告高清录屏工具）", "https://pan.quark.cn/s/0cb1bbec039c"),
    ("视频去重", "https://pan.quark.cn/s/ccee65cc166f"),
    ("黑神话悟空", "https://pan.quark.cn/s/bf63e69e7ac4"),
    ("AutoGLM", "https://pan.quark.cn/s/2846843621eb"),
    ("博看书苑安卓（附36个授权码）", "https://pan.quark.cn/s/a2daac82453e"),
    ("夸父工具箱", "https://pan.quark.cn/s/dc45d88e2e97"),
    ("工具魔盒_2.4.2", "https://pan.quark.cn/s/cdce324e9439"),
    ("安卓解析机器人高级版", "https://pan.quark.cn/s/e9e7a37395af"),
    ("太极工具箱", "https://pan.quark.cn/s/d8647b53e016"),
    ("快影剪辑_纯净版", "https://pan.quark.cn/s/de8c3c44f755"),
    ("Xmind思维导图模板331个", "https://pan.quark.cn/s/b31c5d0863d5"),
]

# 读取现有的 index.md 获取已有的资源名称
tools_dir = r"C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs\tools"
index_path = os.path.join(tools_dir, "index.md")

with open(index_path, "r", encoding="utf-8") as f:
    index_content = f.read()

# 提取已有的资源名称
existing_names = set()
for line in index_content.split("\n"):
    # 匹配 | 资源名称 | 平台 |
    match = re.search(r"\|\s*([^|]+?)\s*\|", line)
    if match:
        name = match.group(1).strip()
        if name and name != "资源名称":
            existing_names.add(name)

print(f"已有资源数量: {len(existing_names)}")

# 找出需要新增的资源
new_resources = []
for name, url in resources:
    # 检查是否已存在（模糊匹配）
    found = False
    for existing in existing_names:
        # 去掉特殊字符后比较
        clean_name = re.sub(r'[_\s\-\(\)（）🎵]', '', name)
        clean_existing = re.sub(r'[_\s\-\(\)（）🎵]', '', existing)
        if clean_name in clean_existing or clean_existing in clean_name:
            found = True
            print(f"已存在: {name}")
            break
    if not found:
        new_resources.append((name, url))

print(f"\n需要新增: {len(new_resources)} 个")
for name, url in new_resources:
    print(f"  - {name}")

# 获取当前最大的 post 编号
existing_posts = [f for f in os.listdir(tools_dir) if f.startswith("post_") and f.endswith(".md")]
max_num = 0
for p in existing_posts:
    num = int(p.replace("post_", "").replace(".md", ""))
    max_num = max(max_num, num)

print(f"\n当前最大 post 编号: {max_num}")

# 创建新 post 文件
start_num = max_num + 1
for i, (name, url) in enumerate(new_resources):
    post_num = start_num + i
    post_path = os.path.join(tools_dir, f"post_{post_num:03d}.md")
    
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
    
    print(f"创建: post_{post_num:03d}.md - {name}")

print(f"\n共创建 {len(new_resources)} 个文件")
