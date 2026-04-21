import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
s=paramiko.SSHClient(); s.set_missing_host_key_policy(paramiko.AutoAddPolicy()); s.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)
stdin,stdout,stderr=s.exec_command('cd /www/wwwroot/resource_site && wp cache flush --allow-root 2>&1',timeout=15); print(stdout.read().decode().strip())
s.exec_command('rm -rf /www/wwwroot/resource_site/wp-content/cache/wp-super-cache/* 2>/dev/null',timeout=5)
s.close()
print("Cache flushed")