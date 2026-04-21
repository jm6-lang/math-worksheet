import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 生成死链XML文件放到网站根目录
deadlink_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.skillxm.cn/this-page-does-not-exist-12345.html</loc>
    <lastmod>2026-04-08</lastmod>
  </url>
</urlset>'''

deadlink_txt = '''https://www.skillxm.cn/this-page-does-not-exist-12345.html'''

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/deadlinks.xml', 'w') as f:
    f.write(deadlink_xml)
with sftp.open('/www/wwwroot/resource_site/deadlinks.txt', 'w') as f:
    f.write(deadlink_txt)
sftp.close()

print("已上传到网站根目录：")
print(f"  XML: https://www.skillxm.cn/deadlinks.xml")
print(f"  TXT: https://www.skillxm.cn/deadlinks.txt")

ssh.close()
