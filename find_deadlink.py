import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 找一个不存在的URL，确认返回404
print("=== 查找死链 ===\n")

# 1. 先测试一个肯定不存在的URL
print("1. 测试404页面:")
cmd = """curl -sI 'https://www.skillxm.cn/this-page-does-not-exist-12345.html' -k 2>/dev/null | head -3"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 2. 构造一个看起来合理的死链
print("\n2. 生成的死链URL:")
dead_links = [
    "https://www.skillxm.cn/post/deleted-article-404.html",
    "https://www.skillxm.cn/old-resource-removed.html",
    "https://www.skillxm.cn/category/removed-page.html",
]

for url in dead_links:
    cmd = f"""curl -sI '{url}' -k 2>/dev/null | head -1"""
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    status = stdout.read().decode().strip()
    print(f"  {url} -> {status}")

ssh.close()

print("\n给你一条死链（404）：")
print("https://www.skillxm.cn/this-page-does-not-exist-12345.html")
