import paramiko, json, sys, traceback
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

def run(cmd, t=30):
    _, o, e = client.exec_command(cmd, timeout=t)
    out = o.read().decode('utf-8', errors='replace').strip()
    err = e.read().decode('utf-8', errors='replace').strip()
    return out, err

sftp = client.open_sftp()

# 1. Update config - blacklist zhihu + video platforms, improve keywords
with sftp.file('/www/wwwroot/resource_site/auto_collect/config.json', 'r') as f:
    cfg = json.loads(f.read())

cfg['blacklisted_domains'] = [
    "baidu.com", "bing.com", "google.com",
    "weixin.qq.com", "mp.weixin.qq.com",
    "youtube.com", "tiktok.com", "douyin.com",
    "taobao.com", "jd.com", "pinduoduo.com",
    "zhihu.com",  # JS-rendered, can't scrape
    "bilibili.com",  # video platform
    "cctv.com",  # video platform
    "weibo.com",  # social media
    "twitter.com", "instagram.com",
    "qq.com",  # mostly JS
    "sogou.com", "so.com",
]

# Keywords targeting blog-style articles (easier to scrape)
cfg['keywords'] = [
    "\u8d5a\u94b1\u65b9\u6cd5 blog \u6559\u7a0b",
    "\u526f\u4e1a\u8d5a\u94b1\u5b9e\u64cd \u65b9\u6cd5",
    "\u7f51\u8d5a\u65b9\u6cd5 \u5168\u6d41\u7a0b \u6559\u7a0b",
    "\u65b0\u624b\u8d5a\u94b1\u6559\u7a0b 2025 \u5b9e\u64cd",
    "\u81ea\u5a92\u4f53\u8fd0\u8425 \u53d8\u73b0 \u6559\u7a0b",
    "\u7406\u8d22\u5165\u95e8 \u6295\u8d44\u6559\u7a0b",
    "\u7535\u5546\u521b\u4e1a \u8d5a\u94b1\u6848\u4f8b",
    "\u77ed\u89c6\u9891\u5236\u4f5c \u53d8\u73b0 \u6559\u7a0b",
    "\u88ab\u52a8\u6536\u5165 \u5efa\u7acb \u65b9\u6cd5",
    "\u81ea\u7531\u804c\u4e1a \u5168\u804c\u8d5a\u94b1",
    "\u5fae\u4fe1\u516c\u4f17\u53f7 \u8d5a\u94b1 \u65b9\u6cd5",
    "\u76f4\u64ad\u5e26\u8d27 \u5165\u95e8 \u6559\u7a0b",
    "\u77e5\u8bc6\u53d8\u73b0 \u6280\u80fd \u8d5a\u94b1",
    "\u4e92\u8054\u7f51\u521b\u4e1a \u7ecf\u9a8c \u5206\u4eab",
    "\u5c0f\u672c\u521b\u4e1a \u8d5a\u94b1 \u9879\u76ee",
]

cfg['min_content_length'] = 800  # higher threshold for quality
cfg['max_posts_per_run'] = 8

with sftp.file('/www/wwwroot/resource_site/auto_collect/config.json', 'w') as f:
    f.write(json.dumps(cfg, ensure_ascii=False, indent=2))
print('config.json updated')

# 2. Upload collector v3 with Google search and better filtering
LOCAL = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585'
with open(LOCAL + r'\collector_v3.py', 'r', encoding='utf-8') as f:
    code = f.read()
with sftp.file('/www/wwwroot/resource_site/auto_collect/collector.py', 'w') as f:
    f.write(code)
print('collector.py v3 uploaded ({} bytes)'.format(len(code)))

sftp.close()

# 3. Clear lock + reset DB (fresh start)
run('rm -f /www/wwwroot/resource_site/auto_collect/collector.lock')
run('rm -f /www/wwwroot/resource_site/auto_collect/published.db')
print('Lock and DB cleared')

# 4. Test run
print('\n=== Test run ===')
o, e = run('cd /www/wwwroot/resource_site/auto_collect && timeout 180 python3 collector.py 2>&1', 200)
if o:
    # Show the end of output (most interesting part)
    lines = o.split('\n')
    print('\n'.join(lines[-80:]))
if e:
    print('STDERR:', e[-500:])

# 5. Check published posts
print('\n=== Recent posts ===')
o2, _ = run("curl -s -H 'X-Api-Token: {}' 'https://skillxm.cn/wp-json/wp/v2/posts?per_page=5&orderby=date' 2>&1 | python3 -c \"import sys,json; posts=json.load(sys.stdin); [print('ID:{} {} | {}'.format(p['id'], p['date'][:16], p['title']['rendered'][:40])) for p in posts]\"".format(cfg.get('wp_api_token', '')))
print(o2)

client.close()
print('\nDone.')
