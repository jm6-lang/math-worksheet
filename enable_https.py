import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Create nginx config with SSL
nginx_conf = '''server {
    listen 80;
    server_name skillxm.cn www.skillxm.cn;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name skillxm.cn www.skillxm.cn;

    ssl_certificate /etc/letsencrypt/live/skillxm.cn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/skillxm.cn/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    root /www/wwwroot/skillxm.cn/public;
    index index.php index.html index.htm;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \\.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\\.ht {
        deny all;
    }
}'''

print("=== Write nginx config ===")
stdin, out, err = c.exec_command('cat > /etc/nginx/sites-available/skillxm.cn.conf << \'EOF\'\n' + nginx_conf + '\nEOF')
print(out.read().decode())

# Enable site
print("\n=== Enable site ===")
stdin, out, err = c.exec_command('ln -sf /etc/nginx/sites-available/skillxm.cn.conf /etc/nginx/sites-enabled/')
print(out.read().decode())

# Test and reload nginx
print("\n=== Test nginx ===")
stdin, out, err = c.exec_command('nginx -t')
print(out.read().decode())

print("\n=== Reload nginx ===")
stdin, out, err = c.exec_command('systemctl reload nginx')
print(out.read().decode())

c.close()
print("\n✅ HTTPS 已配置完成！")