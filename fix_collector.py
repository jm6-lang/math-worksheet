import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 修复采集器 ===\n")

# 1. 备份原配置
stdin, stdout, stderr = ssh.exec_command("cp /www/wwwroot/resource_site/auto_collect/config.json /www/wwwroot/resource_site/auto_collect/config.json.bak", timeout=10)
print("1. 配置已备份")

# 2. 更新配置文件 - 添加更多RSS源，移除Bing搜索依赖
new_config = {
  "wp_url": "https://skillxm.cn",
  "wp_user": "admin",
  "category": "网赚项目",
  "keywords": [
    "网赚项目 博客 教程",
    "副业赚钱 实操 教程",
    "兼职赚钱 副业 教程",
    "网络赚钱项目 2025 教程",
    "数字营销 副业 教程",
    "投资理财教程",
    "个人品牌 副业项目",
    "短视频运营 副业 教程",
    "虚拟资源 赚钱 教程",
    "跨境电商 创业 教程",
    "微信公众号 赚钱 教程",
    "直播带货 副业 教程",
    "知识付费 创业 副业",
    "小红书运营 变现 教程",
    "小程序创业 赚钱 项目"
  ],
  "max_posts_per_run": 8,
  "min_content_length": 500,  # 降低最低字数要求
  "blacklisted_domains": [
    "baidu.com", "bing.com", "google.com", "weixin.qq.com",
    "mp.weixin.qq.com", "youtube.com", "tiktok.com", "douyin.com",
    "taobao.com", "jd.com", "pinduoduo.com", "zhihu.com",
    "bilibili.com", "cctv.com", "weibo.com", "twitter.com",
    "instagram.com", "qq.com", "sogou.com", "so.com"
  ],
  "wp_api_token": "s6eW 2kHy 8yqu XNuY JjoK HHOR",
  "rss_feeds": [
    "https://www.36kr.com/feed",
    "https://sspai.com/feed",
    "https://rsshub.app/zhihu/hotlist",
    "https://rsshub.app/ithome/ranking/daily",
    "https://rsshub.app/toutiao/trending",
    "https://rsshub.app/juejin/trending/0",
    "https://www.ifeng.com/rss/RSSHistory.xml",
    "https://www.zaobao.com.sg/rss/realtime/china",
    "http://www.afenxi.com/feed",
    "https://www.admin5.com/rss/"
  ],
  "category_id": 53
}

# 上传新配置
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/config.json', 'w') as f:
    json.dump(new_config, f, ensure_ascii=False, indent=2)
sftp.close()
print("2. 配置已更新 - 降低最低字数要求，添加更多RSS源")

# 3. 测试采集器运行
print("\n3. 测试采集器...")
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site/auto_collect && timeout 120 python3 collector.py 2>&1 | tail -50", timeout=150)
output = stdout.read().decode().strip()
print(output[-2000:] if len(output) > 2000 else output)

# 4. 检查是否成功
if "published" in output.lower():
    # 提取成功数量
    import re
    match = re.search(r'(\d+)/(\d+) published', output)
    if match:
        print(f"\n采集结果: {match.group(1)}/{match.group(2)} 成功")

ssh.close()
