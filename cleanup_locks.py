import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Remove lock files
print("=== Remove lock files ===")
stdin, out, err = c.exec_command('rm -f /var/lib/letsencrypt/.certbot.lock /var/log/letsencrypt/.certbot.lock /etc/letsencrypt/.certbot.lock 2>/dev/null; ls -la /var/lib/letsencrypt/')
print(out.read().decode())

# Check for certbot processes
print("\n=== Check processes ===")
stdin, out, err = c.exec_command('ps aux | grep certbot | grep -v grep')
print(out.read().decode())

c.close()