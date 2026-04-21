import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# curl with timeout and show full response
stdin, stdout, stderr = ssh.exec_command(
    "curl -s --max-time 30 -w '\\nHTTP_CODE:%{http_code}\\nSIZE:%{size_download}' https://www.skillxm.cn/ 2>/dev/null | tail -20",
    timeout=35
)
output = stdout.read().decode('utf-8', errors='ignore')
print("Response:\n%s" % output[:2000])

# Check if WP is actually crashing
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && timeout 30 php -d display_errors=1 index.php 2>&1 | head -50",
    timeout=35
)
output = stdout.read().decode('utf-8', errors='ignore')
err = stderr.read().decode('utf-8', errors='ignore')
print("\nPHP index.php:\n%s" % (output + err)[:2000] if (output + err) else "(no output)")

# Check error log (nginx error)
stdin, stdout, stderr = ssh.exec_command(
    "tail -5 /var/log/nginx/error.log 2>/dev/null",
    timeout=5
)
print("\nNginx error:\n%s" % stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
