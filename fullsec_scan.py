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

def run_cmd(client, cmd, timeout=30):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
        return out
    except:
        return '[TIMEOUT]'

client = connect()

# Write comprehensive scan script via SFTP
script = r"""#!/bin/bash
echo "================================================================"
echo "  FULL SECURITY SCAN - $(date)"
echo "================================================================"

# ============================================================
# SECTION 1: Backdoor patterns in ALL PHP files on the server
# ============================================================
echo ""
echo "================================================================"
echo "[1] 后门代码模式扫描 - 全盘PHP文件"
echo "================================================================"

SITE="/www/wwwroot"

echo ""
echo "--- [1a] eval + base64/gzinflate (多层混淆后门) ---"
grep -rl "eval\s*(\s*base64_decode\|eval\s*(\s*gzinflate" "$SITE" --include="*.php" 2>/dev/null

echo ""
echo "--- [1b] eval + str_rot13 ---"
grep -rl "eval(str_rot13\|str_rot13.*eval" "$SITE" --include="*.php" 2>/dev/null

echo ""
echo "--- [1c] eval + gzuncompress ---"
grep -rl "eval(gzuncompress\|gzuncompress.*eval" "$SITE" --include="*.php" 2>/dev/null

echo ""
echo "--- [1d] eval + rawurldecode (常见webshell) ---"
grep -rl "eval(rawurldecode\|rawurldecode.*eval" "$SITE" --include="*.php" 2>/dev/null

echo ""
echo "--- [1e] assert + base64_decode ---"
grep -rl "assert.*base64_decode\|base64_decode.*assert" "$SITE" --include="*.php" 2>/dev/null

echo ""
echo "--- [1f] preg_replace /e modifier (RCE) ---"
grep -rl "preg_replace.*\/[a-z]*e[a-z]*['\"]" "$SITE" --include="*.php" 2>/dev/null

echo ""
echo "--- [1g] create_function (代码注入) ---"
grep -rl "create_function\s*(" "$SITE" --include="*.php" 2>/dev/null

echo ""
echo "--- [1h] call_user_func with variable (动态调用) ---"
grep -rn "call_user_func\s*(\s*\$\|call_user_func_array\s*(\s*\$" "$SITE" --include="*.php" 2>/dev/null | head -20

echo ""
echo "--- [1i] $$variable / variable variables (动态代码) ---"
grep -rn '\$\$\|`\${' "$SITE" --include="*.php" 2>/dev/null | head -20

echo ""
echo "--- [1j] backtick execution ---"
grep -rn '`.*\$_\|`.*\$_GET\|`.*\$_POST\|`.*\$_REQUEST' "$SITE" --include="*.php" 2>/dev/null | head -20

echo ""
echo "--- [1k] base64_decode + gzinflate + str_rot13 (三重混淆) ---"
grep -rl "base64_decode.*gzinflate.*str_rot13\|str_rot13.*gzinflate.*base64_decode" "$SITE" --include="*.php" 2>/dev/null

echo ""
echo "--- [1l] chr() + eval chains (无明文后门) ---"
grep -rn "eval(chr\|chr(.*).chr(.*).eval\|eval\s*(\s*chr" "$SITE" --include="*.php" 2>/dev/null | head -20

echo ""
echo "--- [1m] file_get_contents with eval ---"
grep -rn "eval(file_get_contents\|eval\s*(\s*file" "$SITE" --include="*.php" 2>/dev/null | head -10

echo ""
echo "--- [1n] socket_create / fsockopen with variable host ---"
grep -rn "fsockopen\s*(\s*\$\|socket_create" "$SITE" --include="*.php" 2>/dev/null | head -10

# ============================================================
# SECTION 2: Shell upload / webshell patterns
# ============================================================
echo ""
echo "================================================================"
echo "[2] Webshell / 文件上传漏洞扫描"
echo "================================================================"

echo ""
echo "--- [2a] uploads目录中的可执行文件 ---"
find "$SITE" -path "*/uploads/*" \( -name "*.php" -o -name "*.phtml" -o -name "*.php5" -o -name "*.php7" -o -name "*.phps" -o -name "*.pht" \) -type f 2>/dev/null

echo ""
echo "--- [2b] 非标准PHP扩展名文件 ---"
find "$SITE" \( -name "*.php.jpg" -o -name "*.php.png" -o -name "*.php.gif" -o -name "*.php.jpeg" -o -name "*.phtml" -o -name "*.php5" -o -name "*.php7" -o -name "*.pht" -o -name "*.phar" \) -type f 2>/dev/null

echo ""
echo "--- [2c] 最近7天内上传的PHP文件 ---"
find "$SITE" -name "*.php" -mtime -7 -newer "$SITE/resource_site/wp-settings.php" -type f 2>/dev/null

echo ""
echo "--- [2d] .htaccess 异常 (允许PHP执行在uploads) ---"
find "$SITE" -path "*/uploads/*" -name ".htaccess" -exec grep -l "php\|cgi" {} \; 2>/dev/null

# ============================================================
# SECTION 3: Network exfiltration / C2 communication
# ============================================================
echo ""
echo "================================================================"
echo "[3] 可疑网络外连 / C2通信"
echo "================================================================"

echo ""
echo "--- [3a] 使用curl/wget/fsockopen连接外部域名 ---"
grep -rhn "curl_exec\|curl_init\|fsockopen\|file_get_contents\s*(\s*['\"]http" "$SITE/resource_site/wp-content" --include="*.php" 2>/dev/null | grep -v "googleapis\|gravatar\|wordpress\|gmpg\|w3.org\|schema.org\|s.w.org" | head -30

echo ""
echo "--- [3b] base64编码的URL (隐藏C2) ---"
grep -rhn "base64_decode.*http\|base64_encode.*http" "$SITE" --include="*.php" 2>/dev/null | head -10

# ============================================================
# SECTION 4: Suspicious files and directories
# ============================================================
echo ""
echo "================================================================"
echo "[4] 可疑文件和目录"
echo "================================================================"

echo ""
echo "--- [4a] 隐藏PHP文件 ---"
find "$SITE" -name ".*.php" -type f 2>/dev/null

echo ""
echo "--- [4b] 可疑文件名 (常见webshell命名) ---"
find "$SITE" \( -iname "*shell*" -o -iname "*c99*" -o -iname "*r57*" -o -iname "*b374k*" -o -iname "*wso*" -o -iname "*alfa*" -o -iname "*minishell*" -o -iname "*webshell*" -o -iname "*backdoor*" -o -iname "*spy*" -o -iname "*rootkit*" -o -iname "*trojan*" \) -type f 2>/dev/null

echo ""
echo "--- [4c] 可疑目录名 ---"
find "$SITE" -type d \( -name ".*" -o -iname "*cache*temp*" -o -iname "*logs*" \) 2>/dev/null | grep -v "\.git\|\.well-known\|node_modules\|vendor" | head -20

echo ""
echo "--- [4d] /tmp目录中的可疑文件 ---"
find /tmp -name "*.php" -o -name "*.sh" -o -name "*.py" 2>/dev/null | head -20

# ============================================================
# SECTION 5: Persistence mechanisms
# ============================================================
echo ""
echo "================================================================"
echo "[5] 持久化机制检查"
echo "================================================================"

echo ""
echo "--- [5a] 用户crontab ---"
crontab -l 2>/dev/null | grep -v "^#\|^$"

echo ""
echo "--- [5b] /etc/cron.d/ 自定义任务 ---"
ls -la /etc/cron.d/ 2>/dev/null | grep -v "placeholder\|certbot\|e2scrub\|php"

echo ""
echo "--- [5c] 系统crontab中的可疑条目 ---"
grep -rn "wget\|curl\|base64\|eval\|python.*-c\|bash.*-c\|nc\s\|ncat\|/dev/tcp" /etc/crontab /etc/cron.d/ /var/spool/cron/ 2>/dev/null | head -20

echo ""
echo "--- [5d] autorun / init.d 可疑服务 ---"
ls /etc/init.d/ 2>/dev/null | grep -v -E "ssh|nginx|mysql|php|cron|syslog|rsyslog|networking|ufw|apparmor|snapd|unattended|multipathd|dbus|atd|irqbalance|open-vm|haveged|acpid|lvm|mdadm|udev|kmod|rsync|bluetooth|saned|cups|avahi|polkit|colord|accounts|udisks|fwupd|bolt|thermald|power| ModemManager|openvpn|postfix|dovecot|named|httpd|vsftpd|proftpd|pure-ftpd|memcached|redis|mongod|elasticsearch"

echo ""
echo "--- [5e] systemd可疑服务 ---"
systemctl list-units --type=service --state=running 2>/dev/null | grep -v -E "ssh|nginx|mysql|php|cron|systemd|dbus|snapd|ufw|apparmor|polkit|rsyslog|getty|network|udev|journal|logind|user@|multipathd|lvm2|mdadm|accounts|thermald|power|irqbalance|haveged|acpid|unattended|cloud|qemu|serial|fwupd|bolt|udisks|ModemManager|colord|avahi|bluetooth|cups|saned|openvpn|postfix|dovecot|named|httpd|vsftpd|proftpd|pure-ftpd|memcached|redis|mongod|elastic"

# ============================================================
# SECTION 6: Authentication backdoors
# ============================================================
echo ""
echo "================================================================"
echo "[6] 认证后门检查"
echo "================================================================"

echo ""
echo "--- [6a] WordPress用户列表 (检查可疑管理员) ---"
mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "SELECT user_login, user_email, display_name FROM wp_users JOIN wp_usermeta ON wp_users.ID = wp_usermeta.user_id WHERE meta_key='wp_capabilities' AND meta_value LIKE '%administrator%';" 2>/dev/null

echo ""
echo "--- [6b] SSH authorized_keys ---"
cat /root/.ssh/authorized_keys 2>/dev/null | head -20
echo "---"
for d in /home/*/; do
    echo "$d:"
    cat "${d}.ssh/authorized_keys" 2>/dev/null
done

echo ""
echo "--- [6c] /etc/passwd 中可登录用户 ---"
grep -v "nologin\|false\|sync" /etc/passwd

echo ""
echo "--- [6d] WordPress API密钥/令牌 ---"
mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "SELECT user_login, meta_key FROM wp_usermeta WHERE meta_key LIKE '%token%' OR meta_key LIKE '%api_key%' OR meta_key LIKE '%secret%';" 2>/dev/null | head -10

# ============================================================
# SECTION 7: File integrity - modified core files
# ============================================================
echo ""
echo "================================================================"
echo "[7] WordPress核心文件完整性"
echo "================================================================"

echo ""
echo "--- [7a] wp-config.php 异常include ---"
grep -n "include\|require\|eval\|base64\|gzinflate" /www/wwwroot/resource_site/wp-config.php 2>/dev/null

echo ""
echo "--- [7b] wp-settings.php 异常 ---"
wc -l /www/wwwroot/resource_site/wp-settings.php 2>/dev/null
tail -10 /www/wwwroot/resource_site/wp-settings.php 2>/dev/null

echo ""
echo "--- [7c] wp-load.php 异常 ---"
wc -l /www/wwwroot/resource_site/wp-load.php 2>/dev/null
tail -10 /www/wwwroot/resource_site/wp-load.php 2>/dev/null

echo ""
echo "--- [7d] functions.php (当前主题) 异常 ---"
grep -n "eval\|base64_decode\|gzinflate\|shell_exec\|system\s*(\|passthru\|assert\|create_function" /www/wwwroot/resource_site/wp-content/themes/twentytwentyfour/functions.php 2>/dev/null || echo "  Clean"

echo ""
echo "--- [7e] 检查wp-content/plugins目录中的可疑插件 ---"
ls -1 /www/wwwroot/resource_site/wp-content/plugins/ 2>/dev/null

echo ""
echo "--- [7f] 检查mu-plugins ---"
ls -la /www/wwwroot/resource_site/wp-content/mu-plugins/ 2>/dev/null || echo "  No mu-plugins"
ls -la /www/wwwroot/resource_site/wp-content/mu-plugins.disabled/ 2>/dev/null || echo "  No disabled mu-plugins"

# ============================================================
# SECTION 8: Process and network
# ============================================================
echo ""
echo "================================================================"
echo "[8] 进程和网络检查"
echo "================================================================"

echo ""
echo "--- [8a] 可疑进程 (挖矿/C2/扫描) ---"
ps aux | grep -iE "miner|xmrig|masscan|zgrab|nmap|hydra|metasploit|reverse|socat|ncat|proxychains|tor|iodine|dnscat|tunnel" | grep -v grep || echo "  Clean"

echo ""
echo "--- [8b] 异常出站连接 ---"
ss -tnp 2>/dev/null | grep -v "127.0.0.1\|::1" | head -20

echo ""
echo "--- [8c] 监听端口 (非标准) ---"
ss -tlnp 2>/dev/null

echo ""
echo "--- [8d] 最近登录记录 ---"
last -10 2>/dev/null

echo ""
echo "--- [8e] 失败登录尝试 ---"
lastb 2>/dev/null | head -10

echo ""
echo "================================================================"
echo "  SCAN COMPLETE"
echo "================================================================"
"""

sftp = client.open_sftp()
with sftp.file('/tmp/fullsec_scan.sh', 'w') as f:
    f.write(script)
sftp.close()

out = run_cmd(client, 'bash /tmp/fullsec_scan.sh', timeout=60)
print(out)

client.close()
