# -*- coding: utf-8 -*-
"""
更新 tools/index.md 添加新资源
"""

import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

tools_dir = r"C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs\tools"
index_path = os.path.join(tools_dir, "index.md")

# 新增的资源列表（从 post_194 到 post_224）
new_entries = [
    ("post_194", "Reface一键换脸 v4.5.0 AI换脸工具", "Quark"),
    ("post_195", "酒店防窥检测1.26 会员版", "Quark"),
    ("post_196", "AI Chat", "Quark"),
    ("post_197", "扫描全能王 会员版", "Quark"),
    ("post_198", "漫漫漫画 v5.2.43：为广大漫画爱好者打造的追漫神器，去广告版", "Quark"),
    ("post_199", "福昕高级PDF编辑器", "Quark"),
    ("post_200", "傻瓜英语VIP会员版", "Quark"),
    ("post_201", "酷我音乐_会员版 兼容所有机型！带SVIP！支持鸿蒙！", "Quark"),
    ("post_202", "Windows系统永久激活最新密钥", "Quark"),
    ("post_203", "畅听FM_2.3.2 可收听全国电台，免费无广告", "Quark"),
    ("post_204", "Android 健身教练 v1.1.5 免费无广告", "Quark"),
    ("post_205", "开发全能工具箱He3", "Quark"),
    ("post_206", "情侣飞行棋（先保存，防和谐）", "Quark"),
    ("post_207", "万能格式转换", "Quark"),
    ("post_208", "解析机器人_会员版", "Quark"),
    ("post_209", "GET漫画v2.1.1绿化版", "Quark"),
    ("post_210", "任小聊天话术APP", "Quark"),
    ("post_211", "视频音频批量格式转换器 v2.0", "Quark"),
    ("post_212", "微信聊天恢复_4.6.0", "Quark"),
    ("post_213", "万象聚搜 v1.5 - 增 小说 漫画 -视频去水印等功能", "Quark"),
    ("post_214", "风云录屏大师-VIP版（无水印无广告高清录屏工具）", "Quark"),
    ("post_215", "视频去重", "Quark"),
    ("post_216", "黑神话悟空", "Quark"),
    ("post_217", "AutoGLM", "Quark"),
    ("post_218", "博看书苑安卓（附36个授权码）", "Quark"),
    ("post_219", "夸父工具箱", "Quark"),
    ("post_220", "工具魔盒_2.4.2", "Quark"),
    ("post_221", "安卓解析机器人高级版", "Quark"),
    ("post_222", "太极工具箱", "Quark"),
    ("post_223", "快影剪辑_纯净版", "Quark"),
    ("post_224", "Xmind思维导图模板331个", "Quark"),
]

# 读取现有 index.md
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 添加新条目到表格末尾（在 --- 之前）
new_lines = []
for post_num, name, platform in new_entries:
    new_lines.append(f"| {name} | {platform} | [点击进入](/tools/{post_num}) |")

new_content = "\n".join(new_lines)

# 找到表格结束位置（在 --- 之前插入）
if content.rstrip().endswith("---"):
    # 如果以 --- 结尾，直接在 --- 前插入
    content = content.rstrip()[:-3].strip() + "\n" + new_content + "\n\n---"
else:
    # 否则在最后插入
    content = content + "\n" + new_content + "\n"

# 写回
with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"已添加 {len(new_entries)} 个新资源到 index.md")
