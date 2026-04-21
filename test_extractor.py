import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 检查内容提取工具 ===\n")

# 1. 检查trafilatura
stdin, stdout, stderr = ssh.exec_command("pip3 show trafilatura 2>/dev/null || echo '未安装'", timeout=10)
print("1. Trafilatura:", stdout.read().decode().strip())

# 2. 检查其他提取工具
stdin, stdout, stderr = ssh.exec_command("pip3 list 2>/dev/null | grep -iE 'beautifulsoup|requests|selenium|playwright|newspaper'", timeout=10)
print("\n2. 可用库:")
print(stdout.read().decode().strip() or "无")

# 3. 测试不同网站的内容提取
print("\n3. 测试内容提取...")
test_url = "https://www.afenxi.com/124149.html"
stdin, stdout, stderr = ssh.exec_command(f"python3 -c \"import trafilatura; result = trafilatura.fetch_url('{test_url}'); print('FETCHED:', len(result) if result else 'None')\"", timeout=30)
print(f"   Trafilatura测试:", stdout.read().decode().strip())

# 4. 测试requests+BeautifulSoup提取
stdin, stdout, stderr = ssh.exec_command(f"python3 -c \"
import requests
from bs4 import BeautifulSoup
headers = {{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}}
r = requests.get('{test_url}', headers=headers, timeout=15)
soup = BeautifulSoup(r.text, 'html.parser')
# 尝试找文章内容
article = soup.find('article') or soup.find('div', class_='content') or soup.find('div', id='content')
print('Content length:', len(article.text) if article else 'Not found')
\"", timeout=30)
print(f"   BeautifulSoup测试:", stdout.read().decode().strip())

ssh.close()
