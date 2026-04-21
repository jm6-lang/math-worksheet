import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    "nginx -t 2>&1",
    "systemctl reload nginx 2>&1",
    "systemctl status nginx 2>&1 | head -5",
]

for c in cmds:
    print("CMD: " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    if out: print(out, flush=True)
    if err: print("ERR: " + err, flush=True)

import time
time.sleep(2)

# Test
stdin, stdout, stderr = ssh.exec_command("curl -s 'https://skillxm.cn/?t=1' 2>/dev/null | wc -c")
print("Page size: " + stdout.read().decode().strip())

stdin, stdout, stderr = ssh.exec_command("curl -s 'https://skillxm.cn/?t=1' 2>/dev/null | tail -c 500")
print("Footer area:\n" + stdout.read().decode('utf-8', errors='replace'))

stdin, stdout, stderr = ssh.exec_command("cat /tmp/mutest.txt 2>/dev/null || echo 'no-mutest'")
print("MU test: " + stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()
