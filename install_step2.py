import paramiko
import sys
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 完成安装向导 Step 2 ===\n")

# Step 2: 数据库配置
print("1. 进入Step2...")
cmd = """curl -sL 'http://caiji.skillxm.cn/index.php?s=/install/index/step2' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore')

# 查找表单和字段
inputs = re.findall(r'<input[^>]*>', content)
print("表单字段:")
for inp in inputs:
    name = re.search(r'name=["\']([^"\']+)["\']', inp)
    placeholder = re.search(r'placeholder=["\']([^"\']+)["\']', inp)
    value = re.search(r'value=["\']([^"\']*)["\']', inp)
    if name:
        print(f"  {name.group(1)}: value={value.group(1) if value else ''} placeholder={placeholder.group(1) if placeholder else ''}")

# 查找提交按钮
buttons = re.findall(r'<button[^>]*>[^<]*</button>|<a[^>]*>[^<]*(?:下一步|提交|完成)[^<]*</a>', content)
print("\n按钮:", buttons[:5] if buttons else "无")

# 查找表单action
form = re.search(r'<form[^>]*action=["\']([^"\']*)["\'][^>]*>', content)
if form:
    print(f"\n表单action: {form.group(1)}")

# 查看内容
print("\n内容预览:")
print(content[:1500])

ssh.close()
