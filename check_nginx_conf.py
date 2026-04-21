import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Check nginx config files
print("=== Nginx sites-enabled ===")
stdin, out, err = c.exec_command('ls -la /etc/nginx/sites-enabled/')
print(out.read().decode())

print("\n=== Nginx sites-available ===")
stdin, out, err = c.exec_command('ls -la /etc/nginx/sites-available/')
print(out.read().decode())

# Check if our config exists
print("\n=== Check our config ===")
stdin, out, err = c.exec_command('cat /etc/nginx/sites-available/skillxm.cn.conf 2>/dev/null | head -20')
print(out.read().decode())

# Check default config
print("\n=== Default nginx config ===")
stdin, out, err = c.exec_command('cat /etc/nginx/sites-enabled/default 2>/dev/null | head -30')
print(out.read().decode())

c.close()