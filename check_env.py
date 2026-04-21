import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

def run(cmd, t=15):
    _, o, e = client.exec_command(cmd, timeout=t)
    out = o.read().decode('utf-8', errors='replace').strip()
    err = e.read().decode('utf-8', errors='replace').strip()
    return out + ('\n' + err if err else '')

print('=== Python ===')
print(run('python3 --version 2>/dev/null || python --version 2>/dev/null || echo "NO PYTHON"'))
print(run('pip3 --version 2>/dev/null || pip --version 2>/dev/null || echo "NO PIP"'))
print(run('pip3 list 2>/dev/null | grep -iE "requests|beautifulsoup|trafilatura|feedparser|lxml|pillow|newspaper" || echo "None installed"'))

print('\n=== WP-CLI ===')
print(run('wp --version 2>/dev/null || echo "NO WP-CLI"'))

print('\n=== WP Version ===')
print(run('cd /www/wwwroot/resource_site && grep "wp_version" wp-includes/version.php 2>/dev/null'))

print('\n=== WP REST API ===')
print(run('curl -s -o /dev/null -w "%{http_code}" https://skillxm.cn/wp-json/wp/v2/posts 2>/dev/null'))
print(run('curl -s https://skillxm.cn/wp-json/wp/v2/posts?per_page=1 2>/dev/null | head -c 200'))

print('\n=== WP Users ===')
print(run("mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT user_login, ID FROM wp_users;\" 2>/dev/null"))

print('\n=== Disk ===')
print(run('df -h / | tail -1'))

print('\n=== Cron ===')
print(run('crontab -l 2>/dev/null'))

client.close()
