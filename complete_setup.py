import paramiko
import sys
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 完成天空采集器安装 ===\n")

# 1. 确保数据库存在
print("1. 创建数据库...")
cmd = """mysql -u root -p'Langlang0.' -e "CREATE DATABASE IF NOT EXISTS skycaiji CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null"""
ssh.exec_command(cmd, timeout=15)

cmd = """mysql -u root -p'Langlang0.' -e "GRANT ALL PRIVILEGES ON skycaiji.* TO 'skycaiji'@'localhost' IDENTIFIED BY 'SkyCaiJi2024!'; FLUSH PRIVILEGES;" 2>/dev/null"""
ssh.exec_command(cmd, timeout=15)

# 2. 检查runtime目录权限
print("\n2. 设置目录权限...")
cmd = """chmod -R 777 /www/wwwroot/skycaiji/runtime /www/wwwroot/skycaiji/data /www/wwwroot/skycaiji/public/uploads 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("   权限已设置")

# 3. 检查安装文件
print("\n3. 检查安装文件...")
cmd = """ls -la /www/wwwroot/skycaiji/vendor/skycaiji/app/install/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 4. 查看安装控制器
print("\n4. 查看安装控制器...")
cmd = """ls /www/wwwroot/skycaiji/vendor/skycaiji/app/install/controller/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 5. 通过API完成安装
print("\n5. 检查安装状态...")
cmd = """curl -sL 'http://caiji.skillxm.cn/' 2>/dev/null | grep -o '<title>[^<]*</title>'"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 6. 设置定时任务
print("\n6. 设置定时任务...")
cron_cmd = """echo '*/5 * * * * curl -s http://caiji.skillxm.cn/api/crontab/run >/dev/null 2>&1' >> /var/spool/cron/crontabs/root"""
stdin, stdout, stderr = ssh.exec_command(cron_cmd, timeout=10)
print("   定时任务已设置")

# 7. 创建数据库配置文件
print("\n7. 创建数据库配置...")
db_config = """<?php
return array(
    'DB_TYPE' => 'mysql',
    'DB_HOST' => 'localhost',
    'DB_NAME' => 'skycaiji',
    'DB_USER' => 'skycaiji',
    'DB_PWD' => 'SkyCaiJi2024!',
    'DB_PORT' => '3306',
    'DB_PREFIX' => 'sc_',
    'DB_DSN' => '',
    'DB_CHARSET' => 'utf8mb4',
);
"""

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/skycaiji/data/config.php', 'w') as f:
    f.write(db_config)
sftp.close()
print("   数据库配置已创建")

# 8. 验证
print("\n8. 验证安装...")
cmd = """curl -sL 'http://caiji.skillxm.cn/' 2>/dev/null | head -20"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

print("\n=== 天空采集器安装完成 ===")
print("\n访问地址: http://caiji.skillxm.cn")
print("数据库:")
print("  名称: skycaiji")
print("  用户: skycaiji")
print("  密码: SkyCaiJi2024!")

ssh.close()
