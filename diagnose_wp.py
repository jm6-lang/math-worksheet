import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

def run(cmd, t=15):
    _, o, e = client.exec_command(cmd, timeout=t)
    return o.read().decode('utf-8', errors='replace').strip(), e.read().decode('utf-8', errors='replace').strip()

# 1. Check mu-plugin syntax
print("=== mu-plugin ===")
o, _ = run("cat /www/wwwroot/resource_site/wp-content/mu-plugins/api-token-auth.php")
print(o)

# 2. Check WP debug log
print("\n=== WP error log (last 30 lines) ===")
o, _ = run("tail -30 /www/wwwroot/resource_site/wp-content/debug.log 2>/dev/null || echo 'No debug log'")
print(o)

# 3. Check PHP error log
print("\n=== PHP error log (last 20) ===")
o, _ = run("tail -20 /www/server/php/80/var/log/php-fpm.log 2>/dev/null | grep -i error || echo 'No PHP errors'")
print(o)

# 4. Test a simple POST directly
print("\n=== Test simple POST ===")
o, _ = run('curl -s -X POST -H "Content-Type: application/json" -H "X-Api-Token: $(python3 -c \'import json;print(json.load(open(\"/www/wwwroot/resource_site/auto_collect/config.json\"))[\"wp_api_token\"])\' )" -d \'{"title":"Test Post","content":"test content","status":"draft"}\' "https://skillxm.cn/wp-json/wp/v2/posts" 2>&1')
print(o[:500])

# 5. Check existing posts
print("\n=== Existing posts (via MySQL) ===")
o, _ = run("mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT ID, post_title, post_status FROM wp_posts WHERE post_type='post' ORDER BY ID DESC LIMIT 10;\" 2>/dev/null")
print(o)

# 6. Check existing categories
print("\n=== Categories ===")
o, _ = run("mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT term_id, name FROM wp_terms WHERE term_id IN (SELECT term_id FROM wp_term_taxonomy WHERE taxonomy='category');\" 2>/dev/null")
print(o)

# 7. Test creating category via API
print("\n=== Test category creation ===")
o, _ = run('curl -s -X POST -H "Content-Type: application/json" -H "X-Api-Token: $(python3 -c \'import json;print(json.load(open(\"/www/wwwroot/resource_site/auto_collect/config.json\"))[\"wp_api_token\"])\' )" -d \'{"name":"test-cat-123"}\' "https://skillxm.cn/wp-json/wp/v2/categories" 2>&1')
print(o[:500])

client.close()
