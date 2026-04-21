import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

def run(cmd, t=15):
    _, o, _ = client.exec_command(cmd, timeout=t)
    try: return o.read().decode('utf-8', errors='replace').strip()
    except: return '[TIMEOUT]'

# Clean SQL files
print(run('rm -f /tmp/add_caps3.sql /tmp/create_admin.sql /tmp/create_zibpay_tables.sql'))
print(run('rm -f /tmp/enable_reg.sql /tmp/site_beautify.sql /tmp/site_settings.sql /tmp/switch_theme.sql'))

# Clean HTML test files
print(run('rm -f /tmp/admin_page.html /tmp/curl_test.html /tmp/login_result.html'))
print(run('rm -f /tmp/test_admin.html /tmp/test_admin2.html /tmp/test_admin3.html'))
print(run('rm -f /tmp/test_final2.html /tmp/test_home3.html /tmp/test_login.html'))
print(run('rm -f /tmp/test_mu_admin.html /tmp/test_mu_home.html /tmp/test_sed_admin.html'))

# Clean cookies/log files
print(run('rm -f /tmp/cookies.txt /tmp/wp_cookie.txt /tmp/strace_out.txt'))
print(run('rm -f /tmp/install_yara.log /tmp/auto_apply_ip_ssl.log /tmp/panelExec.log'))
print(run('rm -f /tmp/schedule.log /tmp/task_log.log'))

# Clean misc
print(run('rm -rf /tmp/test_cookies /tmp/add_caps3.sql'))
print(run('rm -f /tmp/last_files_set_mode.pl /tmp/stdbool.hbtc_rdh3.c'))

# Save iptables rule (so it survives reboot)
print('\n--- Persist iptables ---')
out = run('which iptables-save')
if out and 'iptables-save' in out:
    print(run('iptables-save > /etc/iptables.rules 2>/dev/null'))
    # Add restore on boot
    print(run('grep -q "iptables-restore" /etc/rc.local 2>/dev/null || echo "iptables-restore < /etc/iptables.rules" >> /etc/rc.local 2>/dev/null'))
    print('iptables rules persisted')
else:
    print('iptables-save not found, skip persist')

# Final count
out = run('ls /tmp/ 2>/dev/null | grep -v "aap_locks\\|snap-private-tmp\\|systemd-private\\|btpanel\\|panel_daily\\|site_total"')
print(f'\nRemaining non-system files: {out if out else "NONE"}')

client.close()
