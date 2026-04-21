import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查采集规则 ===\n")

# 检查规则配置
print("1. 采集规则配置:")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'SELECT id, name, type, config FROM skycaiji_rule;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
result = stdout.read().decode().strip()
print(result if result else "无规则")

# 检查发布配置
print("\n2. 发布配置:")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'SELECT id, task_id, name, module, config FROM skycaiji_release;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 检查任务配置
print("\n3. 任务配置:")
cmd = "mysql -u skycaiji -p'SkyCaiJi2024!' skycaiji -e 'SELECT id, name, config FROM skycaiji_task;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
result = stdout.read().decode().strip()
print(result[:500] if len(result) > 500 else result)

# 手动触发采集
print("\n4. 手动触发采集...")
cmd = "curl -s 'http://caiji.skillxm.cn/index.php?s=/admin/task/run/id/1' 2>/dev/null | head -50"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode('utf-8', errors='ignore').strip()[:300])

ssh.close()
