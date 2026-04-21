import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 获取蓝天采集器官网信息 ===\n")

# 获取网站内容
stdin, stdout, stderr = ssh.exec_command("curl -sL --max-time 15 'http://www.lantian.pro' 2>/dev/null | grep -i 'download\|github\|源码\|开源\|php' | head -20", timeout=20)
print("下载链接:")
print(stdout.read().decode('utf-8', errors='ignore').strip())

# 搜索蓝天采集器官网
stdin, stdout, stderr = ssh.exec_command("curl -sL --max-time 15 'https://www.bing.com/search?q=%E8%93%9D%E5%A4%A9%E9%87%87%E9%9B%86%E5%99%A8+site:github.com' 2>/dev/null | grep -o 'href=\"[^\"]*\"' | grep github | head -10", timeout=20)
print("\nGitHub上的蓝天采集器:")
print(stdout.read().decode('utf-8', errors='ignore').strip())

# 尝试直接搜索
stdin, stdout, stderr = ssh.exec_command("curl -sL --max-time 15 'http://www.lantian.pro/download.html' 2>/dev/null | head -c 2000", timeout=20)
print("\n下载页面:")
print(stdout.read().decode('utf-8', errors='ignore').strip())

ssh.close()
