# -*- coding: utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# Upload the sitemap script directly
sftp = ssh.open_sftp()

sitemap_script = sftp.open('/root/scripts/seo_sitemap.py', 'w')
sitemap_script.write('# -*- coding: utf-8 -*-\n')
sitemap_script.write('import pymysql\nfrom datetime import datetime\n\n')
sitemap_script.write("conn = pymysql.connect(host='localhost', user='wpuser', password='WpPass2024!', database='wp_skillxm', charset='utf8mb4')\n")
sitemap_script.write('cursor = conn.cursor()\n\n')

sitemap_script.write("cursor.execute(\"SELECT ID, post_modified_gmt FROM wp_posts WHERE post_type='post' AND post_status='publish' ORDER BY ID\")\n")
sitemap_script.write('posts = cursor.fetchall()\n\n')

sitemap_script.write("SITE_URL = 'https://skillxm.cn'\n")
sitemap_script.write("now = datetime.utcnow().strftime('%%Y-%%m-%%dT%%H:%%M:%%SZ')\n\n")

# Category sitemap
sitemap_script.write("cat_urls = [('AI知识', '/category/ai-zhi-shi'), ('工具合集', '/category/gong-ju-he-ji'), ('影视娱乐', '/category/ying-shi-yu-le'), ('自媒体运营', '/category/zi-mei-ti-yun-ying'), ('教育资源', '/category/jiao-yu-zi-yuan'), ('跨境电商', '/category/kua-jing-dian-shang'), ('传统文化', '/category/chuan-tong-wen-hua'), ('书籍资料', '/category/shu-ji-zi-liao')]\n\n")

sitemap_script.write('cat_xml = \'\'\'<?xml version="1.0" encoding="UTF-8"?>\\n\'\'\'\n')
sitemap_script.write('cat_xml += \'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\\n\'\n\n')

sitemap_script.write('for cat_name, cat_slug in cat_urls:\n')
sitemap_script.write('    cat_xml += f\'  <url><loc>{SITE_URL}{cat_slug}</loc><lastmod>{now}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>\\n\'\n\n')

sitemap_script.write('cat_xml += \'</urlset>\'\n')
sitemap_script.write("with open('/www/wwwroot/skillxm.cn/public/category-sitemap.xml', 'w') as f:\n    f.write(cat_xml)\n")
sitemap_script.write("print('Category sitemap OK')\n\n")

# Post sitemap
sitemap_script.write('total = len(posts)\n')
sitemap_script.write('post_xml = \'\'\'<?xml version="1.0" encoding="UTF-8"?>\\n\'\'\'\n')
sitemap_script.write("post_xml += '<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\\n'\n\n")

sitemap_script.write('for i, (post_id, modified) in enumerate(posts):\n')
sitemap_script.write('    mod = modified.strftime(\'%%Y-%%m-%%dT%%H:%%M:%%SZ\') if modified else now\n')
sitemap_script.write('    priority = \'0.7\' if post_id > total * 0.5 else \'0.6\'\n')
sitemap_script.write('    post_xml += f\'  <url><loc>{SITE_URL}/?p={post_id}</loc><lastmod>{mod}</lastmod><changefreq>weekly</changefreq><priority>{priority}</priority></url>\\n\'\n')
sitemap_script.write("    if (i + 1) %% 200 == 0:\n        print(f'Progress: {i+1}/{total}')\n\n")

sitemap_script.write('post_xml += \'</urlset>\'\n')
sitemap_script.write("with open('/www/wwwroot/skillxm.cn/public/post-sitemap.xml', 'w') as f:\n    f.write(post_xml)\n")
sitemap_script.write("print(f'Post sitemap OK ({total} posts)')\n\n")

# Sitemap index
sitemap_script.write("idx_xml = \'\'\'<?xml version=\"1.0\" encoding=\"UTF-8\"?>\\n\'\'\'\n")
sitemap_script.write("idx_xml += '<sitemapindex xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\\n'\n")
sitemap_script.write("idx_xml += f'  <sitemap><loc>{SITE_URL}/post-sitemap.xml</loc><lastmod>{now}</lastmod></sitemap>\\n'\n")
sitemap_script.write("idx_xml += f'  <sitemap><loc>{SITE_URL}/category-sitemap.xml</loc><lastmod>{now}</lastmod></sitemap>\\n'\n")
sitemap_script.write("idx_xml += '</sitemapindex>'\n\n")
sitemap_script.write("with open('/www/wwwroot/skillxm.cn/public/sitemap_index.xml', 'w') as f:\n    f.write(idx_xml)\n")
sitemap_script.write("print('Sitemap index OK')\n\n")
sitemap_script.write('conn.close()\n')

sitemap_script.close()
sftp.close()

print("Sitemap script uploaded. Running...", flush=True)
stdin, stdout, stderr = ssh.exec_command("cd /root/scripts && python3 seo_sitemap.py", timeout=180)
output = stdout.read().decode('utf-8', errors='replace').strip()
print(output, flush=True)
err = stderr.read().decode('utf-8', errors='replace').strip()
if err and 'error' in err.lower():
    print("ERR:", err[:300], flush=True)

# Verify
print("\nVerifying...", flush=True)
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/skillxm.cn/public/sitemap*.xml", timeout=10)
print(stdout.read().decode('utf-8', errors='replace').strip(), flush=True)

ssh.close()
