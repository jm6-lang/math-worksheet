import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 修复配置并创建管理员 ===\n")

# 1. 更新配置文件
print("1. 更新配置文件...")
db_config = """<?php
return array(
    'DB_TYPE' => 'mysql',
    'DB_HOST' => 'localhost',
    'DB_NAME' => 'skycaiji',
    'DB_USER' => 'skycaiji',
    'DB_PWD' => 'SkyCaiJi2024!',
    'DB_PORT' => '3306',
    'DB_PREFIX' => 'skycaiji_',
    'DB_DSN' => '',
    'DB_CHARSET' => 'utf8mb4',
);
"""

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/skycaiji/data/config.php', 'w') as f:
    f.write(db_config)
sftp.close()
print("   配置文件已更新（表前缀改为skycaiji_）")

# 2. 创建管理员
print("\n2. 创建管理员账户...")
admin_sql = """
INSERT INTO skycaiji_user (name, pwd, email, groupid, login_count, last_login_time, last_login_ip, addtime, uptime) 
VALUES ('admin', '21232f297a57a5a743894a0e4a801fc3', 'admin@skillxm.cn', 1, 0, 0, '', 1744108800, 1744108800);
"""
cmd = """mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e "{}" 2>/dev/null""".format(admin_sql.replace('\n', ' '))
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("   ", stdout.read().decode().strip() or "管理员已创建")

# 3. 检查用户表
print("\n3. 检查用户表...")
cmd = """mysql -u skycaiji -p'SkyCaiJi2024!' -e "USE skycaiji; SELECT id, name, email FROM skycaiji_user;" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 4. 测试访问
print("\n4. 测试访问...")
cmd = """curl -sL --max-time 10 'http://caiji.skillxm.cn/' 2>/dev/null | grep -o '<title>[^<]*</title>'"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("   标题:", stdout.read().decode().strip())

# 5. 测试登录
print("\n5. 测试登录页面...")
cmd = """curl -sL --max-time 10 'http://caiji.skillxm.cn/index.php?s=/admin/login' 2>/dev/null | head -20"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode('utf-8', errors='ignore').strip()[:300])

ssh.close()
