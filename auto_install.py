import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 自动完成天空采集器安装 ===\n")

# 1. 检查安装控制器
print("1. 检查安装API...")
cmd = """curl -s 'http://caiji.skillxm.cn/index.php?s=/install/check' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("   ", stdout.read().decode().strip()[:200])

# 2. 检查安装页面
print("\n2. 检查安装页面...")
cmd = """curl -s 'http://caiji.skillxm.cn/index.php?s=/install' 2>/dev/null | head -30"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore')
print(content[:500])

# 3. 尝试提交安装
print("\n3. 尝试提交安装表单...")
install_cmd = """curl -s -X POST 'http://caiji.skillxm.cn/index.php?s=/install/checkDb' \\
  -H 'Content-Type: application/x-www-form-urlencoded' \\
  -d 'db_host=localhost&db_name=skycaiji&db_user=skycaiji&db_pwd=SkyCaiJi2024!&db_port=3306&db_prefix=sc_' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(install_cmd, timeout=15)
print("   ", stdout.read().decode().strip()[:300])

ssh.close()
