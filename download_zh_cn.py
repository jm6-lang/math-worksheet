import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Download Chinese language pack
print("=== Download Chinese language pack ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public/wp-content && curl -O https://downloads.wordpress.org/translation/core/6.9.4/zh_CN.zip 2>&1')
print(out.read().decode()[:500])

# Extract
print("\n=== Extract ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public/wp-content && unzip -o zh_CN.zip 2>&1')
print(out.read().decode()[:300])

# Check languages directory
print("\n=== Check languages ===")
stdin, out, err = c.exec_command('ls -la /www/wwwroot/skillxm.cn/public/wp-content/languages/')
print(out.read().decode())

c.close()