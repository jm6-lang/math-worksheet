import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

def run(cmd, t=15):
    _, o, _ = client.exec_command(cmd, timeout=t)
    try: return o.read().decode('utf-8', errors='replace').strip()
    except: return '[TIMEOUT]'

print(run('rm -f /tmp/wp_login_result.html'))
out = run('ls /tmp/ 2>/dev/null')
print(f'/tmp final:\n{out}')

client.close()
