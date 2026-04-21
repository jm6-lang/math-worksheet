import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)
    stdin, stdout, stderr = client.exec_command('echo "成功! 用户: $(whoami)"', timeout=10)
    print(stdout.read().decode('utf-8', errors='replace'))
    client.close()
except Exception as e:
    print(f"旧密码连接失败: {e}")