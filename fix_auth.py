import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

# Kill any stuck collector processes
stdin, stdout, stderr = ssh.exec_command(
    "pkill -f 'collector.py' 2>/dev/null; rm -f /www/wwwroot/resource_site/auto_collect/collector.lock; echo killed",
    timeout=10
)
print(stdout.read().decode('utf-8', errors='replace'))

# Verify new token is set
stdin, stdout, stderr = ssh.exec_command(
    "grep wp_api_token /www/wwwroot/resource_site/auto_collect/config.json",
    timeout=10
)
print("Token:", stdout.read().decode('utf-8', errors='replace').strip())

# Quick auth test with new token
new_token = "s6eW 2kHy 8yqu XNuY JjoK HHOR"
stdin, stdout, stderr = ssh.exec_command(
    f"curl -s -o /dev/null -w '%{{http_code}}' -u admin:'{new_token}' https://skillxm.cn/wp-json/wp/v2/users/me",
    timeout=15
)
code = stdout.read().decode('utf-8', errors='replace').strip()
print("Auth test HTTP:", code)

ssh.close()
