import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Check apt
stdin, out, err = c.exec_command('apt-get update 2>&1 | tail -5')
print('Update:', out.read().decode())

print("\n=== Install certbot ===")
stdin, out, err = c.exec_command('apt-get install -y certbot python3-certbot-nginx 2>&1 | tail -10')
print(out.read().decode())

c.close()