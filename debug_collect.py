import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查采集问题 ===\n")

# 1. 检查天空采集器日志
print("1. 检查天空采集器日志...")
cmd = "tail -30 /www/wwwroot/skycaiji/runtime/log/202604/*.log 2>/dev/null | tail -50"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode('utf-8', errors='ignore').strip()[-2000:] if stdout.read().decode('utf-8', errors='ignore').strip() else "无日志")

# 2. 检查已采集的文章
print("\n2. 检查已采集的文章...")
cmd = "mysql -u skycaiji -pSkyCaiJi2024! skycaiji -e 'SELECT COUNT(*) as total FROM skycaiji_collected;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 3. 检查采集配置是否正确
print("\n3. 检查任务配置...")
cmd = "mysql -u skycaiji -pSkyCaiJi2024! skycaiji -e 'SELECT * FROM skycaiji_task;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 4. 检查规则配置
print("\n4. 检查规则配置...")
cmd = "mysql -u skycaiji -pSkyCaiJi2024! skycaiji -e 'SELECT * FROM skycaiji_rule;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 5. 测试手动采集
print("\n5. 测试手动采集...")
cmd = "curl -s 'http://caiji.skillxm.cn/index.php?s=/admin/task/run/id/1' 2>/dev/null | head -30"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode('utf-8', errors='ignore').strip()[:500])

ssh.close()
