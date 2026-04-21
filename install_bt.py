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

# Install BT Panel (宝塔面板)
# Using the standard installation command
install_cmd = "curl -sSO https://download.bt.cn/install/install_panel.sh && bash install_panel.sh -e"

print("开始安装宝塔面板...")
print("这可能需要几分钟，请等待...")

stdin, stdout, stderr = client.exec_command(install_cmd, get_pty=True)

# Read output in a loop
output = ""
while True:
    try:
        line = stdout.channel.recv(4096).decode()
        if not line:
            break
        output += line
        print(line, end='')
        if "bt-panel" in line.lower() or "complete" in line.lower() or "success" in line.lower():
            break
        time.sleep(1)
    except:
        break

print("\n安装完成")

# Check if BT is now installed
stdin, stdout, stderr = client.exec_command("bt --version 2>&1")
print("\n检查宝塔:")
print(stdout.read().decode())

client.close()