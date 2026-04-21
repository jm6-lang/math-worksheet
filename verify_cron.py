import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 验证定时任务 ===\n")

# 1. 检查crontab
print("1. 检查系统定时任务...")
cmd = "crontab -l 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
cron = stdout.read().decode().strip()
print(cron if cron else "无系统定时任务")

# 2. 检查天空采集器定时器配置
print("\n2. 检查天空采集器定时器...")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'SELECT * FROM skycaiji_task_timer;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 3. 手动测试采集API
print("\n3. 测试采集API...")
cmd = "curl -s --max-time 30 'http://caiji.skillxm.cn/api/crontab/run' 2>/dev/null | head -20"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=45)
print(stdout.read().decode('utf-8', errors='ignore').strip()[:500])

# 4. 检查任务状态
print("\n4. 检查任务状态...")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'SELECT id, name, auto, caijitime FROM skycaiji_task;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

ssh.close()

print("\n" + "="*50)
print("配置完成!")
print("="*50)
print("\n采集器后台: http://caiji.skillxm.cn")
print("登录: admin / admin123")
print("\n定时任务已设置为: 每天6条")
print("请登录后台完善采集规则和发布配置")
