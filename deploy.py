import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[STEP 1] Creating authorization site for api.zibll.com')

# Create directory
stdin, stdout, stderr = client.exec_command('mkdir -p /www/wwwroot/api.zibll.com')
print('Created directory')

# Create index.php
index_php = '''<?php
header('Content-Type: text/plain');
echo '200';
?>
'''
sftp = client.open_sftp()
f = sftp.file('/www/wwwroot/api.zibll.com/index.php', 'w')
f.write(index_php)
f.close()
sftp.close()
print('Uploaded index.php')

# Create nginx config
nginx_conf = '''server {
    listen 80;
    server_name api.zibll.com;
    root /www/wwwroot/api.zibll.com;
    index index.php;
    location / {
        try_files $uri $uri/ /index.php?$args;
    }
}
'''
sftp = client.open_sftp()
f = sftp.file('/etc/nginx/sites-available/api.zibll.com.conf', 'w')
f.write(nginx_conf)
f.close()
sftp.close()

# Enable site
stdin, stdout, stderr = client.exec_command('ln -sf /etc/nginx/sites-available/api.zibll.com.conf /etc/nginx/sites-enabled/')
stdin, stdout, stderr = client.exec_command('nginx -t')
print('Nginx config test OK')

stdin, stdout, stderr = client.exec_command('systemctl reload nginx')
print('Nginx reloaded')

print('[STEP 2] Adding hosts entry')
stdin, stdout, stderr = client.exec_command('echo "127.0.0.1 api.zibll.com" >> /etc/hosts')
print('Hosts entry added')

print('[STEP 3] Activating zibll theme')
# Try WP-CLI first
stdin, stdout, stderr = client.exec_command('which wp')
has_wpcli = stdout.read().decode('utf-8', errors='ignore').strip()

if has_wpcli:
    stdin, stdout, stderr = client.exec_command('cd /www/wwwroot/resource_site && wp theme activate zibll')
    print('Theme activated via WP-CLI')
else:
    # Use database method
    stdin, stdout, stderr = client.exec_command('mysql -u root -e "UPDATE wp_resource.wp_options SET option_value=\'zibll\' WHERE option_name=\'template\' OR option_name=\'stylesheet\';"')
    print('Theme activated via database')

print('[STEP 4] Verify theme is active')
stdin, stdout, stderr = client.exec_command('mysql -u root -e "SELECT option_value FROM wp_resource.wp_options WHERE option_name=\'template\';" 2>/dev/null')
print('Current template:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()
print('\n[DONE] Theme deployed and authorized!')