import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

cmds = [
    'curl -s -o /dev/null -w "%{http_code}" --max-time 5 https://picsum.photos/200/300',
    'curl -s -o /dev/null -w "%{http_code}" --max-time 5 https://httpbin.org/image/jpeg',
    'curl -s -o /dev/null -w "%{http_code}" --max-time 5 https://placehold.co/800x600.png',
    'curl -s -o /dev/null -w "%{http_code}" --max-time 5 https://via.placeholder.com/800x600.jpg',
    'curl -s -o /dev/null -w "%{http_code}" --max-time 5 https://www.w3schools.com/css/img_5terre.jpg',
]

for cmd in cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=20)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    print(f'{cmd.split()[-1]}: {out}')

ssh.close()