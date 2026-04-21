import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 配置WP Super Cache
commands = [
    # 在wp-config.php中启用缓存
    "cd /www/wwwroot/resource_site && grep -q 'WP_CACHE' wp-config.php || sed -i \"/define( 'DB_COLLATE'/a define('WP_CACHE', true);\" wp-config.php",
    
    # 检查配置
    "cd /www/wwwroot/resource_site && grep WP_CACHE wp-config.php",
    
    # 确保advanced-cache.php存在
    "cd /www/wwwroot/resource_site && ls -la wp-content/advanced-cache.php",
    
    # 创建缓存目录
    "mkdir -p /www/wwwroot/resource_site/wp-content/cache/supercache && chown -R www-data:www-data /www/wwwroot/resource_site/wp-content/cache",
    
    # 测试缓存是否工作
    "curl -s -I http://localhost/ | grep -E 'X-WP-Super-Cache|Cache|Age'"
]

print("=== 配置WP Super Cache ===")
for cmd in commands:
    print(f"\n执行: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()
    if output:
        print(f"输出: {output}")
    if error:
        print(f"错误: {error}")

# 测试响应时间
print("\n=== 测试优化后的响应时间 ===")
stdin, stdout, stderr = ssh.exec_command("curl -o /dev/null -s -w 'Time: %{time_total}s\n' http://localhost/")
print(stdout.read().decode())

ssh.close()