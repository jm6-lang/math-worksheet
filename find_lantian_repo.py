import paramiko
import sys
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 搜索蓝天采集器 ===\n")

# 搜索各种可能的关键词
keywords = [
    "lantian-scraper",
    "lantian-php",
    "skycraper php",  
    "蓝天采集",
    "sky-blue scraper"
]

found_repos = []
for kw in keywords:
    cmd = f"curl -s 'https://api.github.com/search/repositories?q={kw.replace(' ', '+')}&per_page=3' 2>/dev/null"
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    try:
        data = json.loads(stdout.read().decode())
        count = data.get('total_count', 0)
        print(f"'{kw}': {count} 结果")
        if count > 0:
            for item in data.get('items', [])[:2]:
                print(f"  -> {item.get('html_url')} ({item.get('description','')[:40]})")
                found_repos.append(item)
    except Exception as e:
        print(f"'{kw}': 错误")

# 尝试直接访问可能的仓库
print("\n尝试直接访问可能的仓库:")
possible_urls = [
    "https://api.github.com/repos/xintein/lantian",
    "https://api.github.com/repos/lantian/lantian",
    "https://api.github.com/repos/skycraper/skycraper",
]

for url in possible_urls:
    cmd = f"curl -s '{url}' 2>/dev/null"
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
    try:
        data = json.loads(stdout.read().decode())
        if 'html_url' in data:
            print(f"  找到! {data.get('html_url')} - {data.get('description','')[:50]}")
            found_repos.append(data)
    except:
        print(f"  {url}: 404")

ssh.close()

if found_repos:
    print(f"\n共找到 {len(found_repos)} 个相关仓库")
