import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 直接测试36kr内容提取 ===\n")

cmd = 'curl -s "https://36kr.com/p/3756523983536905" -H "User-Agent: Mozilla/5.0" | python3 -c "import sys; from bs4 import BeautifulSoup; html=sys.stdin.read(); soup=BeautifulSoup(html,\"html.parser\"); print(len(html),\"bytes\"); [tag.decompose() for tag in soup([\"script\",\"style\"])]; print(len(soup.get_text(strip=True)),\"chars\")"'
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
print(stdout.read().decode().strip())

print("\n=== 直接测试SSPai内容提取 ===\n")
cmd = 'curl -s "https://sspai.com/post/108150" -H "User-Agent: Mozilla/5.0" | python3 -c "import sys; from bs4 import BeautifulSoup; html=sys.stdin.read(); soup=BeautifulSoup(html,\"html.parser\"); print(len(html),\"bytes\"); [tag.decompose() for tag in soup([\"script\",\"style\"])]; print(len(soup.get_text(strip=True)),\"chars\")"'
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
print(stdout.read().decode().strip())

ssh.close()
