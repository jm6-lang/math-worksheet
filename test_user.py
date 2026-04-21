import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Try different usernames
usernames = ['root', 'admin', 'ubuntu', 'user']
password = 'Langlang0'

for user in usernames:
    try:
        client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, user, password, timeout=10)
        stdin, stdout, stderr = client.exec_command('echo "成功! 用户: $(whoami)"', timeout=10)
        print(f"✓ {user}: {stdout.read().decode('utf-8', errors='replace').strip()}")
        client.close()
        break
    except Exception as e:
        print(f"✗ {user}: {e}")
        try:
            client.close()
        except:
            pass