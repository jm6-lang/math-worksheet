import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查任务表结构 ===\n")

# 检查任务表
print("1. skycaiji_task 表结构:")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'DESC skycaiji_task;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 检查任务定时器表
print("\n2. skycaiji_task_timer 表结构:")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'DESC skycaiji_task_timer;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 检查规则表
print("\n3. skycaiji_rule 表结构:")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'DESC skycaiji_rule;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 检查采集器表
print("\n4. skycaiji_collector 表结构:")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'DESC skycaiji_collector;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

ssh.close()
