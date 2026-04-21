# -*- coding: utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Download the result file
sftp = ssh.open_sftp()
with sftp.open('/root/scripts/published_titles.txt', 'rb') as f:
    raw = f.read()
sftp.close()

content = raw.decode('utf-8')

# Parse published titles
published_titles = set()
for line in content.strip().split('\n'):
    parts = line.split('\t')
    if len(parts) >= 2:
        title = parts[1]
        published_titles.add(title)

print("Published titles from batch (ID 662-709):")
for t in sorted(published_titles):
    print(" - {}".format(t), flush=True)

print("\nTotal published in batch: {}".format(len(published_titles)), flush=True)

# User's full list (from the message)
user_resources = [
    # Books (14)
    "中国古玩鉴识知识系列书籍",
    "创业优质教程合集",
    "百病食疗大全彩图精装",
    "用声音修炼气场完结",
    "梅花易数白话解",
    "富爸爸系列全集32册",
    "书库合集",
    "人人都可以学的顶级思维法套装7册",
    "富爸爸套装五册",
    "中医补肾壮阳秘方",
    "父与子的X教尬聊",
    "MBA课程",
    "中医古籍合集超全系列",
    "农村自建房图纸合集",
    # Tools (55)
    "解锁版软件",
    "TikTokMod解除限制版",
    "一键迁移网盘资源",
    "迅雷最新不限速版",
    "wifi万能钥匙SVIP版",
    "UC网盘批量转存工具",
    "夸克网盘批量转存分享工具",
    "金铲铲单机版",
    "骗子酒馆手机版",
    "可灵无限灵感值",
    "全网最全机顶盒视频教程",
    "迅雷VIP解锁版",
    "微信好友检测工具",
    "影梭定位修改大师",
    "抢福袋工具",
    "微粉大师",
    "李跳跳",
    "WPS解锁版",
    "Windows纯净版系统镜像",
    "国外最火app合集",
    "电脑系统安装工具包",
    "抖音短视频下载提取",
    "去除马赛克",
    "AI写作鱼",
    "3D动态照片",
    "变声器大师破解版",
    "梨园行戏曲TV版",
    "马克全能去水印",
    "Zapya快牙",
    "作业帮",
    "TVBox_takagen99",
    "酷我音乐车机版",
    "Youtube视频下载器",
    "视频去水印神器",
    "轻听音乐",
    "全球卫星电视TV",
    "即梦Ai破解版",
    "动物翻译器",
    "搬运工具包",
    "电脑密码破解工具",
    "手机版闲鱼助手",
    "图片批量处理",
    "文件批量重命名",
    "手机刷机工具箱",
    "CDR2023中文破解版",
    "打卡软件神器",
    "查企业查信息",
    "笔趣阁",
    "公众号爆文机器人",
    "七星虚拟机",
    "电商图片采集工具",
    "场控助手",
    "TVBOX最新接口",
    "AI唱歌软件",
    "SolidWorks2025"
]

print("\n\nChecking which resources are NOT published:")
missing = []
for res in user_resources:
    # Check if any published title contains this resource name
    found = any(res in title or title in res for title in published_titles)
    if not found:
        missing.append(res)
        print(" MISSING: {}".format(res), flush=True)

print("\n\nTotal missing: {}".format(len(missing)), flush=True)

ssh.close()
