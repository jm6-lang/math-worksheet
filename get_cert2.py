import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Kill stuck certbot processes
print("=== Kill processes ===")
stdin, out, err = c.exec_command('kill -9 37648 37649 2>/dev/null; sleep 2; ps aux | grep certbot | grep -v grep || echo "no certbot process"')
print(out.read().decode())

# Get SSL certificate
print("\n=== Get SSL certificate ===")
stdin, out, err = c.exec_command('certbot certonly --webroot -w /var/www/html -d skillxm.cn -d www.skillxm.cn --agree-tos --email admin@skillxm.cn --non-interactive 2>&1')
print(out.read().decode())

# Check certificate
print("\n=== Check certificate ===")
stdin, out, err = c.exec_command('ls -la /etc/letsencrypt/live/skillxm.cn/ 2>/dev/null || echo "no cert yet"')
print(out.read().decode())

c.close()