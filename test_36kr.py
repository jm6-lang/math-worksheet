import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 测试36kr文章内容获取 ===\n")

# 直接用curl获取36kr文章
cmd = '''curl -s "https://36kr.com/p/3756523983536905" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" -H "Accept-Language: zh-CN,zh;q=0.9" | wc -c'''
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
bytes_count = stdout.read().decode().strip()
print(f"36kr文章字节数: {bytes_count}")

# 用Python requests
cmd = '''python3 -c "
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
r = requests.get('https://36kr.com/p/3756523983536905', headers=headers, timeout=15)
print('Status:', r.status_code)
print('Len:', len(r.text))
if r.status_code == 200:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    for tag in soup(['script', 'style', 'nav']):
        tag.decompose()
    text = soup.get_text(separator=' ', strip=True)
    print('Text len:', len(text))
    print('Preview:', text[:500])
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode().strip())

ssh.close()
