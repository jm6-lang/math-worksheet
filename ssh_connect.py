import paramiko
import socket
import time
import sys

# Server config
HOST = "240b:4001:278:8402:0:bd18:bd09:af0d"
PORT = 22
USERNAME = "root"
PASSWORD = "l95UE5ysF)7.gR"

print(f"Connecting to {HOST}:{PORT}...")

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Try connecting
    client.connect(
        hostname=HOST,
        port=PORT,
        username=USERNAME,
        password=PASSWORD,
        timeout=30,
        allow_agent=False,
        look_for_keys=False
    )
    
    print("[OK] Connected! Running test command...")
    
    # Execute test command
    stdin, stdout, stderr = client.exec_command("uname -a && echo '---' && whoami && echo '---' && ls -la /www/wwwroot 2>/dev/null || echo 'No /www/wwwroot'")
    
    output = stdout.read().decode('utf-8', errors='ignore')
    error = stderr.read().decode('utf-8', errors='ignore')
    
    print(output)
    if error:
        print("STDERR:", error)
    
    # Check if theme directory exists
    stdin, stdout, stderr = client.exec_command("ls -la /www/wwwroot/ 2>/dev/null | head -20")
    print("\n[DIR] Sites in /www/wwwroot/:")
    print(stdout.read().decode('utf-8', errors='ignore'))
    
    client.close()
    print("\n[OK] SSH connection successful!")
    
except paramiko.AuthenticationException:
    print("[X] Authentication failed - wrong password?")
except socket.timeout:
    print("[X] Connection timed out - server might not be reachable")
except socket.gaierror as e:
    print(f"[X] DNS/connection error: {e}")
except Exception as e:
    print(f"[X] Error: {e}")