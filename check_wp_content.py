import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Check posts
print("=== Posts ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp post list --allow-root 2>&1')
print(out.read().decode())

# Check categories
print("\n=== Categories ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp term list category --allow-root 2>&1')
print(out.read().decode())

# Check menus
print("\n=== Menus ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp menu list --allow-root 2>&1')
print(out.read().decode())

# Check theme options
print("\n=== Theme Options (Puock) ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp option get puock_options --allow-root 2>&1')
print(out.read().decode()[:500])

c.close()