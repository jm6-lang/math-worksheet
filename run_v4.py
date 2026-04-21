import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

def run(cmd, t=200):
    _, o, e = client.exec_command(cmd, timeout=t)
    return o.read().decode('utf-8', errors='replace').strip(), e.read().decode('utf-8', errors='replace').strip()

# Clear and run
run("rm -f /www/wwwroot/resource_site/auto_collect/collector.lock /www/wwwroot/resource_site/auto_collect/published.db")
run("rm -f /www/wwwroot/resource_site/wp-content/debug.log")

print("=== Running collector v4 (RSS + Search) ===")
o, e = run('cd /www/wwwroot/resource_site/auto_collect && timeout 200 python3 collector.py 2>&1', 220)
if o:
    lines = o.split('\n')
    print('\n'.join(lines[-80:]))
if e:
    print('STDERR:', e[-500:])

# Check new posts
o, _ = run("mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT ID, LEFT(post_title,55) FROM wp_posts WHERE post_type='post' AND post_status='publish' ORDER BY ID DESC LIMIT 15;\" 2>/dev/null")
print("\n=== Latest posts ===")
print(o)

client.close()
