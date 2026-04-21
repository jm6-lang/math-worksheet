import paramiko, time, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

def connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)
    return client

def run_cmd(client, cmd, timeout=15):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
        return out
    except:
        return '[TIMEOUT]'

client = connect()

# Direct MySQL commands
bash_script = """#!/bin/bash
echo "=== Current theme in DB ==="
mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "SELECT option_name, option_value FROM wp_options WHERE option_name IN ('template','stylesheet','current_theme');" 2>/dev/null

echo ""
echo "=== Switching to twentytwentyfour ==="
mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e "UPDATE wp_options SET option_value='twentytwentyfour' WHERE option_name IN ('template','stylesheet');" 2>/dev/null
mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e "UPDATE wp_options SET option_value='Twenty Twenty-Four' WHERE option_name='current_theme';" 2>/dev/null
echo "Done."

echo ""
echo "=== Verify ==="
mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "SELECT option_name, option_value FROM wp_options WHERE option_name IN ('template','stylesheet','current_theme');" 2>/dev/null

echo ""
echo "=== Restart PHP-FPM ==="
systemctl restart php8.1-fpm
sleep 2

echo "=== Site test ==="
curl -s -k --max-time 15 -D- -o /dev/null https://127.0.0.1/ 2>&1 | head -10
curl -s -k --max-time 15 https://127.0.0.1/ 2>/dev/null | grep -o "<title>[^<]*</title>" | head -1
echo ""
echo "Page size:"
curl -s -k --max-time 15 https://127.0.0.1/ 2>/dev/null | wc -c

echo ""
echo "=== DONE ==="
"""

sftp = client.open_sftp()
with sftp.file('/tmp/fix_theme.sh', 'w') as f:
    f.write(bash_script)
sftp.close()

out = run_cmd(client, 'bash /tmp/fix_theme.sh', timeout=30)
print(out)

client.close()
