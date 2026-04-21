# -*- coding: utf-8 -*-
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# ===== Step 4: Add meta descriptions and Yoast SEO meta to all posts =====
meta_script = r'''# -*- coding: utf-8 -*-
import pymysql
import re

conn = pymysql.connect(host='localhost', user='wpuser', password='WpPass2024!', database='wp_skillxm', charset='utf8mb4')
cursor = conn.cursor()

# Get all posts
cursor.execute("SELECT ID, post_title, post_content, post_name FROM wp_posts WHERE post_type='post' AND post_status='publish' ORDER BY ID")
rows = cursor.fetchall()
print("Processing {} posts...".format(len(rows)), flush=True)

# Category to keyword mapping for meta
cat_keywords = {
    'AI知识': 'AI教程_AI工具_人工智能学习',
    '工具合集': '实用工具_软件工具_电脑工具',
    '影视娱乐': '影视资源_电影_电视剧_高清下载',
    '自媒体运营': '自媒体运营_短视频变现_抖音教程',
    '传统文化': '传统文化_国学经典_中医养生',
    '书籍资料': '电子书籍_电子书下载_PDF资源',
    '教育资源': '在线课程_教学视频_学习教程',
    '跨境电商': '跨境电商教程_亚马逊运营_SHOPEE',
    ' Uncategorized': '资源分享',
    '赚钱教程': '副业赚钱_网络创业_兼职项目',
    '课程资料': '课程资源_教学视频_学习资料',
}

updated = 0
skipped = 0

for post_id, title, content, post_name in rows:
    # Generate meta description from content (first 150 chars of text)
    text_only = re.sub(r'<[^>]+>', '', content)
    text_only = re.sub(r'\s+', ' ', text_only).strip()
    
    # Get category for keywords
    cursor.execute("""
        SELECT t.name FROM wp_terms t 
        JOIN wp_term_taxonomy tt ON t.term_id=tt.term_id 
        JOIN wp_term_relationships tr ON tt.term_taxonomy_id=tr.term_taxonomy_id 
        WHERE tr.object_id=%s AND tt.taxonomy='category' LIMIT 1
    """, (post_id,))
    row = cursor.fetchone()
    cat_name = row[0] if row else '资源'
    keywords_base = cat_keywords.get(cat_name, '免费资源_学习资料')
    
    # Meta description: 150-160 chars
    meta_desc = text_only[:155].strip() if text_only else title + '免费资源分享'
    if len(meta_desc) > 155:
        meta_desc = meta_desc[:152] + '...'
    
    # SEO title: title + site name suffix
    seo_title = title[:55] + ' - AI知识资源网免费分享' if len(title) > 55 else title + ' 免费资源下载'
    
    # Clean post name for slug (already done in WP, but ensure it's URL-friendly)
    
    try:
        # Yoast SEO meta: _yoast_wpseo_title, _yoast_wpseo_metadesc, _yoast_wpseo_focuskw
        # Or RankMath style meta
        
        # Insert/update postmeta
        metas = [
            ('_yoast_wpseo_title', seo_title),
            ('_yoast_wpseo_metadesc', meta_desc),
            ('_yoast_wpseo_focuskw', keywords_base.split('_')[0]),
            ('_yoast_wpseo_keywords', keywords_base),
        ]
        
        for meta_key, meta_value in metas:
            cursor.execute("""
                INSERT INTO wp_postmeta (post_id, meta_key, meta_value) VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE meta_value = VALUES(meta_value)
            """, (post_id, meta_key, meta_value))
        
        conn.commit()
        updated += 1
        
    except Exception as e:
        conn.rollback()
        print("[FAIL] ID:{} - {}".format(post_id, str(e)[:100]), flush=True)
        skipped += 1

conn.close()
print("Done! Updated: {}, Skipped: {}".format(updated, skipped), flush=True)
'''

sftp = ssh.open_sftp()
with sftp.open('/root/scripts/seo_meta.py', 'w') as f:
    f.write(meta_script)
sftp.close()

print("Adding meta descriptions to all posts...", flush=True)
stdin, stdout, stderr = ssh.exec_command("cd /root/scripts && python3 seo_meta.py", timeout=300)
output = stdout.read().decode('utf-8', errors='replace').strip()
print(output, flush=True)

err = stderr.read().decode('utf-8', errors='replace').strip()
if err and 'error' in err.lower():
    print("ERR:", err[:300], flush=True)

ssh.close()
