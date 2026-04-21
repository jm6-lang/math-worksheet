import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

def run(cmd, t=15):
    _, o, _ = client.exec_command(cmd, timeout=t)
    try: return o.read().decode('utf-8', errors='replace').strip()
    except: return '[TIMEOUT]'

# Clean /tmp
print(run('rm -rf /tmp/themes_backup'))
print(run('rm -f /tmp/test_inc.php /tmp/setup_theme.php /tmp/test_theme.php /tmp/inc_php_backup.php /tmp/fix_footer.php'))
print(run('rm -f /tmp/fs.sh /tmp/fullsec_scan.sh /tmp/cleanup_final.sh'))
print(run('rm -f /tmp/del_zibll.sh /tmp/zibll_safe_check.py'))

# Block brute force IP
print('\n--- Blocking 43.106.13.111 ---')
print(run('iptables -A INPUT -s 43.106.13.111 -j DROP'))
print(run('iptables -L INPUT -n | grep 43.106.13.111'))

# Verify /tmp is clean
print('\n--- /tmp verify ---')
out = run('ls /tmp/*.php /tmp/*.sh /tmp/*.py /tmp/*.tar.gz /tmp/*.zip 2>/dev/null')
print(f'Remaining scripts: {out if out else "NONE"}')

out = run('ls -d /tmp/*/ 2>/dev/null')
print(f'Remaining dirs: {out if out else "NONE"}')

client.close()
