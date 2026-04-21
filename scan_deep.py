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

def run_cmd(client, cmd, timeout=15):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='replace').strip()
        return out
    except:
        return '[TIMEOUT]'

client = connect()

# Check api.zibll.com (fake API server!)
print('='*70)
print('[!] 检查 /www/wwwroot/api.zibll.com (假API站点)')
print('='*70)
out = run_cmd(client, 'ls -la /www/wwwroot/api.zibll.com/ 2>/dev/null')
print(out)
out = run_cmd(client, 'cat /www/wwwroot/api.zibll.com/index.php 2>/dev/null')
print(f'\n内容:\n{out}')
out = run_cmd(client, 'ls -la /www/server/panel/vhost/nginx/ 2>/dev/null | grep zibll')
print(f'\nNginx配置:\n{out}')

# Check zibll-bypass mu-plugin
print('\n' + '='*70)
print('[!] 检查 zibll-bypass.php (mu-plugin)')
print('='*70)
out = run_cmd(client, 'cat /www/wwwroot/resource_site/wp-content/mu-plugins.disabled/zibll-bypass.php 2>/dev/null')
print(out)

# Check the BT panel cron job
print('\n' + '='*70)
print('[!] 检查宝塔定时任务')
print('='*70)
out = run_cmd(client, 'cat /www/server/cron/3ab48c27ec99cb9787749c362afae517 2>/dev/null')
print(out)

# Check Nginx vhost for zibll references
print('\n' + '='*70)
print('[!] 检查Nginx配置中zibll相关')
print('='*70)
out = run_cmd(client, 'grep -rl "zibll\\|api.zibll" /www/server/panel/vhost/ 2>/dev/null')
print(out if out else '无')

# Check if /etc/hosts still has zibll
out = run_cmd(client, 'cat /etc/hosts')
print(f'\n/etc/hosts:\n{out}')

# Check timthumb.php in puock (known vulnerable)
print('\n' + '='*70)
print('[!] 检查 puock/timthumb.php (已知漏洞组件)')
print('='*70)
out = run_cmd(client, 'grep -n "passthru\\|shell_exec\\|system\\|eval" /www/wwwroot/resource_site/wp-content/themes/puock/timthumb.php 2>/dev/null')
print(out)

# Check if there's a separate zibll options table
print('\n' + '='*70)
print('[!] 检查数据库中的zibll相关表')
print('='*70)
out = run_cmd(client, "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SHOW TABLES LIKE '%zib%';\" 2>/dev/null")
print(out if out else '无zibll相关表')

out = run_cmd(client, "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SHOW TABLES;\" 2>/dev/null")
print(f'\n所有数据表:\n{out}')

client.close()
