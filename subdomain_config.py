import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 配置采集器子域名 ===\n")

# 1. 恢复原配置并添加子域名
print("1. 恢复原Nginx配置...")
cmd = """cat > /etc/nginx/sites-available/resource_site.conf << 'NGINXEOF'
server {
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
    
    access_log /var/log/nginx/resource_site.access;
}

# 天空采集器独立子域名
server {
    listen 80;
    server_name caiji.skillxm.cn;
    
    root /www/wwwroot/skycaiji/public;
    index index.php index.html;
    
    client_max_body_size 100M;
    
    # 禁止访问敏感文件
    location ~ /(\\.user\\.ini|\\.ht) {
        deny all;
    }
    
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    
    location ~ \\.php$ {
        fastcgi_pass unix:/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
    
    # 静态资源缓存
    location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf)$ {
        expires 7d;
        add_header Cache-Control "public";
    }
}
NGINXEOF
"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("   配置已写入")

# 2. 禁用旧配置
print("\n2. 禁用旧配置...")
ssh.exec_command("rm -f /etc/nginx/sites-enabled/skycaiji.conf", timeout=10)

# 3. 测试Nginx
print("\n3. 测试Nginx...")
stdin, stdout, stderr = ssh.exec_command("nginx -t 2>&1", timeout=10)
print("   ", stdout.read().decode().strip())

# 4. 重载Nginx
print("\n4. 重载Nginx...")
stdin, stdout, stderr = ssh.exec_command("nginx -s reload 2>&1", timeout=10)
print("   ", stdout.read().decode().strip() or "成功")

# 5. 测试访问
print("\n5. 测试访问...")
cmd = """curl -sL --max-time 10 'http://127.0.0.1/' -H 'Host: caiji.skillxm.cn' 2>/dev/null | head -100"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore').strip()
print(content[:800])

ssh.close()
