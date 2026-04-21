import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 下载天空采集器 ===\n")

# 使用GitHub API获取下载链接
print("1. 获取最新发布版本...")
cmd = """curl -sL 'https://api.github.com/repos/zorlan/skycaiji/releases/latest' 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('版本:', d.get('tag_name','unknown')); [print('下载:', a['browser_download_url']) for a in d.get('assets',[])]" """
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode().strip()
print(result)

# 也尝试直接用git clone
print("\n2. 使用git clone下载...")
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot && rm -rf skycaiji && git clone https://github.com/zorlan/skycaiji.git skycaiji 2>&1", timeout=60)
result = stdout.read().decode().strip()
print(result[:500])

# 检查文件
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/skycaiji/ | head -20", timeout=10)
print("\n3. 文件列表:")
print(stdout.read().decode().strip())

ssh.close()
