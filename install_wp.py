import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Create MySQL database for WordPress
print("=== Create MySQL database ===")
stdin, out, err = c.exec_command('mysql -e "CREATE DATABASE IF NOT EXISTS wp_skillxm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"')
print('DB created:', err.read().decode().strip() if err.read() else 'OK')

# Create MySQL user
stdin, out, err = c.exec_command('mysql -e "CREATE USER IF NOT EXISTS \'wpuser\'@\'localhost\' IDENTIFIED BY \'WpPass2024!\';"')
print('User created:', err.read().decode().strip() if err.read() else 'OK')

stdin, out, err = c.exec_command('mysql -e "GRANT ALL PRIVILEGES ON wp_skillxm.* TO \'wpuser\'@\'localhost\';"')
print('Grant:', err.read().decode().strip() if err.read() else 'OK')

stdin, out, err = c.exec_command('mysql -e "FLUSH PRIVILEGES;"')
print('Flush:', err.read().decode().strip() if err.read() else 'OK')

print("\n=== Database info ===")
print("DB Name: wp_skillxm")
print("User: wpuser")
print("Password: WpPass2024!")

# Download WordPress
print("\n=== Download WordPress ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && curl -O https://wordpress.org/latest.tar.gz')
print(out.read().decode().strip()[:200])

# Extract WordPress
print("\n=== Extract WordPress ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && tar -xzf latest.tar.gz && mv wordpress/* . && rm -rf wordpress latest.tar.gz')
print(out.read().decode().strip()[:200])

print("\n=== Set permissions ===")
stdin, out, err = c.exec_command('chown -R www:www /www/wwwroot/skillxm.cn/public && chmod -R 755 /www/wwwroot/skillxm.cn/public')
print(out.read().decode().strip())

print("\n=== WordPress files ===")
stdin, out, err = c.exec_command('ls -la /www/wwwroot/skillxm.cn/public/ | head -15')
print(out.read().decode())

c.close()
print("\n✅ WordPress 已下载！")
print("访问 http://skillxm.cn 完成安装向导")