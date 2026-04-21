import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 执行网站优化 ===\n")

# 1. 清理数据库垃圾数据
print("1. 清理数据库...")
commands = [
    "cd /www/wwwroot/resource_site && wp db optimize --allow-root",
    "cd /www/wwwroot/resource_site && wp post delete --force $(wp post list --post_type=revision --format=ids --allow-root) --allow-root 2>/dev/null",
    "cd /www/wwwroot/resource_site && wp transient delete --expired --allow-root",
]
for cmd in commands:
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)

# 2. 清理WP-Super-Cache缓存
print("2. 清理页面缓存...")
stdin, stdout, stderr = ssh.exec_command("rm -rf /www/wwwroot/resource_site/wp-content/cache/*.php /www/wwwroot/resource_site/wp-content/cache/*/*.php 2>/dev/null", timeout=30)

# 3. 清理缩略图
print("3. 清理未使用的媒体文件...")
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && wp media cleanup --force --allow-root 2>/dev/null", timeout=60)

# 4. 优化nginx配置 - 添加更多缓存头
print("4. 优化nginx配置...")

nginx_config = '''server {
    listen 80;
    server_name skillxm.cn www.skillxm.cn;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name skillxm.cn www.skillxm.cn;
    
    ssl_certificate /etc/letsencrypt/live/skillxm.cn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/skillxm.cn/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    
    root /www/wwwroot/resource_site;
    index index.php index.html index.htm;

    client_max_body_size 50M;
    
    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 16 8k;
    gzip_http_version 1.1;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;
    gzip_min_length 256;
    
    # 静态资源长期缓存
    location ~* \\.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # HTML短期缓存
    location ~* \\.html$ {
        expires 1h;
        add_header Cache-Control "no-cache";
    }
    
    # 禁止访问敏感文件
    location ~ /(\\.user\\.ini|\\.htaccess|wp-config\\.php) {
        deny all;
    }
    
    # WordPress固定链接
    location / {
        try_files $uri $uri/ /index.php?$args;
    }
    
    # PHP处理
    location ~ \\.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
        fastcgi_buffering on;
        fastcgi_buffer_size 128k;
        fastcgi_buffers 256 16k;
        fastcgi_busy_buffers_size 256k;
    }
    
    access_log /var/log/nginx/resource_site.access.log combined buffer=32k;
    error_log /var/log/nginx/resource_site.error.log warn;
}
'''

sftp = ssh.open_sftp()
with sftp.open('/etc/nginx/sites-enabled/resource_site.conf', 'w') as f:
    f.write(nginx_config)
sftp.close()
print("   nginx配置已优化")

# 5. 测试并重载nginx
stdin, stdout, stderr = ssh.exec_command("nginx -t && systemctl reload nginx && echo 'nginx重载成功'", timeout=15)
print("5.", stdout.read().decode().strip())

# 6. 重启PHP-FPM以应用新配置
stdin, stdout, stderr = ssh.exec_command("systemctl restart php8.1-fpm && echo 'PHP-FPM重启成功'", timeout=15)
print("6.", stdout.read().decode().strip())

# 7. 清理WordPress对象缓存
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && wp cache flush --allow-root && echo '对象缓存已清理'", timeout=15)
print("7.", stdout.read().decode().strip())

# 8. 测试网站
stdin, stdout, stderr = ssh.exec_command("curl -sL -o /dev/null -w '%{http_code}' https://skillxm.cn/", timeout=15)
status = stdout.read().decode().strip()
print(f"\n网站状态: HTTP {status}")

# 9. 获取响应时间
import time
time.sleep(1)
stdin, stdout, stderr = ssh.exec_command("curl -sL -o /dev/null -w '响应时间: %{time_total}s' https://skillxm.cn/", timeout=15)
print(stdout.read().decode().strip())

ssh.close()
print("\n=== 优化完成 ===")
