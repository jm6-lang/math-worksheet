import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 彻底清理并重启 ===\n")

# 1. 杀死所有nginx进程
print("1. 杀死所有nginx...")
stdin, stdout, stderr = ssh.exec_command("pkill -9 nginx; pkill -9 php-fpm; sleep 2; ps aux | grep nginx | grep -v grep", timeout=15)
print(stdout.read().decode().strip() or "无nginx进程")

# 2. 检查端口占用
print("\n2. 检查端口80和443...")
cmd = """netstat -tlnp 2>/dev/null | grep -E ':(80|443) ' || ss -tlnp | grep -E ':(80|443) '"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip() or "端口空闲")

# 3. 启动PHP-FPM
print("\n3. 启动PHP-FPM...")
stdin, stdout, stderr = ssh.exec_command("php-fpm8.1 2>&1 &", timeout=10)
print(stdout.read().decode().strip() or "PHP-FPM已启动")

# 4. 启动Nginx
print("\n4. 启动Nginx...")
stdin, stdout, stderr = ssh.exec_command("nginx 2>&1", timeout=10)
print(stdout.read().decode().strip() or "Nginx已启动")

# 5. 确认进程
print("\n5. 确认进程...")
cmd = """ps aux | grep -E 'nginx|php' | grep -v grep | head -5"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 6. 测试skycaiji
print("\n6. 测试skycaiji...")
cmd = """curl -sL --max-time 10 'http://127.0.0.1/' -H 'Host: caiji.skillxm.cn' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore')
print("响应长度:", len(content))
if len(content) > 100:
    if "skycaiji" in content.lower() or "天空" in content or "采集" in content:
        print("✓ 天空采集器!")
    print(content[:300])

ssh.close()
