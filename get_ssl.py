import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Get SSL certificate
print("=== Get SSL certificate ===")
stdin, out, err = c.exec_command('certbot certonly --nginx -d skillxm.cn -d www.skillxm.cn --agree-tos --email admin@skillxm.cn --non-interactive 2>&1')
print(out.read().decode())

# Check cert
print("\n=== Check certificate ===")
stdin, out, err = c.exec_command('ls -la /etc/letsencrypt/live/skillxm.cn/')
print(out.read().decode())

c.close()