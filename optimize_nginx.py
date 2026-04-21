import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 1. 优化Nginx配置
nginx_optimized = '''server {
    listen 80;
    server_name skillxm.cn www.skillxm.cn;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name skillxm.cn www.skillxm.cn;
    
    ssl_certificate /etc/letsencrypt/live/skillxm.cn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/skillxm.cn/privkey.pem;
    
    # SSL优化
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    
    root /www/wwwroot/resource_site;
    index index.php index.html index.htm;

    client_max_body_size 50M;
    
    # 开启gzip压缩
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_buffers 16 8k;
    gzip_http_version 1.1;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;
    gzip_min_length 256;
    
    # 浏览器缓存静态资源
    location ~* \\.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {
        expires 6M;
        add_header Cache-Control "public, immutable";
        access_log off;
    }
    
    # 禁止访问敏感文件
    location ~ /\\. {
        deny all;
    }
    
    location ~ /(wp-config\\.php|wp-admin/install\\.php) {
        deny all;
    }

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \\.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
        
        # PHP-FPM优化
        fastcgi_buffering on;
        fastcgi_buffer_size 4k;
        fastcgi_buffers 8 4k;
        fastcgi_busy_buffers_size 8k;
    }
    
    # 日志优化
    access_log /var/log/nginx/resource_site.access.log combined buffer=32k;
    error_log /var/log/nginx/resource_site.error.log warn;
}
'''

# 写入优化后的配置
sftp = ssh.open_sftp()
with sftp.open('/tmp/nginx_optimized.conf', 'w') as f:
    f.write(nginx_optimized)
sftp.close()

# 备份原配置并应用新配置
commands = [
    "cp /etc/nginx/sites-available/resource_site.conf /etc/nginx/sites-available/resource_site.conf.bak",
    "cp /tmp/nginx_optimized.conf /etc/nginx/sites-available/resource_site.conf",
    "nginx -t",  # 测试配置
    "systemctl reload nginx"
]

print("=== 优化Nginx配置 ===")
for cmd in commands:
    print(f"\n执行: {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode()
    error = stderr.read().decode()
    if output:
        print(f"输出: {output}")
    if error:
        print(f"错误: {error}")

ssh.close()
print("\nNginx配置优化完成!")