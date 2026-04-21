import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 优化PHP-FPM配置
php_fpm_optimized = '''[www]
user = www-data
group = www-data
listen = /run/php/php8.1-fpm.sock
listen.owner = www-data
listen.group = www-data

pm = dynamic
pm.max_children = 50
pm.start_servers = 5
pm.min_spare_servers = 5
pm.max_spare_servers = 35
pm.max_requests = 500

; 性能优化
request_terminate_timeout = 300
request_slowlog_timeout = 10s
slowlog = /var/log/php-fpm/slow.log

; 内存限制
php_admin_value[memory_limit] = 256M
php_admin_value[max_execution_time] = 300
php_admin_value[max_input_vars] = 3000
'''

# 写入PHP-FPM配置
sftp = ssh.open_sftp()
with sftp.open('/tmp/www_optimized.conf', 'w') as f:
    f.write(php_fpm_optimized)
sftp.close()

commands = [
    "cp /etc/php/8.1/fpm/pool.d/www.conf /etc/php/8.1/fpm/pool.d/www.conf.bak",
    "cp /tmp/www_optimized.conf /etc/php/8.1/fpm/pool.d/www.conf",
    "php-fpm8.1 -t",  # 测试配置
    "systemctl reload php8.1-fpm"
]

print("=== 优化PHP-FPM配置 ===")
for cmd in commands:
    print(f"\n执行: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()
    if output:
        print(f"输出: {output}")
    if error:
        print(f"错误: {error}")

# 优化MySQL/MariaDB
print("\n=== 检查MySQL配置 ===")
stdin, stdout, stderr = ssh.exec_command("cat /etc/mysql/mariadb.conf.d/50-server.cnf 2>/dev/null | grep -E 'innodb_buffer_pool_size|query_cache' | head -10")
print(stdout.read().decode())

ssh.close()
print("\nPHP-FPM优化完成!")