# -*- coding: utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# ===== Step 6: Generate XML Sitemap manually =====
sitemap_script = r'''# -*- coding: utf-8 -*-
import pymysql
from datetime import datetime

conn = pymysql.connect(host='localhost', user='wpuser', password='WpPass2024!', database='wp_skillxm', charset='utf8mb4')
cursor = conn.cursor()

cursor.execute("""
    SELECT ID, post_modified_gmt 
    FROM wp_posts 
    WHERE post_type='post' AND post_status='publish' 
    ORDER BY ID
""")
posts = cursor.fetchall()

SITE_URL = 'https://skillxm.cn'
BATCH_SIZE = 1000
now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

# Generate sitemap_index
sitemap_index = '''<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="''' + SITE_URL + '''/main-sitemap.xsl"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
'''

# Generate category sitemap
cat_sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
'''

# Category URLs
cat_urls = [
    ('AI知识', '/category/ai-zhi-shi'),
    ('工具合集', '/category/gong-ju-he-ji'),
    ('影视娱乐', '/category/ying-shi-yu-le'),
    ('自媒体运营', '/category/zi-mei-ti-yun-ying'),
    ('教育资源', '/category/jiao-yu-zi-yuan'),
    ('跨境电商', '/category/kua-jing-dian-shang'),
    ('传统文化', '/category/chuan-tong-wen-hua'),
    ('书籍资料', '/category/shu-ji-zi-liao'),
    ('赚钱教程', '/category/zhuan-qian-jiao-cheng'),
    ('课程资料', '/category/ke-cheng-zi-liao'),
]

for cat_name, cat_slug in cat_urls:
    cat_sitemap += '''  <url>
    <loc>{}/{}</loc>
    <lastmod>{}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
'''.format(SITE_URL, cat_slug, now)

cat_sitemap += '</urlset>'

with open('/www/wwwroot/skillxm.cn/public/category-sitemap.xml', 'w') as f:
    f.write(cat_sitemap)

print("Category sitemap created", flush=True)

# Split posts into chunks for sitemap
total = len(posts)
chunk_size = 1000
chunks = [posts[i:i+chunk_size] for i in range(0, total, chunk_size)]

for idx, chunk in enumerate(chunks):
    sitemap_file = '/www/wwwroot/skillxm.cn/public/sitemap-{}.xml'.format(idx + 1)
    
    content = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
'''
    
    for post_id, modified_gmt in chunk:
        url = '{}/?p={}'.format(SITE_URL, post_id)
        # Use proper slug if available
        mod_date = modified_gmt.strftime('%Y-%m-%dT%H:%M:%SZ') if modified_gmt else now
        
        # Priority based on ID (newer = higher)
        priority = '0.6'
        if post_id > total * 0.8:
            priority = '0.8'
        elif post_id > total * 0.5:
            priority = '0.7'
        
        content += '''  <url>
    <loc>{}</loc>
    <lastmod>{}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>{}</priority>
  </url>
'''.format(url, mod_date, priority)
    
    content += '</urlset>'
    
    with open(sitemap_file, 'w') as f:
        f.write(content)
    
    sitemap_index += '''  <sitemap>
    <loc>{}/sitemap-{}.xml</loc>
    <lastmod>{}</lastmod>
  </sitemap>
'''.format(SITE_URL, idx + 1, now)
    print("Created sitemap-{} with {} posts".format(idx + 1, len(chunk)), flush=True)

sitemap_index += '</sitemapindex>'

with open('/www/wwwroot/skillxm.cn/public/sitemap_index.xml', 'w') as f:
    f.write(sitemap_index)

print("\nMain sitemap_index created!", flush=True)

conn.close()

# Create main-sitemap.xsl for browser-friendly view
xsl = '''<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
    xmlns:html="http://www.w3.org/1999/xhtml"
    xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="html" encoding="UTF-8"/>
  <xsl:template match="/">
    <html>
      <head>
        <title>XML Sitemap - AI知识资源网</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
        <style>
          body { font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
          table { width: 100%; border-collapse: collapse; }
          th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
          th { background-color: #333; color: white; }
          tr:nth-child(even) { background-color: #f2f2f2; }
          a { color: #1a73e8; text-decoration: none; }
          a:hover { text-decoration: underline; }
          h1 { color: #333; }
        </style>
      </head>
      <body>
        <h1>XML Sitemap - AI知识资源网</h1>
        <p>总计URL数量：<xsl:value-of select="count(sitemap:sitemapindex/sitemap:sitemap)"/> 个子站点图</p>
        <table>
          <tr><th>站点图文件</th><th>最后更新</th></tr>
          <xsl:for-each select="sitemap:sitemapindex/sitemap:sitemap">
            <tr>
              <td><a><xsl:attribute name="href"><xsl:value-of select="sitemap:loc"/></xsl:attribute><xsl:value-of select="sitemap:loc"/></a></td>
              <td><xsl:value-of select="sitemap:lastmod"/></td>
            </tr>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
'''

with open('/www/wwwroot/skillxm.cn/public/main-sitemap.xsl', 'w') as f:
    f.write(xsl)

print("XSL stylesheet created!", flush=True)
print("\nAll sitemap files created!", flush=True)
'''

sftp = ssh.open_sftp()
with sftp.open('/root/scripts/seo_sitemap.py', 'w') as f:
    f.write(sitemap_script)
sftp.close()

print("Generating sitemap...", flush=True)
stdin, stdout, stderr = ssh.exec_command("cd /root/scripts && python3 seo_sitemap.py", timeout=120)
output = stdout.read().decode('utf-8', errors='replace').strip()
print(output, flush=True)

# Verify sitemap
print("\nVerifying sitemap...", flush=True)
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/skillxm.cn/public/sitemap*.xml && wc -l /www/wwwroot/skillxm.cn/public/sitemap_index.xml", timeout=10)
out = stdout.read().decode('utf-8', errors='replace').strip()
print(out, flush=True)

ssh.close()
