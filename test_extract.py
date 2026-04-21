import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 直接测试内容提取 ===\n")

# 测试36kr文章
test_url = "https://36kr.com/p/3756523983536905"
cmd = f'''cd /www/wwwroot/resource_site/auto_collect && python3 -c "
import requests
from bs4 import BeautifulSoup
import random

UAS = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36']
headers = {{'User-Agent': random.choice(UAS), 'Accept-Language': 'zh-CN,zh;q=0.9'}}

r = requests.get('{test_url}', headers=headers, timeout=15)
print('Status:', r.status_code)
print('Len:', len(r.text))

soup = BeautifulSoup(r.text, 'html.parser')

# Check for common article selectors
for sel in ['article', '.article-content', '.post-content', '.content', '.main-content']:
    elem = soup.select_one(sel)
    if elem:
        text = elem.get_text(separator='\\n', strip=True)
        print(f'Selector {sel}: {len(text)} chars')
        if len(text) > 100:
            print('Preview:', text[:300])
            break
else:
    # Try body
    body = soup.find('body')
    if body:
        print('Body:', len(body.get_text(strip=True)), 'chars')
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode().strip())

# 测试SSPai文章
print("\n\n=== 测试SSPai ===")
test_url = "https://sspai.com/post/108150"
cmd = f'''cd /www/wwwroot/resource_site/auto_collect && python3 -c "
import requests
from bs4 import BeautifulSoup

headers = {{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}}

r = requests.get('{test_url}', headers=headers, timeout=15)
print('Status:', r.status_code)

soup = BeautifulSoup(r.text, 'html.parser')
for tag in soup(['script', 'style']):
    tag.decompose()

for sel in ['article', '.content', '.article']:
    elem = soup.select_one(sel)
    if elem:
        text = elem.get_text(separator='\\n', strip=True)
        print(f'{sel}: {len(text)} chars')
        if len(text) > 500:
            print('OK! Content found')
            print(text[:300])
            break
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode().strip())

ssh.close()
