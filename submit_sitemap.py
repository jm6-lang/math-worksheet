import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

cmds = [
    # Google sitemap ping
    "curl -s 'https://www.google.com/ping?sitemap=https://skillxm.cn/sitemap_index.xml' 2>/dev/null | head -5",
    "echo '---'",
    
    # Google Search Console API - use the URL Inspection API
    # First try Bing (accepts sitemap submissions via API)
    "curl -s -o /dev/null -w 'Bing: HTTP %{http_code}' 'https://www.bing.com/ping?sitemap=https://skillxm.cn/sitemap_index.xml' 2>/dev/null",
    "echo ''",
    
    # Yandex
    "curl -s -o /dev/null -w 'Yandex: HTTP %{http_code}' 'https://webmaster.yandex.ru/ping?sitemap=https://skillxm.cn/sitemap_index.xml' 2>/dev/null",
    "echo ''",
    
    # Submit individual URLs to Baidu via their link submit API (requires token, but try ping)
    "curl -s -o /dev/null -w 'Baidu ping: HTTP %{http_code}' 'http://ping.baidu.com/ping/RPC2' -H 'Content-Type: text/xml' -d '<?xml version=\"1.0\" encoding=\"UTF-8\"?><methodCall><methodName>weblogUpdates.ping</methodName><params><param><value>AI知识资源网</value></param><param><value>https://skillxm.cn</value></param></params></methodCall>' 2>/dev/null",
    "echo ''",
    
    # Verify our sitemap is accessible from outside
    "curl -s -o /dev/null -w 'Sitemap from outside: HTTP %{http_code}' 'https://skillxm.cn/sitemap_index.xml' 2>/dev/null",
    "echo ''",
    "curl -s -o /dev/null -w 'Post sitemap: HTTP %{http_code}' 'https://skillxm.cn/post-sitemap.xml' 2>/dev/null",
    "echo ''",
    "curl -s -o /dev/null -w 'Robots: HTTP %{http_code}' 'https://skillxm.cn/robots.txt' 2>/dev/null",
    "echo ''",
    
    # Show sitemap content
    "curl -s 'https://skillxm.cn/sitemap_index.xml' 2>/dev/null",
    "echo ''",
]

for c in cmds:
    if c == 'echo \'---\'':
        print("---", flush=True)
        continue
    print(">> " + c, flush=True)
    stdin, stdout, stderr = ssh.exec_command(c, timeout=20)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    if out:
        print(out, flush=True)
    print(flush=True)

ssh.close()
