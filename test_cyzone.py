import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 测试创业邦 ===\n")

# 获取RSS
cmd = 'curl -sL "https://www.cyzone.cn/rss/" --max-time 15 | head -c 2000'
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
print("RSS内容:")
rss = stdout.read().decode('utf-8', errors='ignore')
print(rss[:1500])

# 提取文章链接
import re
links = re.findall(r'<link>([^<]+)</link>', rss)
print(f"\n找到 {len(links)} 个链接")
if links:
    print("示例链接:", links[:3])

# 测试文章
if links:
    test_url = links[0]
    print(f"\n测试文章: {test_url}")
    cmd = f'curl -sL "{test_url}" --max-time 15 -H "User-Agent: Mozilla/5.0" | head -c 500'
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
    print("响应:", stdout.read().decode('utf-8', errors='ignore')[:500])

ssh.close()
