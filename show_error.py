import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

sftp = ssh.open_sftp()

# Enable debug display
with sftp.open('/www/wwwroot/resource_site/wp-config.php', 'r') as f:
    config = f.read().decode('utf-8')

# Add debug display
if "WP_DEBUG_DISPLAY" not in config:
    config = config.replace("define( 'WP_DEBUG', false );", "define( 'WP_DEBUG', true );\ndefine( 'WP_DEBUG_DISPLAY', true );")
    if "WP_DEBUG" not in config:
        config = config.replace("<?php", "<?php\ndefine( 'WP_DEBUG', true );\ndefine( 'WP_DEBUG_DISPLAY', true );")

with sftp.open('/www/wwwroot/resource_site/wp-config.php', 'w') as f:
    f.write(config)
sftp.close()
print("Debug enabled")

import time
time.sleep(2)
stdin, stdout, stderr = ssh.exec_command("curl -s https://www.skillxm.cn/ 2>/dev/null | head -80", timeout=15)
print("\nOutput:\n%s" % stdout.read().decode('utf-8', errors='ignore')[:3000])

ssh.close()
