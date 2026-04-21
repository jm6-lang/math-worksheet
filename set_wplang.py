import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Add WPLANG to wp-config.php
print("=== Add WPLANG to wp-config ===")
stdin, out, err = c.exec_command('sed -i "s/define( .WP_DEBUG., false );/define( \\'WP_DEBUG\\', false );\\ndefine( \\'WPLANG\\', \\'zh_CN\\' );/" /www/wwwroot/skillxm.cn/public/wp-config.php')
print(out.read().decode())

# Verify
stdin, out, err = c.exec_command('grep -E "WPLANG|WP_DEBUG" /www/wwwroot/skillxm.cn/public/wp-config.php')
print('Result:', out.read().decode())

c.close()