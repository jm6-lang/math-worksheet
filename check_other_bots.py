import paramiko

server = '240b:4001:278:8402:0:bd18:bd09:af0d'
port = 22222
user = 'root'
password = 'Langlang0.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server, port=port, username=user, password=password,
               timeout=20, allow_agent=False, look_for_keys=False)

def cmd(c, timeout=60):
    stdin, stdout, stderr = client.exec_command(c, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# 提取所有唯一的 User-Agent
print('=== 全部唯一 User-Agent（去重统计）===')
ua_output = cmd("grep -E 'access\\.log' /var/log/nginx/access.log 2>/dev/null | awk -F'\"' '{print $6}' | sort | uniq -c | sort -rn | head -60")
print(ua_output)

print()
print('=== 按爬虫/蜘蛛分类统计 ===')

# 各类常见爬虫关键词
bots = {
    'Bingbot': 'bingbot|Bingbot|msnbot',
    'Yandex': 'YandexBot|YandexImages',
    'Baidu': 'Baiduspider|baidu.com',
    'Sogou': 'Sogou|spider',
    '360': '360Spider|360',
    'Bytespider': 'Bytespider|bytedance',
    'Twitter/X': 'Twitterbot|Twitter',
    'Facebook': 'facebookexternalhit|facebook',
    'DuckDuckGo': 'DuckDuckBot|duckduckgo',
    'Apple': 'Applebot',
    'Slack': 'Slackbot',
    'Telegram': 'TelegramBot',
    'Amazon': 'Amazonbot|Alexa',
    'Ahrefs': 'AhrefsBot|ahrefs',
    'Semrush': 'SemrushBot|semrush',
    'MJ12bot': 'MJ12bot|majestic',
    'Dotbot': 'Dotbot|dotbot',
    'DataForSeo': 'DataForSeoBot|dataforseo',
    'Screaming': 'Screaming|scREEM',
    'GPTBot': 'GPTBot|ChatGPT-User|CCBot',
    'Claude': 'Claude-Web|ClaudeBot',
    'Perplexity': 'PerplexityBot|perplexity',
    'YouBot': 'YouBot|you.com',
    'Brave': 'Brave/1',
    'Turnitin': 'TurnitinBot',
    'Goose': 'Goose|feather',
    'Zoomin': 'ZoominBot',
    'Linespider': 'Linespider',
    'Yisou': 'Yisou|umanye',
    'Shenma': 'Shenma',
    'Haosou': 'HaosouSpider',
    'Other spider': 'spider|bot|crawl',
}

for name, pattern in bots.items():
    count = cmd(f'grep -i "{pattern}" /var/log/nginx/access.log 2>/dev/null | wc -l').strip()
    if int(count) > 0:
        print(f'{name:20s}: {count} 条')

print()
print('=== 完整 IP 访问排行 TOP 30（非搜索引擎）===')
print('(排除 Googlebot / Baidu / 已知的假爬虫 IP)')
exclude_ips = '|'.join([
    '66.249.69', '66.249.64', '66.249.65', '66.249.66', '66.249.67', '66.249.68',
    '72.14.199', '74.125.', '142.250.', '172.217.', '209.85.'
])
print(cmd(f"grep -vE '{exclude_ips}' /var/log/nginx/access.log 2>/dev/null | grep -oE '[0-9]{{1,3}}\\.[0-9]{{1,3}}\\.[0-9]{{1,3}}\\.[0-9]{{1,3}}' | sort | uniq -c | sort -rn | head -30"))

print()
print('=== 按国家/地区分布 TOP 20 IP ===')
# 简化版：通过 IP 前缀估算地区
print(cmd("grep -oE '[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}' /var/log/nginx/access.log 2>/dev/null | sort -u | head -5"))

# 扫描可疑 User-Agent（非正常浏览器）
print()
print('=== 非正常 User-Agent（非浏览器）TOP 30 ===')
non_browser = cmd("grep -iE 'curl|wget|python|scrapy|requests|httpclient|java-|go-http|axios|node-fetch|phantomjs|selenium|playwright|puppeteer|jsdom|libwww|perl|ruby|php|java/| okhttp|apache-http|nginx|httpx|aiohttp|fetch|mechanize' /var/log/nginx/access.log 2>/dev/null | awk -F'\"' '{print $6}' | sort | uniq -c | sort -rn | head -30")
print(non_browser or '无')

print()
print('=== 这些非浏览器爬虫的 IP 来源 ===')
print(cmd("grep -iE 'curl|wget|python|scrapy|requests|java-|go-http|axios|node-fetch|phantomjs|selenium|playwright|puppeteer|httpx|aiohttp|mechanize' /var/log/nginx/access.log 2>/dev/null | grep -oE '[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}' | sort | uniq -c | sort -rn | head -20"))

client.close()
