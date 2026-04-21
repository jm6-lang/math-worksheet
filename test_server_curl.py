import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Try downloading an image directly via curl
cmds = [
    'curl -s -o /tmp/test_img.jpg https://httpbin.org/image/jpeg && ls -la /tmp/test_img.jpg',
    'curl -s -o /tmp/test_picsum.jpg https://picsum.photos/200/300 && ls -la /tmp/test_picsum.jpg',
    'curl -s -o /tmp/test_placeholder.png https://placehold.co/800x600.png && ls -la /tmp/test_placeholder.png',
]

for cmd in cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    print(f"Cmd: {cmd.split()[-1]}")
    print(f"  Output: {out[:200]}")
    if err.strip():
        print(f"  Error: {err[:200]}")

ssh.close()