import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

def run(cmd, t=15):
    _, o, _ = client.exec_command(cmd, timeout=t)
    try: return o.read().decode('utf-8', errors='replace').strip()
    except: return '[TIMEOUT]'

# Clean all remaining scripts and temp dirs we created
print(run('rm -f /tmp/clear_cache.php /tmp/clear_opcache.php /tmp/fix_files.php'))
print(run('rm -f /tmp/fix_functions.py /tmp/fix_inc.py /tmp/install_yara.sh'))
print(run('rm -f /tmp/patch.py /tmp/patch_inc.py /tmp/puock.zip'))
print(run('rm -f /tmp/setup_footer.php /tmp/test_code.php /tmp/test_trace.php'))
print(run('rm -f /tmp/test_wp.php /tmp/test_wp_only.php'))
print(run('rm -rf /tmp/theme_extract'))
print(run('rm -rf /tmp/tmp.CWwMfnxiWN /tmp/tmp_qrhjfc5 /tmp/tmpgi22ciik /tmp/tmprbtq_fz8 /tmp/tmpxpbi3z8p'))

# Final verify
print('\n--- Final check ---')
out = run('find /tmp -maxdepth 1 \\( -name "*.php" -o -name "*.sh" -o -name "*.py" -o -name "*.zip" -o -name "*.tar.gz" \\) -type f 2>/dev/null')
print(f'Scripts: {out if out else "NONE"}')

out = run('ls /tmp/ 2>/dev/null')
print(f'/tmp contents:\n{out}')

client.close()
