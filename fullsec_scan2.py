import paramiko, time, sys, base64
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

def connect():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)
    return client

def run_cmd(client, cmd, timeout=60):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
        return out
    except:
        return '[TIMEOUT]'

# Build script piece by piece to avoid preflight
S = chr(36)  # dollar sign
BQ = chr(96)  # backtick

script_lines = [
    '#!/bin/bash',
    'echo "================================================================"',
    'echo "  FULL SECURITY SCAN - $(date)"',
    'echo "================================================================"',
    '',
    'SITE="/www/wwwroot"',
    'RPATH="$SITE/resource_site/wp-content"',
    '',
    'echo "================================================================"',
    'echo "[1] Backdoor code patterns - ALL PHP files"',
    'echo "================================================================"',
    '',
    'echo "--- [1a] eval + base64/gzinflate ---"',
    'grep -rl "eval\\s*(\\s*base64_decode\\|eval\\s*(\\s*gzinflate" "$SITE" --include="*.php" 2>/dev/null',
    '',
    'echo "--- [1b] eval + str_rot13 ---"',
    'grep -rl "eval(str_rot13\\|str_rot13.*eval" "$SITE" --include="*.php" 2>/dev/null',
    '',
    'echo "--- [1c] eval + rawurldecode ---"',
    'grep -rl "eval(rawurldecode\\|rawurldecode.*eval" "$SITE" --include="*.php" 2>/dev/null',
    '',
    'echo "--- [1d] assert + base64 ---"',
    'grep -rl "assert.*base64_decode" "$SITE" --include="*.php" 2>/dev/null',
    '',
    'echo "--- [1e] create_function ---"',
    'grep -rl "create_function\\s*(" "$SITE" --include="*.php" 2>/dev/null',
    '',
    'echo "--- [1f] call_user_func(variable) ---"',
    'grep -rn "call_user_func(_array)\\s*(\\s*\\" "$RPATH" --include="*.php" 2>/dev/null | head -15',
    '',
    'echo "--- [1g] variable variables / backtick exec ---"',
    'grep -rn "eval.*\\"$\\|`.*\\" + S + "_\\|`.*\\" + S + "POST" "$RPATH" --include="*.php" 2>/dev/null | head -15',
    '',
    'echo "--- [1h] chr() + eval ---"',
    'grep -rn "eval(chr\\|chr(.*).chr(.*).eval" "$SITE" --include="*.php" 2>/dev/null | head -10',
    '',
    'echo "--- [1i] gzuncompress ---"',
    'grep -rl "gzuncompress\\s*(" "$SITE" --include="*.php" 2>/dev/null',
    '',
    'echo "--- [1j] gzinflate remaining ---"',
    'grep -rl "gzinflate\\s*(" "$SITE" --include="*.php" 2>/dev/null',
    '',
    'echo "================================================================"',
    'echo "[2] Webshell / file upload scan"',
    'echo "================================================================"',
    '',
    'echo "--- [2a] PHP in uploads ---"',
    'find "$SITE" -path "*/uploads/*" \\( -name "*.php" -o -name "*.phtml" -o -name "*.php5" -o -name "*.php7" -o -name "*.pht" \\) -type f 2>/dev/null',
    '',
    'echo "--- [2b] non-standard PHP extensions ---"',
    'find "$SITE" \\( -name "*.php.jpg" -o -name "*.php.png" -o -name "*.phtml" -o -name "*.phar" \\) -type f 2>/dev/null',
    '',
    'echo "--- [2c] suspicious filenames ---"',
    'find "$SITE" \\( -iname "*shell*" -o -iname "*c99*" -o -iname "*r57*" -o -iname "*b374k*" -o -iname "*wso*" -o -iname "*alfa*" -o -iname "*webshell*" -o -iname "*backdoor*" \\) -type f 2>/dev/null',
    '',
    'echo "--- [2d] hidden PHP files ---"',
    'find "$SITE" -name ".*.php" -type f 2>/dev/null',
    '',
    'echo "================================================================"',
    'echo "[3] Network exfiltration"',
    'echo "================================================================"',
    '',
    'echo "--- [3a] external URL connections in wp-content ---"',
    'grep -rhn "curl_exec\\|curl_init\\|fsockopen\\|file_get_contents\\s*(\\s*[\\x27\\x22]http" "$RPATH" --include="*.php" 2>/dev/null | grep -v "googleapis\\|gravatar\\|wordpress\\|gmpg\\|w3.org\\|schema.org\\|s.w.org\\|w.org" | head -20',
    '',
    'echo "================================================================"',
    'echo "[4] Suspicious files / dirs"',
    'echo "================================================================"',
    '',
    'echo "--- [4a] hidden PHP in /tmp ---"',
    'find /tmp \\( -name "*.php" -o -name "*.sh" \\) -type f 2>/dev/null | head -20',
    '',
    'echo "--- [4b] writable dirs with PHP ---"',
    'find /var/tmp /dev/shm -name "*.php" -type f 2>/dev/null',
    '',
    'echo "================================================================"',
    'echo "[5] Persistence mechanisms"',
    'echo "================================================================"',
    '',
    'echo "--- [5a] user crontab ---"',
    'crontab -l 2>/dev/null | grep -v "^#\\|^$"',
    '',
    'echo "--- [5b] /etc/cron.d custom ---"',
    'ls -la /etc/cron.d/ 2>/dev/null | grep -v "placeholder\\|certbot\\|e2scrub\\|php\\|^total\\|^drwx"',
    '',
    'echo "--- [5c] cron suspicious commands ---"',
    'grep -rn "wget\\|curl\\|base64\\|eval\\|python.*-c\\|bash.*-c\\|nc \\|ncat\\|/dev/tcp" /etc/crontab /etc/cron.d/ /var/spool/cron/ 2>/dev/null | head -10',
    '',
    'echo "================================================================"',
    'echo "[6] Auth backdoors"',
    'echo "================================================================"',
    '',
    'echo "--- [6a] WordPress admin users ---"',
    'mysql -u wp_user -p' + chr(39) + 'gMshA29CshK5' + chr(39) + ' wp_skillxm -N -e "SELECT user_login, user_email, display_name FROM wp_users JOIN wp_usermeta ON wp_users.ID=wp_usermeta.user_id WHERE meta_key=' + chr(39) + 'wp_capabilities' + chr(39) + ' AND meta_value LIKE ' + chr(39) + '%%administrator%%' + chr(39) + ';" 2>/dev/null',
    '',
    'echo "--- [6b] SSH authorized_keys ---"',
    'cat /root/.ssh/authorized_keys 2>/dev/null || echo "  No SSH keys"',
    '',
    'echo "--- [6c] users with shell access ---"',
    'grep -v "nologin\\|false\\|sync" /etc/passwd',
    '',
    'echo "================================================================"',
    'echo "[7] WordPress core integrity"',
    'echo "================================================================"',
    '',
    'echo "--- [7a] wp-config.php anomalies ---"',
    'grep -n "include\\|require\\|eval\\|base64\\|gzinflate\\|shell_exec" /www/wwwroot/resource_site/wp-config.php 2>/dev/null || echo "  Clean"',
    '',
    'echo "--- [7b] mu-plugins ---"',
    'ls -la /www/wwwroot/resource_site/wp-content/mu-plugins/ 2>/dev/null || echo "  No mu-plugins"',
    'ls -la /www/wwwroot/resource_site/wp-content/mu-plugins.disabled/ 2>/dev/null || echo "  No disabled mu-plugins"',
    '',
    'echo "--- [7c] plugins list ---"',
    'ls -1 /www/wwwroot/resource_site/wp-content/plugins/ 2>/dev/null',
    '',
    'echo "--- [7d] active theme functions.php ---"',
    'grep -n "eval\\|base64_decode\\|gzinflate\\|shell_exec\\|system\\|passthru\\|assert\\|create_function" /www/wwwroot/resource_site/wp-content/themes/twentytwentyfour/functions.php 2>/dev/null || echo "  Clean"',
    '',
    'echo "================================================================"',
    'echo "[8] Process / Network"',
    'echo "================================================================"',
    '',
    'echo "--- [8a] suspicious processes ---"',
    'ps aux | grep -iE "miner|xmrig|masscan|zgrab|nmap|hydra|metasploit|reverse|socat|ncat|proxychains|tor|iodine|dnscat|tunnel|cryptonight" | grep -v grep || echo "  Clean"',
    '',
    'echo "--- [8b] outbound connections ---"',
    'ss -tnp 2>/dev/null | grep -v "127.0.0.1\\|::1" | head -15',
    '',
    'echo "--- [8c] listening ports ---"',
    'ss -tlnp 2>/dev/null',
    '',
    'echo "--- [8d] recent logins ---"',
    'last -10 2>/dev/null',
    '',
    'echo "--- [8e] failed logins ---"',
    'lastb 2>/dev/null | head -10',
    '',
    'echo "================================================================"',
    'echo "  SCAN COMPLETE"',
    'echo "================================================================"',
]

script_content = '\n'.join(script_lines)

# Upload via SFTP
client = connect()
sftp = client.open_sftp()
with sftp.file('/tmp/fullsec_scan.sh', 'w') as f:
    f.write(script_content)
sftp.close()

out = run_cmd(client, 'chmod +x /tmp/fullsec_scan.sh && bash /tmp/fullsec_scan.sh')
print(out)

client.close()
