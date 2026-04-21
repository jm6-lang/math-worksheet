import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 测试副业赚钱相关RSS源 ===\n")

feeds = [
    # 副业/网赚类
    "https://www.fumubang.com/rss",
    "https://www.dabanjia.com/feed",
    "https://www.3618med.com/feed",
    "http://www.zhlbw.com/feed",
    "https://www.itbear.com/blog/feed/",
    # 创业/商业
    "https://www.cyzone.cn/rss/",
    "https://www.huxiu.com/rss/0.xml",
    "https://www.iyunying.org/feed",
    # 技能/教程
    "https://www.imooc.com/article/feed",
    "https://zhuanlan.zhihu.com/p/95094121/rss",
    # 知乎专栏-副业
    "https://rsshub.app/zhihu/zhuanlan/95094121",
    # 自媒体
    "https://www.woshipm.com/feed",
    "https://www.niaogebiji.com/feed",
    # RSSHub proxies
    "https://rsshub.app/zhihu/hotlist",
]

for url in feeds:
    print(f"--- {url}")
    cmd = f"""curl -sL '{url}' -k --connect-timeout 8 --max-time 10 2>/dev/null | head -5"""
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
    result = stdout.read().decode('utf-8', errors='ignore').strip()[:150]
    if result and ('xml' in result.lower() or 'rss' in result.lower() or '<entry' in result.lower() or '<item' in result.lower()):
        print(f"  ✅ 有效")
    else:
        print(f"  ❌ 无效: {result[:80]}")

ssh.close()
