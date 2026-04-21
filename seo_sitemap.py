# -*- coding: utf-8 -*-
import pymysql
from datetime import datetime

conn = pymysql.connect(host='localhost', user='wpuser', password='WpPass2024!', database='wp_skillxm', charset='utf8mb4')
cursor = conn.cursor()

cursor.execute("SELECT ID, post_modified_gmt FROM wp_posts WHERE post_type='post' AND post_status='publish' ORDER BY ID")
posts = cursor.fetchall()

SITE_URL = 'https://skillxm.cn'
now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

print("Total posts: {}".format(len(posts)), flush=True)

# === Category sitemap ===
cat_urls = [
    ('AI\u77e5\u8bc6', '/category/ai-zhi-shi'),
    ('\u5de5\u5177\u5408\u96c6', '/category/gong-ju-he-ji'),
    ('\u5f71\u89c6\u5a31\u4e50', '/category/ying-shi-yu-le'),
    ('\u81ea\u5a92\u4f53\u8fd0\u8425', '/category/zi-mei-ti-yun-ying'),
    ('\u6559\u80b2\u8d44\u6e90', '/category/jiao-yu-zi-yuan'),
    ('\u8de8\u5883\u7535\u5546', '/category/kua-jing-dian-shang'),
    ('\u4f20\u7edf\u6587\u5316', '/category/chuan-tong-wen-hua'),
    ('\u4e66\u7c4d\u8d44\u6599', '/category/shu-ji-zi-liao'),
]

cat_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
cat_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for cat_name, cat_slug in cat_urls:
    cat_xml += '  <url><loc>{}{}</loc><lastmod>{}</lastmod><changefreq>daily</changefreq><priority>0.8</priority></url>\n'.format(SITE_URL, cat_slug, now)
cat_xml += '</urlset>'

with open('/www/wwwroot/skillxm.cn/public/category-sitemap.xml', 'w') as f:
    f.write(cat_xml)
print("Category sitemap OK", flush=True)

# === Post sitemap ===
total = len(posts)
post_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
post_xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for i, (post_id, modified) in enumerate(posts):
    mod = modified.strftime('%Y-%m-%dT%H:%M:%SZ') if modified else now
    priority = '0.7' if post_id > total * 0.5 else '0.6'
    post_xml += '  <url><loc>{}/?p={}</loc><lastmod>{}</lastmod><changefreq>weekly</changefreq><priority>{}</priority></url>\n'.format(SITE_URL, post_id, mod, priority)
    if (i + 1) % 200 == 0:
        print("Progress: {}/{}".format(i+1, total), flush=True)
post_xml += '</urlset>'

with open('/www/wwwroot/skillxm.cn/public/post-sitemap.xml', 'w') as f:
    f.write(post_xml)
print("Post sitemap OK ({} posts)".format(total), flush=True)

# === Sitemap index ===
idx_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
idx_xml += '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
idx_xml += '  <sitemap><loc>{}/post-sitemap.xml</loc><lastmod>{}</lastmod></sitemap>\n'.format(SITE_URL, now)
idx_xml += '  <sitemap><loc>{}/category-sitemap.xml</loc><lastmod>{}</lastmod></sitemap>\n'.format(SITE_URL, now)
idx_xml += '</sitemapindex>'

with open('/www/wwwroot/skillxm.cn/public/sitemap_index.xml', 'w') as f:
    f.write(idx_xml)
print("Sitemap index OK", flush=True)

conn.close()
print("All sitemap files created!", flush=True)
