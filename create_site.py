import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Try to create site using BT CLI
# First check if we can run bt commands
stdin, out, err = c.exec_command('cd /www/server/panel && python3 tools.py panel panel_brute_prod test 2>&1 | head -20')
print('BT tools test:', out.read().decode())

# Check BT API
stdin, out, err = c.exec_command('ls -la /www/server/panel/class/ | grep -E "api|site" | head -10')
print('\nBT classes:', out.read().decode())

c.close()