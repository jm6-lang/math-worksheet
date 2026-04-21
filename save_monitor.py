#!/usr/bin/env python3
import paramiko

HOST = "240b:4001:278:8402:0:bd18:bd09:af0d"
USERNAME = "root"
PASSWORD = "l95UE5ysF)7.gR"
THEME = "/www/wwwroot/resource_site/wp-content/themes/zibll"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

sftp = client.open_sftp()

# Save monitor script on server
monitor_py = '''#!/usr/bin/env python3
import paramiko
import sys

HOST = "240b:4001:278:8402:0:bd18:bd09:af0d"
USERNAME = "root"
PASSWORD = "l95UE5ysF)7.gR"
THEME = "/www/wwwroot/resource_site/wp-content/themes/zibll"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

# Check for backdoor patterns
stdin, stdout, stderr = client.exec_command(f"grep -rl 'eval.*gzinflate\\|gzinflate.*eval' {THEME}/ 2>/dev/null")
bad_files = stdout.read().decode("utf-8", errors="ignore").strip()

if bad_files:
    print(f"DANGER: {bad_files}")
    for f in bad_files.split("\\n"):
        print(f"Deleting: {f}")
        stdin, stdout, stderr = client.exec_command(f"rm -f {f}")
    sys.exit(1)
else:
    print("OK - Theme is safe")
    sys.exit(0)

client.close()
'''

f = sftp.file('/tmp/zibll_safe_check.py', 'w')
f.write(monitor_py)
f.close()

stdin, stdout, stderr = client.exec_command('chmod +x /tmp/zibll_safe_check.py')
print('Python monitor created at /tmp/zibll_safe_check.py')

# Test it
stdin, stdout, stderr = client.exec_command('python3 /tmp/zibll_safe_check.py')
print('Test result:', stdout.read().decode('utf-8', errors='ignore').strip())

client.close()
print('[DONE] Monitor script ready!')