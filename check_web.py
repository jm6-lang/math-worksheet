import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Check website status
stdin, out, err = c.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost/')
print('Website HTTP:', out.read().decode().strip())

# Check directory
stdin, out, err = c.exec_command('ls -la /www/wwwroot/')
print('\n/www/wwwroot/ contents:')
print(out.read().decode())

# Check domain binding
stdin, out, err = c.exec_command('cat /www/server/panel/vhost/nginx/*.conf 2>/dev/null | grep -E "server_name|listen" | head -20')
print('\nNginx vhost configs:')
print(out.read().decode())

c.close()