import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查安装结果 ===\n")

# 获取完整页面
cmd = """curl -sL 'http://caiji.skillxm.cn/index.php?s=/install/index/step2' \\
  -X POST \\
  -H 'Content-Type: application/x-www-form-urlencoded' \\
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
  2>/dev/null | grep -E '(成功|完成|错误|失败|安装)' | head -20"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode('utf-8', errors='ignore')
print("关键词:", result[:500])

# 检查数据库表
print("\n数据库表:")
cmd = """mysql -u skycaiji -p'SkyCaiJi2024!' -e "USE skycaiji; SHOW TABLES;" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
tables = stdout.read().decode().strip()
print(tables[:500] if tables else "无表")

# 尝试登录
print("\n尝试访问后台:")
cmd = """curl -sL 'http://caiji.skillxm.cn/index.php?s=/admin' 2>/dev/null | head -20"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode('utf-8', errors='ignore').strip()[:300])

ssh.close()
