import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Kill existing certbot and clear lock
print("=== Kill certbot ===")
stdin, out, err = c.exec_command('pkill -9 certbot; rm -f /run/lock/*.lock')
print(out.read().decode())

# Check if cert exists
print("\n=== Check existing cert ===")
stdin, out, err = c.exec_command('ls -la /etc/letsencrypt/live/skillxm.cn/ 2>/dev/null || echo "no cert"')
print(out.read().decode())

c.close()