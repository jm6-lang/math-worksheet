import paramiko

server = '240b:4001:278:8402:0:bd18:bd09:af0d'
port = 22
user = 'root'
password = 'Langlang0.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server, port=port, username=user, password=password,
               timeout=20, allow_agent=False, look_for_keys=False,
               banner_timeout=20, auth_timeout=20)

def cmd(c):
    stdin, stdout, stderr = client.exec_command(c, timeout=30)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# 检查 PHP 语法
print('[1] 检查 PHP 语法...')
print(cmd('php -l /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php'))

# 查看 Nginx 错误日志
print('\n[2] Nginx 错误日志（最近10行）...')
print(cmd('tail -10 /var/log/nginx/error.log 2>/dev/null || echo "无错误日志"'))

# 查看 PHP-FPM 错误日志
print('\n[3] PHP 错误日志...')
print(cmd('tail -10 /var/log/php8.1-fpm.log 2>/dev/null || tail -10 /var/log/php-fpm/error.log 2>/dev/null || echo "无 PHP 错误日志"'))

# 检查文件末尾是否完整
print('\n[4] 检查文件末尾...')
print(cmd('tail -20 /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php'))

client.close()
