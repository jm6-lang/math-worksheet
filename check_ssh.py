import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('240b:4001:278:8402:0:bd18:bd09:af0d', port=22, username='root', password='Langlang0.', timeout=20, allow_agent=False, look_for_keys=False)
stdin, stdout, stderr = c.exec_command('grep -n "Port" /etc/ssh/sshd_config', timeout=10)
print(stdout.read().decode())
c.close()
