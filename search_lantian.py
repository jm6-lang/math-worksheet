import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 从服务器搜索蓝天采集器 ===\n")

# 搜索GitHub
stdin, stdout, stderr = ssh.exec_command("curl -s 'https://api.github.com/search/repositories?q=lantian+crawler+OR+%E8%93%9D%E5%A4%A9%E9%87%87%E9%9B%86&per_page=10' 2>/dev/null | python3 -c \"import sys,json; data=json.load(sys.stdin); [print(x.get('html_url',''),x.get('description','')) for x in data.get('items',[])[:5]]\"", timeout=30)
print("GitHub搜索结果:")
print(stdout.read().decode().strip() or "无结果")

# 尝试直接下载
print("\n尝试访问蓝天采集器官网...")
stdin, stdout, stderr = ssh.exec_command("curl -sL --max-time 10 'http://www.lantian.pro' 2>/dev/null | head -c 500", timeout=15)
print(stdout.read().decode('utf-8', errors='ignore').strip() or "无法访问")

ssh.close()
