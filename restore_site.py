import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Restore WP_CACHE and reactivate wp-super-cache
cmds = [
    # Restore WP_CACHE
    "sed -i \"s/define('WP_CACHE', false)/define('WP_CACHE', true)/\" /www/wwwroot/resource_site/wp-config.php",
    
    # Reactivate wp-super-cache
    "wp plugin activate wp-super-cache --allow-root --path=/www/wwwroot/resource_site/ 2>&1 | tail -2",
    
    # Also fix WP_DEBUG_DISPLAY to false to hide notices
    "sed -i \"s/define('WP_DEBUG_DISPLAY', true)/define('WP_DEBUG_DISPLAY', false)/\" /www/wwwroot/resource_site/wp-config.php",
    
    # Verify wp-config
    "grep 'WP_CACHE\\|WP_DEBUG' /www/wwwroot/resource_site/wp-config.php",
]

for c in cmds:
    print("CMD: " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out: print(out, flush=True)

import time
time.sleep(2)

# Test
stdin, stdout, stderr = ssh.exec_command("curl -sk 'https://skillxm.cn/?v=16' 2>/dev/null | wc -c")
print("Page size: " + stdout.read().decode().strip())

ssh.close()
print("Restored!")
