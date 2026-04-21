import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 检查published.db的内容
cmd = """sqlite3 /www/wwwroot/resource_site/auto_collect/published.db ".tables" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=5)
print("表: %s" % stdout.read().decode().strip())

cmd = """sqlite3 /www/wwwroot/resource_site/auto_collect/published.db ".schema" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=5)
print("\n表结构:\n%s" % stdout.read().decode('utf-8', errors='ignore'))

cmd = """sqlite3 /www/wwwroot/resource_site/auto_collect/published.db "SELECT COUNT(*) FROM articles;" 2>/dev/null || sqlite3 /www/wwwroot/resource_site/auto_collect/published.db "SELECT COUNT(*) FROM sqlite_master WHERE type='table';" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=5)
print("\n记录数: %s" % stdout.read().decode().strip())

# 如果有数据，看看内容
cmd = """sqlite3 /www/wwwroot/resource_site/auto_collect/published.db "SELECT * FROM sqlite_master;" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=5)
print("\n完整内容:\n%s" % stdout.read().decode('utf-8', errors='ignore')[:2000])

ssh.close()
