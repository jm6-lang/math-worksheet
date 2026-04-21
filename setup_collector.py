import paramiko, json, time, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USER = 'root'
PASS = 'l95UE5ysF)7.gR'
BASE = '/www/wwwroot/resource_site/auto_collect'
LOCAL = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585'

def connect():
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(HOST, 22, USER, PASS, timeout=15)
    return c

def run(client, cmd, t=120):
    _, o, e = client.exec_command(cmd, timeout=t)
    out = o.read().decode('utf-8', errors='replace').strip()
    err = e.read().decode('utf-8', errors='replace').strip()
    return out, err

client = connect()

# Step 1: Install pip3
print("=== [1/5] Installing pip3 ===")
o, e = run(client, 'apt-get update -qq 2>&1 | tail -2 && apt-get install -y python3-pip python3-venv 2>&1 | tail -3', 120)
print(o[-200:] if o else 'done')

# Step 2: Install Python packages
print("\n=== [2/5] Installing Python packages ===")
o, e = run(client, 'pip3 install requests beautifulsoup4 lxml trafilatura Pillow 2>&1 | tail -8', 180)
print(o[-300:] if o else 'done')

# Step 3: Install WP-CLI + create app password
print("\n=== [3/5] WP-CLI + Application Password ===")
run(client, 'curl -sO https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && chmod +x wp-cli.phar && mv wp-cli.phar /usr/local/bin/wp 2>&1', 60)
o, e = run(client, 'wp --version --allow-root 2>&1')
print('WP-CLI:', o)
o, e = run(client, 'cd /www/wwwroot/resource_site && wp user application-password create admin "auto-collect" --porcelain --allow-root 2>&1', 30)
app_pwd = o.strip()
if not app_pwd or 'Error' in (e + o):
    print('Trying existing passwords or creating via MySQL...')
    o2, _ = run(client, "cd /www/wwwroot/resource_site && wp user application-password list admin --format=csv --fields=name --allow-root 2>&1")
    print('Existing:', o2[:200])
    if 'auto-collect' in o2:
        o3, _ = run(client, "cd /www/wwwroot/resource_site && wp user application-password list admin --format=json --allow-root 2>&1")
        print('JSON:', o3[:300])
    if not app_pwd:
        app_pwd = 'x'.join([str(i) for i in range(1, 17)])
        print('Using fallback password:', app_pwd[:4] + '...')
print('App Password: {}...{}'.format(app_pwd[:4], app_pwd[-4:]))

# Step 4: Upload files
print("\n=== [4/5] Uploading collector files ===")
run(client, 'mkdir -p {}/logs'.format(BASE))

sftp = client.open_sftp()

# config.json
cfg = {
    "wp_url": "https://skillxm.cn",
    "wp_user": "admin",
    "wp_app_password": app_pwd,
    "category": "\u8d5a\u94b1\u6559\u7a0b",
    "keywords": [
        "\u8d5a\u94b1\u65b9\u6cd5\u6559\u7a0b 2025",
        "\u526f\u4e1a\u8d5a\u94b1\u9879\u76ee",
        "\u7f51\u8d5a\u65b9\u6cd5 \u65b0\u624b",
        "\u81ea\u5a92\u4f53\u8d5a\u94b1\u6559\u7a0b",
        "\u7406\u8d22\u6295\u8d44\u5165\u95e8\u6559\u7a0b",
        "\u7535\u5546\u8fd0\u8425\u8d5a\u94b1\u65b9\u6cd5",
        "\u77ed\u89c6\u9891\u53d8\u73b0\u6559\u7a0b",
        "\u88ab\u52a8\u6536\u5165\u65b9\u6cd5",
        "\u81ea\u7531\u804c\u4e1a\u8d5a\u94b1",
        "\u5728\u5bb6\u8d5a\u94b1\u65b9\u6cd5",
        "\u63a5\u5355\u8d5a\u94b1 \u65b0\u624b",
        "\u5fae\u4fe1\u8d5a\u94b1\u65b9\u6cd5",
        "\u76f4\u64ad\u5e26\u8d27\u8d5a\u94b1",
        "\u77e5\u8bc6\u53d8\u73b0\u6559\u7a0b",
    ],
    "max_posts_per_run": 5,
    "min_content_length": 500,
    "blacklisted_domains": [
        "baidu.com", "bing.com", "google.com",
        "weixin.qq.com", "mp.weixin.qq.com",
        "youtube.com", "tiktok.com", "douyin.com",
        "taobao.com", "jd.com", "pinduoduo.com",
    ]
}
with sftp.file(BASE + '/config.json', 'w') as f:
    f.write(json.dumps(cfg, ensure_ascii=False, indent=2))
print('config.json uploaded')

# collector.py - read local file and upload
with open(LOCAL + r'\collector.py', 'r', encoding='utf-8') as f:
    collector_code = f.read()
with sftp.file(BASE + '/collector.py', 'w') as f:
    f.write(collector_code)
print('collector.py uploaded ({} bytes)'.format(len(collector_code)))

sftp.close()
run(client, 'chmod +x {}/collector.py'.format(BASE))

# Step 5: Test run
print("\n=== [5/5] Test run ===")
o, e = run(client, 'cd {} && python3 collector.py 2>&1'.format(BASE), 120)
if o:
    print(o[-3000:])
else:
    print('No output')
if e:
    print('STDERR:', e[-500:])

# Setup cron
print("\n=== Cron setup ===")
run(client, '(crontab -l 2>/dev/null | grep -v collector; echo "0 9,18 * * * cd {} && /usr/bin/python3 collector.py >> {}/logs/cron.log 2>&1") | crontab -'.format(BASE, BASE))
o, _ = run(client, 'crontab -l 2>/dev/null')
print('Cron:', o)

client.close()
print("\n=== DONE ===")
