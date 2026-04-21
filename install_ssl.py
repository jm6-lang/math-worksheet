import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Install certbot via snap
print("=== Install Certbot ===")
stdin, out, err = c.exec_command('snap install --classic certbot 2>&1')
print(out.read().decode()[:500])

print("\n=== Create symlink ===")
stdin, out, err = c.exec_command('ln -s /snap/bin/certbot /usr/bin/certbot')
print(out.read().decode())

# Get SSL certificate
print("\n=== Get SSL certificate ===")
stdin, out, err = c.exec_command('certbot certonly --nginx -d skillxm.cn -d www.skillxm.cn --agree-tos --email your-email@example.com 2>&1 | tail -20')
print(out.read().decode())

c.close()