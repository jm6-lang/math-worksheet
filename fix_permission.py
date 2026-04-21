import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 检查PHP-FPM运行用户
cmd = "ps aux | grep php-fpm | head -5"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print("=== PHP-FPM进程 ===")
print(stdout.read().decode())

# 全面修复WordPress目录权限
cmd3 = '''cd /www/wwwroot/resource_site && chown -R www-data:www-data . && find . -type d -exec chmod 755 {} \\; && find . -type f -exec chmod 644 {} \\; && chmod 644 wp-config.php && echo "权限修复完成"'''
stdin, stdout, stderr = ssh.exec_command(cmd3, timeout=60)
print("\n=== 权限修复 ===")
print(stdout.read().decode())
err = stderr.read().decode()
if err:
    print("错误:", err)

# 重启PHP-FPM
cmd4 = "systemctl restart php8.1-fpm && echo 'PHP-FPM重启成功'"
stdin, stdout, stderr = ssh.exec_command(cmd4, timeout=30)
print("\n=== 重启PHP-FPM ===")
print(stdout.read().decode())

# 测试访问
cmd5 = "curl -s -o /dev/null -w '%{http_code}' https://www.skillxm.cn/"
stdin, stdout, stderr = ssh.exec_command(cmd5, timeout=30)
print("\n=== 首页HTTP状态 ===")
print(stdout.read().decode())

cmd6 = "curl -s -o /dev/null -w '%{http_code}' 'https://www.skillxm.cn/?p=1825'"
stdin, stdout, stderr = ssh.exec_command(cmd6, timeout=30)
print("\n=== 新文章HTTP状态 ===")
print(stdout.read().decode())

# 检查最新nginx错误
cmd7 = "tail -5 /var/log/nginx/error.log 2>/dev/null || tail -5 /www/server/nginx/logs/error.log"
stdin, stdout, stderr = ssh.exec_command(cmd7, timeout=30)
print("\n=== 最新Nginx错误 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
