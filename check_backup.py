import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 宝塔面板备份
cmds = [
    "ls -lht /www/backup/database/ 2>/dev/null | head -10",
    "ls -lht /www/backup/site/ 2>/dev/null | head -10",
    "find /www/backup -name '*.sql.gz' -o -name '*.sql' 2>/dev/null | head -10",
    "find /www/backup -name '*.zip' -o -name '*.tar.gz' 2>/dev/null | head -10",
    "bt default 2>/dev/null | head -3",
    "ls /www/server/panel/backup/ 2>/dev/null | head -10",
]
for cmd in cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    result = stdout.read().decode('utf-8', errors='ignore').strip()
    if result:
        print(result)

ssh.close()
