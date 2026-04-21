import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 查看安装表单 ===\n")

# 获取安装页面完整内容
cmd = """curl -s 'http://caiji.skillxm.cn/index.php?s=/install' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore')

# 查找表单
import re
forms = re.findall(r'<form[^>]*>.*?</form>', content, re.DOTALL)
print("找到表单:", len(forms))

# 查找input字段
inputs = re.findall(r'<input[^>]*>', content)
print("\n表单字段:")
for inp in inputs[:20]:
    name = re.search(r'name=["\']([^"\']+)["\']', inp)
    id = re.search(r'id=["\']([^"\']+)["\']', inp)
    placeholder = re.search(r'placeholder=["\']([^"\']+)["\']', inp)
    print(f"  {name.group(1) if name else '?'} | id={id.group(1) if id else '?'} | placeholder={placeholder.group(1) if placeholder else ''}")

# 查找提交按钮
buttons = re.findall(r'<button[^>]*>[^<]*</button>', content)
print("\n按钮:")
for btn in buttons:
    print(f"  {btn[:100]}")

# 查看是否有PHP错误
print("\n\n完整内容（最后1000字符）:")
print(content[-1000:])

ssh.close()
