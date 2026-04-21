import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')
s=paramiko.SSHClient(); s.set_missing_host_key_policy(paramiko.AutoAddPolicy()); s.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check mu-plugin status
for cmd in [
    "ls -la /www/wwwroot/resource_site/wp-content/mu-plugins/",
    "php -l /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php 2>&1",
    "head -3 /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php",
    "tail -3 /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php",
]:
    stdin,stdout,stderr=s.exec_command(cmd, timeout=10)
    print(stdout.read().decode('utf-8', errors='ignore'))

# Check WP_DEBUG_LOG for any mu-plugin errors
stdin,stdout,stderr=s.exec_command("tail -5 /www/wwwroot/resource_site/wp-content/debug.log 2>/dev/null", timeout=10)
log = stdout.read().decode('utf-8', errors='ignore')
for line in log.split('\n'):
    if 'fatal' in line.lower() or 'error' in line.lower():
        print("ERR: %s" % line[:200])

s.close()