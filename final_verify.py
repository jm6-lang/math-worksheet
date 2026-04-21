import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 最终验证 ===\n")

# 验证所有配置
print("1. 任务组:")
cmd = "mysql -u skycaiji -pSkyCaiJi2024! skycaiji -e 'SELECT * FROM skycaiji_taskgroup;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

print("\n2. 采集规则:")
cmd = "mysql -u skycaiji -pSkyCaiJi2024! skycaiji -e 'SELECT id, name, type FROM skycaiji_rule;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

print("\n3. 发布配置:")
cmd = "mysql -u skycaiji -pSkyCaiJi2024! skycaiji -e 'SELECT id, name, module, task_id FROM skycaiji_release;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

print("\n4. 采集任务:")
cmd = "mysql -u skycaiji -pSkyCaiJi2024! skycaiji -e 'SELECT id, name, auto FROM skycaiji_task;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

print("\n5. 定时任务:")
cmd = "mysql -u skycaiji -pSkyCaiJi2024! skycaiji -e 'SELECT * FROM skycaiji_task_timer;' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

print("\n6. 系统定时任务:")
cmd = "crontab -l 2>/dev/null | grep caiji"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

ssh.close()

print("\n" + "="*60)
print("天空采集器配置完成!")
print("="*60)
print("\n访问地址: http://caiji.skillxm.cn")
print("后台登录: admin / admin123")
print("\n采集任务:")
print("  - 任务组: 网赚教程")
print("  - 采集规则: EasyRule")
print("  - 定时: 每天6条")
print("  - 发布: WordPress")
print("\n请登录后台完善具体的采集规则配置")
