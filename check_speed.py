import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check Nginx config
stdin, stdout, stderr = ssh.exec_command("cat /etc/nginx/sites-available/resource_site.conf")
nginx_conf = stdout.read().decode()

# Check if gzip is enabled
stdin, stdout, stderr = ssh.exec_command("grep -E 'gzip|brotli' /etc/nginx/nginx.conf /etc/nginx/sites-available/* 2>/dev/null | head -20")
gzip_status = stdout.read().decode()

# Check PHP-FPM config
stdin, stdout, stderr = ssh.exec_command("cat /etc/php/8.1/fpm/pool.d/www.conf | grep -E 'pm\.|max_children' | head -10")
php_fpm = stdout.read().decode()

# Check if caching is enabled
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/resource_site/wp-content/plugins/ | grep -i cache")
cache_plugins = stdout.read().decode()

# Check current response time
stdin, stdout, stderr = ssh.exec_command("curl -o /dev/null -s -w 'Time: %{time_total}s\nCode: %{http_code}\n' http://localhost/")
curl_test = stdout.read().decode()

ssh.close()

print("=== 当前网站配置 ===\n")
print("Nginx配置:")
print(nginx_conf[:1500] if len(nginx_conf) > 1500 else nginx_conf)
print("\n\n压缩状态:")
print(gzip_status if gzip_status else "未配置压缩")
print("\nPHP-FPM配置:")
print(php_fpm if php_fpm else "使用默认配置")
print("\n缓存插件:")
print(cache_plugins if cache_plugins else "未安装缓存插件")
print("\n当前响应时间:")
print(curl_test)