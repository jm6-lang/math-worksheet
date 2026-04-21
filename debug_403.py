import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Check directory permissions
print("=== 检查目录 ===")
stdin, out, err = c.exec_command('ls -la /www/wwwroot/')
print(out.read().decode())

stdin, out, err = c.exec_command('ls -la /www/wwwroot/skillxm.cn/')
print(out.read().decode())

# Check if nginx can read
print("=== 检查权限 ===")
stdin, out, err = c.exec_command('ls -la /www/wwwroot/skillxm.cn/public/')
print(out.read().decode())

# Test directly
print("=== 直接访问文件 ===")
stdin, out, err = c.exec_command('cat /www/wwwroot/skillxm.cn/public/index.html | head -5')
print(out.read().decode())

# Check nginx error log
print("=== Nginx错误日志 ===")
stdin, out, err = c.exec_command('tail -20 /var/log/nginx/error.log 2>/dev/null | tail -10')
print(out.read().decode())

c.close()