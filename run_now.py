import paramiko
import socket

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)
    print("SSH connected!")

    # Quick test
    stdin, stdout, stderr = ssh.exec_command("echo ok && python3 --version", timeout=5)
    print(stdout.read().decode())

    # Run collector with timeout
    stdin, stdout, stderr = ssh.exec_command(
        "cd /www/wwwroot/resource_site/auto_collect && timeout 30 python3 collector.py 2>&1",
        timeout=40
    )
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    print("OUT:", out[-3000:] if len(out) > 3000 else out)
    if err.strip():
        print("ERR:", err[-1000:])
    
    ssh.close()
except Exception as e:
    print(f"Error: {e}")
