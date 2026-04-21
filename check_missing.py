import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Get all published post titles to check for duplicates
stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT post_title FROM wp_posts WHERE post_type='post' AND post_status='publish';\"")
titles = stdout.read().decode('utf-8', errors='ignore').strip().split('\n')
titles_set = set(titles)
print("Total published titles: {}".format(len(titles_set)), flush=True)

# Check for specific titles from the latest batch
resources_to_check = [
    "解锁版软件",
    "TikTokMod解除限制版", 
    "一键迁移网盘资源百度转迅雷",
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
    "国外最火应用app合集",
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
    "Youtube油管视频下载器",
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

print("\nChecking which resources are already published:")
for res in resources_to_check:
    found = any(res in title for title in titles_set)
    print("{}: {}".format(res, "已发布" if found else "未发布"), flush=True)

ssh.close()
