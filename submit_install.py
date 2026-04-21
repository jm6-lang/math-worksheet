import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 提交安装表单 ===\n")

# 提交表单
cmd = """curl -sL -X POST 'http://caiji.skillxm.cn/index.php?s=/install/index/step2' \\
  -H 'Content-Type: application/x-www-form-urlencoded' \\
  -H 'Origin: http://caiji.skillxm.cn' \\
  -H 'Referer: http://caiji.skillxm.cn/index.php?s=/install/index/step2' \\
  --data-urlencode 'db_host=localhost' \\
  --data-urlencode 'db_port=3306' \\
  --data-urlencode 'db_name=skycaiji' \\
  --data-urlencode 'db_user=skycaiji' \\
  --data-urlencode 'db_pwd=SkyCaiJi2024!' \\
  --data-urlencode 'db_prefix=sc_' \\
  --data-urlencode 'user_name=admin' \\
  --data-urlencode 'user_pwd=Admin123!' \\
  --data-urlencode 'user_repwd=Admin123!' \\
  --data-urlencode 'user_email=admin@skillxm.cn' \\
  2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
content = stdout.read().decode('utf-8', errors='ignore')

print("响应:", content[:2000])

ssh.close()
