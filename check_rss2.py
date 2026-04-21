import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 检查RSS源 ===\n")

# 检查36kr RSS内容
cmd = 'curl -s "https://www.36kr.com/feed" | grep -o "<title>[^<]*</title>" | head -10'
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("36kr RSS标题:")
print(stdout.read().decode('utf-8', errors='ignore').strip())

# 检查SSPai RSS
print("\n\nSSPai RSS标题:")
cmd = 'curl -s "https://sspai.com/feed" | grep -o "<title>[^<]*</title>" | head -10'
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode('utf-8', errors='ignore').strip())

# 检查RSS链接是否指向完整文章
print("\n\n检查SSPai RSS链接类型:")
cmd = 'curl -s "https://sspai.com/feed" | grep -o "<link>[^<]*</link>" | head -5'
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode('utf-8', errors='ignore').strip())

ssh.close()
