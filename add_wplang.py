import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Read current wp-config
stdin, out, err = c.exec_command('cat /www/wwwroot/skillxm.cn/public/wp-config.php')
config = out.read().decode()

# Add WPLANG
if 'WPLANG' not in config:
    config = config.replace(
        "define( 'WP_DEBUG', false );",
        "define( 'WP_DEBUG', false );\ndefine( 'WPLANG', 'zh_CN' );"
    )
    
    stdin, out, err = c.exec_command('cat > /www/wwwroot/skillxm.cn/public/wp-config.php << \'EOF\'\n' + config + '\nEOF')
    print('Updated:', err.read().decode().strip() if err.read() else 'OK')

# Verify
stdin, out, err = c.exec_command('grep WPLANG /www/wwwroot/skillxm.cn/public/wp-config.php')
print('Result:', out.read().decode().strip())

c.close()