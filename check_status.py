import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查天空采集器状态 ===\n")

# 1. 测试访问
print("1. 测试访问...")
cmd = """curl -s --max-time 10 'http://caiji.skillxm.cn/' 2>/dev/null | grep -o '<title>[^<]*</title>'"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
result = stdout.read().decode().strip()
print("   页面标题:", result)

# 2. 检查数据库
print("\n2. 检查数据库...")
cmd = """mysql -u root -p'Langlang0.' -e "SHOW DATABASES LIKE 'skycaiji';" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("   ", stdout.read().decode().strip())

# 3. 检查数据库表
print("\n3. 检查数据库表...")
cmd = """mysql -u skycaiji -p'SkyCaiJi2024!' -e "USE skycaiji; SHOW TABLES;" 2>/dev/null | head -10"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
tables = stdout.read().decode().strip()
print("   表:", tables[:200] if tables else "无表（未安装）")

# 4. 检查配置文件
print("\n4. 检查配置文件...")
cmd = """ls -la /www/wwwroot/skycaiji/data/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 5. 检查定时任务
print("\n5. 检查定时任务...")
cmd = """crontab -l 2>/dev/null | grep caiji"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
cron = stdout.read().decode().strip()
print("   定时任务:", cron if cron else "未设置")

# 6. 检查安装向导
print("\n6. 检查安装向导状态...")
cmd = """curl -s --max-time 10 'http://caiji.skillxm.cn/' 2>/dev/null | grep -i 'install\|向导\|安装' | head -3"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("   ", stdout.read().decode().strip()[:200] if stdout.read().decode().strip() else "未检测到安装内容")

# 7. 检查是否已完成安装
print("\n7. 检查安装状态...")
cmd = """cat /www/wwwroot/skycaiji/data/config.php 2>/dev/null | head -10"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
config = stdout.read().decode().strip()
print("   配置文件:")
print("   ", config[:300] if config else "无配置文件")

ssh.close()
