import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    # Try IPv4 first, then IPv6
    for ip in ['43.103.5.46', '240b:4001:278:8402:0:bd18:bd09:af0d']:
        try:
            client.connect(ip, 22, 'root', 'Langlang0.', timeout=15)
            stdin, stdout, stderr = client.exec_command('echo "✓ 连接成功! IP: $(hostname -I | awk \'{print $1}\') 用户: $(whoami)"', timeout=10)
            print(f"IP {ip}: {stdout.read().decode('utf-8', errors='replace').strip()}")
            client.close()
            break
        except Exception as e:
            print(f"✗ {ip}: {e}")
            try:
                client.close()
            except:
                pass
except Exception as e:
    print(f"错误: {e}")
