import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    'ls -la /www/wwwroot/resource_site/wp-content/mu-plugins/',
    'rm -rf /www/wwwroot/resource_site/wp-content/mu-plugins/',
    'ls /www/wwwroot/resource_site/wp-content/mu-plugins/ 2>&1',
    'grep -c "sitemap" /www/wwwroot/resource_site/wp-content/themes/yymarket/footer.php 2>/dev/null || echo "0"',
]

for c in cmds:
    stdin, stdout, stderr = ssh.exec_command(c, timeout=10)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    print(f">>> {c}")
    print(out or err or '(empty)')
    print()

ssh.close()
print("Done")
