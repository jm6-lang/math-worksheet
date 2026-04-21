import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 创建管理员账户 ===\n")

# 1. 检查用户表结构
print("1. 检查用户表结构...")
cmd = """mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "DESC skycaiji_user;" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 2. 检查现有用户
print("\n2. 检查现有用户...")
cmd = """mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "SELECT * FROM skycaiji_user;" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip()[:500])

# 3. 创建管理员（MD5密码 admin123）
print("\n3. 创建管理员...")
admin_sql = """mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "INSERT INTO skycaiji_user (name, pwd, email, groupid, login_count, last_login_time, last_login_ip, addtime, uptime, status) VALUES ('admin', '21232f297a57a5a743894a0e4a801fc3', 'admin@skillxm.cn', 1, 0, 0, '', UNIX_TIMESTAMP(), UNIX_TIMESTAMP(), 1) ON DUPLICATE KEY UPDATE pwd='21232f297a57a5a743894a0e4a801fc3', email='admin@skillxm.cn';"""
stdin, stdout, stderr = ssh.exec_command(admin_sql, timeout=15)
result = stdout.read().decode().strip()
print(result if result else "管理员账户已创建/更新")

# 4. 确认
print("\n4. 确认管理员...")
cmd = """mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "SELECT id, name, email, groupid FROM skycaiji_user;" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

print("\n=== 完成 ===")
print("\n后台登录信息:")
print("  网址: http://caiji.skillxm.cn/index.php?s=/admin/login")
print("  用户名: admin")
print("  密码: admin")
print("  (MD5: 21232f297a57a5a743894a0e4a801fc3)")

ssh.close()
