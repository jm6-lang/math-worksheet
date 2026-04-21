import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Find and remove lock files
print("=== Find lock files ===")
stdin, out, err = c.exec_command('find / -name "*.lock" -path "*certbot*" 2>/dev/null')
print(out.read().decode())

# Check for certbot process
print("\n=== Check processes ===")
stdin, out, err = c.exec_command('ps aux | grep certbot | grep -v grep')
print(out.read().decode())

# Try with webroot method
print("\n=== Try webroot method ===")
stdin, out, err = c.exec_command('mkdir -p /var/www/html/.well-known/acme-challenge')
print(out.read().decode())

# Update nginx config for webroot
print("\n=== Update nginx config ===")
nginx_conf = '''server {
    listen 80;
    server_name skillxm.cn www.skillxm.cn 43.103.5.46;
    
    root /www/wwwroot/skillxm.cn/public;
    index index.php index.html index.htm;
    
    location /.well-known/acme-challenge {
        root /var/www/html;
    }
    
    location / {
        try_files $uri $uri/ /index.php?$args;
    }
    
    location ~ \\.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}'''

stdin, out, err = c.exec_command('cat > /etc/nginx/sites-available/skillxm.cn.conf << \'EOF\'\n' + nginx_conf + '\nEOF')
print(out.read().decode())

stdin, out, err = c.exec_command('nginx -t && systemctl reload nginx')
print(out.read().decode())

c.close()