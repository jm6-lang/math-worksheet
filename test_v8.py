import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 上传v8
with open(r"C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\collector_v8.py", "r", encoding="utf-8") as f:
    new_collector = f.read()

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/collector.py', 'w') as f:
    f.write(new_collector)
sftp.close()
print("采集器v8已上传")

# 验证
stdin, stdout, stderr = ssh.exec_command("python3 -m py_compile /www/wwwroot/resource_site/auto_collect/collector.py && echo 'OK'", timeout=10)
print("语法:", stdout.read().decode().strip())

# 更新配置，使用cyzone RSS
new_config = {
  "wp_url": "https://skillxm.cn",
  "wp_user": "admin",
  "category": "网赚项目",
  "keywords": ["网赚项目", "副业赚钱", "创业教程"],
  "max_posts_per_run": 8,
  "min_content_length": 300,
  "blacklisted_domains": ["baidu.com", "bing.com", "google.com", "weixin.qq.com", "mp.weixin.qq.com"],
  "wp_api_token": "s6eW 2kHy 8yqu XNuY JjoK HHOR",
  "rss_feeds": [
    "https://www.cyzone.cn/rss/",
  ],
  "category_id": 53
}

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/config.json', 'w') as f:
    import json
    json.dump(new_config, f, ensure_ascii=False, indent=2)
sftp.close()
print("配置已更新 - 使用创业邦RSS")

# 测试
print("\n测试采集器（2分钟）...")
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site/auto_collect && timeout 120 python3 collector.py 2>&1", timeout=150)
result = stdout.read().decode().strip()
print(result[-4000:] if len(result) > 4000 else result)

# 检查数据库
stdin, stdout, stderr = ssh.exec_command("sqlite3 /www/wwwroot/resource_site/auto_collect/published.db 'SELECT COUNT(*) FROM pub; SELECT MAX(created) FROM pub;'", timeout=10)
print("\n数据库:", stdout.read().decode().strip())

ssh.close()
