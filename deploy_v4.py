import paramiko, json, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

def run(cmd, t=30):
    _, o, e = client.exec_command(cmd, timeout=t)
    return o.read().decode('utf-8', errors='replace').strip(), e.read().decode('utf-8', errors='replace').strip()

sftp = client.open_sftp()

# 1. Update mu-plugin
with sftp.file('/www/wwwroot/resource_site/auto_collect/config.json', 'r') as f:
    cfg = json.loads(f.read())
token = cfg.get('wp_api_token', '')

muphp = "<?php\n"
muphp += "add_filter('rest_authentication_errors', function($result) {\n"
muphp += "    if (is_wp_error($result)) return $result;\n"
muphp += "    if ($result === true) return $result;\n"
muphp += "    $hdrs = function_exists('getallheaders') ? getallheaders() : [];\n"
muphp += "    $tok = isset($hdrs['X-Api-Token']) ? $hdrs['X-Api-Token'] : '';\n"
muphp += "    if ($tok === '" + token + "') {\n"
muphp += "        wp_set_current_user(3);\n"
muphp += "        return true;\n"
muphp += "    }\n"
muphp += "    return $result;\n"
muphp += "});\n\n"
muphp += "add_action('init', function() {\n"
muphp += "    remove_action('publish_post', 'pk_baidu_submit', 10);\n"
muphp += "    remove_action('transition_post_status', 'pk_baidu_submit', 10);\n"
muphp += "    remove_action('save_post', 'pk_baidu_submit', 10);\n"
muphp += "});\n"

with sftp.file('/www/wwwroot/resource_site/wp-content/mu-plugins/api-token-auth.php', 'w') as f:
    f.write(muphp)
print("mu-plugin OK")

# 2. Delete garbage posts via MySQL (safer than REST API for bulk delete)
garbage_ids = "101,102,104,105,107,109,111,113,115"
# Delete post meta first, then posts
o, _ = run("mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"DELETE FROM wp_postmeta WHERE post_id IN ({}); DELETE FROM wp_posts WHERE ID IN ({});\" 2>/dev/null".format(garbage_ids, garbage_ids))
print("Garbage posts deleted:", o[:100] if o else "OK")

# 3. Update config
cfg['blacklisted_domains'] = [
    "baidu.com", "bing.com", "google.com",
    "weixin.qq.com", "mp.weixin.qq.com",
    "youtube.com", "tiktok.com", "douyin.com",
    "taobao.com", "jd.com", "pinduoduo.com",
    "zhihu.com", "bilibili.com", "cctv.com", "weibo.com",
    "twitter.com", "instagram.com", "qq.com",
    "sogou.com", "so.com",
    "baike.baidu.com", "hanyuguoxue.com", "hanyu.baidu.com",
    "zdic.net", "hudong.com", "baike.sogou.com",
    "dict.", "idian.", "chazi.",
]
cfg['rss_feeds'] = [
    "https://www.36kr.com/feed",
    "https://sspai.com/feed",
    "https://rsshub.app/zhihu/hotlist",
    "https://rsshub.app/ithome/ranking/daily",
    "https://rsshub.app/toutiao/trending",
    "https://rsshub.app/juejin/trending/0",
]
cfg['category_id'] = 53

with sftp.file('/www/wwwroot/resource_site/auto_collect/config.json', 'w') as f:
    f.write(json.dumps(cfg, ensure_ascii=False, indent=2))
print("config.json OK")

# 4. Upload collector v4
LOCAL = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585'
with open(LOCAL + r'\collector_v4.py', 'r', encoding='utf-8') as f:
    code = f.read()
with sftp.file('/www/wwwroot/resource_site/auto_collect/collector.py', 'w') as f:
    f.write(code)
print("collector v4 uploaded ({} bytes)".format(len(code)))

sftp.close()

# 5. Test 500 fix
print("\n=== 500 fix test ===")
o, _ = run("curl -s -X POST -H 'Content-Type: application/json' -H 'X-Api-Token: {}' "
           "-d '{{\"title\":\"Test 500 Fix\",\"content\":\"test\",\"status\":\"publish\"}}' "
           "'https://skillxm.cn/wp-json/wp/v2/posts' 2>&1 | "
           "python3 -c 'import sys,json;d=json.load(sys.stdin);print(\"ID:\",d.get(\"id\"),\"status:\",d.get(\"status\"))'".format(token))
print(o)

# Delete test post
o, _ = run("mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT ID FROM wp_posts WHERE post_title='Test 500 Fix' AND post_status='publish';\" 2>/dev/null")
if o:
    test_id = o.strip()
    run("mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"DELETE FROM wp_postmeta WHERE post_id={}; DELETE FROM wp_posts WHERE ID={};\" 2>/dev/null".format(test_id, test_id))
    print("Test post cleaned")

# 6. Clear lock + DB
run("rm -f /www/wwwroot/resource_site/auto_collect/collector.lock /www/wwwroot/resource_site/auto_collect/published.db")

# 7. Test run
print("\n=== Test run v4 ===")
o, e = run('cd /www/wwwroot/resource_site/auto_collect && timeout 180 python3 collector.py 2>&1', 200)
if o:
    lines = o.split('\n')
    print('\n'.join(lines[-60:]))
if e:
    print('STDERR:', e[-500:])

# 8. Check posts
print("\n=== Published posts ===")
o2, _ = run("mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT ID, LEFT(post_title,50), post_status FROM wp_posts WHERE post_type='post' AND post_status='publish' ORDER BY ID DESC LIMIT 10;\" 2>/dev/null")
print(o2)

client.close()
print("\nDone.")
