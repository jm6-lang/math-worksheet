import paramiko
import time

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(
    hostname="240b:4001:278:8402:0:bd18:bd09:af0d",
    username="root",
    password="l95UE5ysF)7.gR",
    timeout=30
)

# Check BT installation in different ways
commands = [
    ("whereis bt", "whereis bt"),
    ("find bt", "find /www -name 'bt*' 2>/dev/null | head -20"),
    ("check port 8888", "netstat -tlnp | grep 8888"),
    ("check bt default path", "ls -la /www/ 2>/dev/null || echo 'no /www'"),
    ("ps aux | grep bt", "ps aux | grep -E 'bt|panel' | grep -v grep"),
]

for name, cmd in commands:
    stdin, stdout, stderr = client.exec_command(cmd)
    output = stdout.read().decode().strip()
    err = stderr.read().decode().strip()
    print(f"=== {name} ===")
    print(output[:800])
    if err:
        print(f"Error: {err[:200]}")
    print()

# Try interactive BT install
print("尝试非交互式安装...")
stdin, stdout, stderr = client.exec_command(
    "echo 'y' | bash install_panel.sh 2>&1 | tail -50",
    get_pty=True
)
time.sleep(30)
output = stdout.read().decode()
print(output[-2000:])

client.close()