
import pymysql, json, re

conn = pymysql.connect(host='localhost', user='wp_user', password='gMshA29CshK5', database='wp_skillxm', charset='utf8mb4')
cursor = conn.cursor()

with open('/www/wwwroot/resource_site/auto_collect/links_batch1.json', 'r', encoding='utf-8') as f:
    entries = json.load(f)

# 获取所有文章的ID和标题
cursor.execute("SELECT ID, post_title FROM wp_posts WHERE post_type='post' AND post_status='publish' AND post_title != 'Hello world!'")
articles = {row[1].strip(): row[0] for row in cursor.fetchall()}

matched = 0
not_matched = []

for entry in entries:
    link_title = entry['title'].strip()
    link_url = entry['url']
    
    # 尝试多种匹配方式
    found_id = None
    
    # 1. 精确匹配
    if link_title in articles:
        found_id = articles[link_title]
    
    # 2. 标题包含匹配
    if not found_id:
        for art_title, art_id in articles.items():
            if link_title in art_title or art_title in link_title:
                found_id = art_id
                break
    
    # 3. 去掉标点后匹配
    if not found_id:
        clean = re.sub(r'[【】「」『』《》【】\[\]()（）\s]', '', link_title)
        for art_title, art_id in articles.items():
            art_clean = re.sub(r'[【】「」『』《》【】\[\]()（）\s]', '', art_title)
            if clean in art_clean or art_clean in clean:
                found_id = art_id
                break
    
    if found_id:
        # 在文章末尾追加网盘链接
        cursor.execute("SELECT post_content FROM wp_posts WHERE ID = %s", (found_id,))
        content = cursor.fetchone()[0]
        
        # 检查是否已有链接
        if link_url not in content:
            link_html = '\n\n<h3>📥 资源下载</h3>\n<p>网盘链接：<a href=\"%s\" target=\"_blank\" rel=\"noopener\">%s</a></p>' % (link_url, link_url)
            new_content = content + link_html
            cursor.execute("UPDATE wp_posts SET post_content = %s WHERE ID = %s", (new_content, found_id))
            conn.commit()
            print("  [OK] ID=%d %s" % (found_id, link_title[:35]))
            matched += 1
        else:
            print("  [SKIP] ID=%d 已有链接" % found_id)
            matched += 1
    else:
        not_matched.append(link_title)

cursor.close()
conn.close()
print("\n匹配成功: %d/%d" % (matched, len(entries)))
if not_matched:
    print("\n未匹配:")
    for t in not_matched:
        print("  - %s" % t[:60])
