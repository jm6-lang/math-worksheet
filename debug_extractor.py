import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 调试内容提取 ===\n")

# 1. 直接在服务器上测试提取
test_url = "https://sspai.com/post/108343"
print(f"测试URL: {test_url}")

cmd = '''cd /www/wwwroot/resource_site/auto_collect && python3 -c "
import requests
from bs4 import BeautifulSoup

url = 'https://sspai.com/post/108343'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

try:
    r = requests.get(url, headers=HEADERS, timeout=15)
    print('Status:', r.status_code)
    print('Encoding:', r.encoding)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # 查找内容
    selectors = ['article', '[class*=content]', '[class*=article]', '[class*=post]']
    for sel in selectors:
        elem = soup.select_one(sel)
        if elem:
            text = elem.get_text(separator='\\n', strip=True)
            print(f'Selector {sel}: {len(text)} chars')
            if len(text) > 100:
                print('First 200 chars:', text[:200])
                break
except Exception as e:
    print('Error:', e)
"
'''

stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode().strip())

# 2. 测试36kr文章
print("\n\n测试36kr文章...")
cmd2 = '''cd /www/wwwroot/resource_site/auto_collect && python3 -c "
import requests
url = 'https://www.36kr.com/p/2802345785685255'
HEADERS = {'User-Agent': 'Mozilla/5.0', 'Accept-Language': 'zh-CN'}
try:
    r = requests.get(url, headers=HEADERS, timeout=15)
    print('Status:', r.status_code)
    print('Len:', len(r.text))
except Exception as e:
    print('Error:', e)
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd2, timeout=30)
print(stdout.read().decode().strip())

ssh.close()
