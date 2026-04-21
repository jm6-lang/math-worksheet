import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Test HTTP access
stdin, out, err = c.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost/')
http_code = out.read().decode().strip()
print('HTTP code:', http_code)

# Test content
stdin, out, err = c.exec_command('curl -s http://localhost/ | head -c 200')
content = out.read().decode()
print('Content preview:', content[:200])

c.close()