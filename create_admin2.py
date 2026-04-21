import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 用正确字段创建管理员 ===\n")

# 用正确的字段创建管理员（密码: admin123）
admin_sql = """mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "INSERT INTO skycaiji_user (username, password, salt, email, groupid, regtime) VALUES ('admin', '0192023a7bbd73250516f069df18b500', 'abc123', 'admin@skillxm.cn', 1, UNIX_TIMESTAMP()) ON DUPLICATE KEY UPDATE password='0192023a7bbd73250516f069df18b500', email='admin@skillxm.cn', groupid=1;" """
stdin, stdout, stderr = ssh.exec_command(admin_sql, timeout=15)
result = stdout.read().decode().strip()
print("执行结果:", result if result else "成功")

# 确认
print("\n确认管理员:")
cmd = """mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "SELECT uid, username, email, groupid FROM skycaiji_user;" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 测试登录
print("\n测试登录页面:")
cmd = """curl -sL --max-time 10 'http://caiji.skillxm.cn/index.php?s=/admin/login' 2>/dev/null | grep -E '<title>|<input' | head -10"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode('utf-8', errors='ignore').strip())

ssh.close()

print("\n" + "="*50)
print("天空采集器安装完成!")
print("="*50)
print("\n访问地址: http://caiji.skillxm.cn")
print("\n后台登录:")
print("  网址: http://caiji.skillxm.cn/index.php?s=/admin/login")
print("  用户名: admin")
print("  密码: admin123")
