import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 配置天空采集器 ===\n")

# 1. 安装PHP依赖
print("1. 安装PHP依赖 (composer)...")
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/skycaiji && composer install --no-dev --optimize-autoloader 2>&1 | tail -20", timeout=120)
print(stdout.read().decode().strip())

# 2. 设置目录权限
print("\n2. 设置目录权限...")
ssh.exec_command("chmod -R 755 /www/wwwroot/skycaiji", timeout=10)
ssh.exec_command("chmod -R 777 /www/wwwroot/skycaiji/runtime", timeout=10)
ssh.exec_command("chmod -R 777 /www/wwwroot/skycaiji/public/uploads", timeout=10)
ssh.exec_command("chmod -R 777 /www/wwwroot/skycaiji/data", timeout=10)
print("   权限设置完成")

# 3. 检查PHP扩展
print("\n3. 检查PHP扩展...")
cmd = """php -m | grep -E 'pdo|mysqli|curl|gd|mbstring|json|xml'"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("   已安装:", stdout.read().decode().strip())

# 4. 创建数据库
print("\n4. 创建数据库...")
cmd = """mysql -u root -p'Langlang0.' -e "CREATE DATABASE IF NOT EXISTS skycaiji CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; SHOW DATABASES LIKE 'skycaiji';" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
result = stdout.read().decode().strip()
print("   ", result)

# 5. 创建数据库用户
print("\n5. 创建数据库用户...")
cmd = """mysql -u root -p'Langlang0.' -e "CREATE USER IF NOT EXISTS 'skycaiji'@'localhost' IDENTIFIED BY 'SkyCaiJi2024!'; GRANT ALL PRIVILEGES ON skycaiji.* TO 'skycaiji'@'localhost'; FLUSH PRIVILEGES;" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("   数据库用户创建完成")

# 6. 配置Nginx
print("\n6. 配置Nginx...")
nginx_config = """server {
    listen 80;
    server_name skycaiji.skillxm.cn;
    root /www/wwwroot/skycaiji/public;
    index index.php index.html;
    
    client_max_body_size 100M;
    client_body_buffer_size 1m;
    
    access_log /var/log/nginx/skycaiji_access.log;
    error_log /var/log/nginx/skycaiji_error.log;
    
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    
    location ~ \\.php$ {
        fastcgi_pass unix:/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
        fastcgi_buffer_size 128k;
        fastcgi_buffers 4 256k;
        fastcgi_busy_buffers_size 256k;
    }
    
    location ~ /\\. {
        deny all;
    }
    
    location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
"""

sftp = ssh.open_sftp()
with sftp.open('/etc/nginx/sites-available/skycaiji.conf', 'w') as f:
    f.write(nginx_config)
sftp.close()
print("   Nginx配置已写入")

# 7. 启用站点并测试
print("\n7. 启用站点...")
stdin, stdout, stderr = ssh.exec_command("ln -sf /etc/nginx/sites-available/skycaiji.conf /etc/nginx/sites-enabled/skycaiji.conf && nginx -t", timeout=10)
print("   ", stdout.read().decode().strip())

# 8. 重载Nginx
stdin, stdout, stderr = ssh.exec_command("nginx -s reload 2>&1", timeout=10)
print("   Nginx重载:", stdout.read().decode().strip() or "成功")

# 9. 检查安装状态
print("\n9. 检查安装...")
cmd = "curl -sL --max-time 10 'http://localhost/' -o /dev/null -w '%{http_code}' 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("   本地访问状态:", stdout.read().decode().strip())

# 10. 设置定时任务
print("\n10. 设置定时任务...")
cron_cmd = "echo '*/5 * * * * curl -s http://skycaiji.skillxm.cn/api/crontab/run > /dev/null 2>&1' >> /var/spool/cron/crontabs/root"
stdin, stdout, stderr = ssh.exec_command(cron_cmd, timeout=10)
print("   定时任务已设置 (每5分钟执行)")

print("\n=== 天空采集器安装完成 ===")
print("\n访问地址: http://skycaiji.skillxm.cn")
print("首次访问会自动跳转到安装向导")
print("\n请在浏览器中完成以下步骤:")
print("1. 访问 http://skycaiji.skillxm.cn")
print("2. 按照向导填写数据库信息:")
print("   数据库: skycaiji")
print("   用户名: skycaiji")
print("   密码: SkyCaiJi2024!")
print("3. 完成安装后即可使用")

ssh.close()
