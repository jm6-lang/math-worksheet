import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(
    hostname="240b:4001:278:8402:0:bd18:bd09:af0d",
    username="root",
    password="l95UE5ysF)7.gR",
    timeout=30
)

# Get BT panel info
print("=== 获取宝塔面板信息 ===")
stdin, stdout, stderr = client.exec_command("bt 14")
output = stdout.read().decode('utf-8', errors='ignore')
print(output)

print("\n=== 检查面板端口 ===")
stdin, stdout, stderr = client.exec_command("netstat -tlnp | grep -E '8888|888|80|443'")
print(stdout.read().decode('utf-8', errors='ignore'))

print("\n=== 检查面板状态 ===")
stdin, stdout, stderr = client.exec_command("systemctl status bt 2>/dev/null || /etc/init.d/bt status 2>/dev/null || ps aux | grep -E 'BT-Panel|bt' | grep -v grep")
print(stdout.read().decode('utf-8', errors='ignore'))

client.close()