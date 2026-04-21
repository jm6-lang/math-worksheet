import paramiko
from datetime import datetime

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# 资源列表 - 影视娱乐分类
resources = [
    {
        'title': 'U盘车载专用音乐3068首【24GB】',
        'desc': '精选3068首车载音乐，24GB大容量，涵盖流行、摇滚、抒情等多种风格，U盘直接插车即可播放。',
        'link': 'https://pan.quark.cn/s/b3bf3381be57',
        'cat': 86
    },
    {
        'title': '欧美节奏控音乐精选【100首】',
        'desc': '100首超燃欧美节奏音乐，电音、流行、摇滚一网打尽，让你嗨到停不下来。',
        'link': 'https://pan.quark.cn/s/d24a3fb36173',
        'cat': 86
    },
    {
        'title': '低音炮车载音乐精选【360首】',
        'desc': '360首低音炮车载音乐，重低音效果拉满，车载音响必备，开车必备神器。',
        'link': 'https://pan.quark.cn/s/e63b50e9015a',
        'cat': 86
    },
    {
        'title': '网易云评论超10万的情感歌曲合集',
        'desc': '精选网易云音乐评论超10万的感人歌曲，每首都是一个故事，治愈你的每一个夜晚。',
        'link': 'https://pan.quark.cn/s/eabd1416b3ed',
        'cat': 86
    },
    {
        'title': '夜店劲爆慢摇舞曲串烧+粤语热歌榜【300首】',
        'desc': '中英文串烧+精选粤语热歌300首，夜店风、慢摇风应有尽有，转存即听。',
        'link': 'https://pan.quark.cn/s/aeb4c9bd7292',
        'cat': 86
    },
    {
        'title': '抖音快手热歌榜精选【750首】',
        'desc': '抖音快手热门歌曲750首，紧跟潮流热点，转存即听，随时掌握流行风向。',
        'link': 'https://pan.quark.cn/s/af4527f7974d',
        'cat': 86
    },
    {
        'title': '读书学习专用背景音乐合集',
        'desc': '精选轻音乐、钢琴曲、自然白噪音，打造沉浸式学习环境，提升专注力。',
        'link': 'https://pan.quark.cn/s/ef0a2faac6f8',
        'cat': 86
    },
    {
        'title': '车载音乐U盘无损格式合集',
        'desc': '高品质无损音乐合集，发烧级音质，车载音响完美适配，享受极致听觉体验。',
        'link': 'https://pan.quark.cn/s/c5d2aaf7e516',
        'cat': 86
    },
    {
        'title': '发烧人声音乐歌曲精选【340首】',
        'desc': '340首发烧级人声音乐，嗓音质感拉满，适合音响发烧友和音乐爱好者。',
        'link': 'https://pan.quark.cn/s/7ac17fc10fca',
        'cat': 86
    },
    {
        'title': 'MTV精选1万首【自带卡拉OK音轨】',
        'desc': '10000首MTV精选，自带卡拉OK音轨，在家就能K歌，聚会必备神器。',
        'link': 'https://pan.quark.cn/s/c6e9eac10d79',
        'cat': 86
    },
    {
        'title': '国语经典成名曲精选【100首】',
        'desc': '100首国语经典成名曲，回忆满满，转存即听，重温华语乐坛黄金年代。',
        'link': 'https://pan.quark.cn/s/21c3cc764f9b',
        'cat': 86
    },
    {
        'title': '经典香港乐坛70-80-90年代歌曲合集',
        'desc': '香港乐坛黄金时代经典歌曲，70/80/90年代金曲全覆盖，重温港乐辉煌岁月。',
        'link': 'https://pan.quark.cn/s/a7049a5ccf84',
        'cat': 86
    },
    {
        'title': '英文流行歌曲精选【150首】',
        'desc': '150首欧美流行金曲，涵盖经典与热门，英语学习与音乐欣赏两不误。',
        'link': 'https://pan.quark.cn/s/85a951dc657b',
        'cat': 86
    },
    {
        'title': '李健专辑全集【11CD】',
        'desc': '音乐诗人李健全套专辑11CD，清澈嗓音治愈心灵，适合静静聆听的时光。',
        'link': 'https://pan.quark.cn/s/8c714df70baf',
        'cat': 86
    },
    {
        'title': '刀郎《罗刹海市》+辉煌十年绝版珍藏【无损3CD】',
        'desc': '刀郎新歌《罗刹海市》+辉煌十年绝版珍藏专辑，无损音质3CD，经典永流传。',
        'link': 'https://pan.quark.cn/s/dd76e37fd8bc',
        'cat': 86
    },
    {
        'title': '精选千首音乐合集【中日韩英全覆盖】',
        'desc': '1000首精选音乐，涵盖中文、日文、韩文、英文歌曲，车载、夜店、抒情全风格。',
        'link': 'https://pan.quark.cn/s/16a51bd663f3',
        'cat': 86
    }
]

def generate_content(title, desc, link):
    return f'''<p><strong>{desc}</strong></p>

<h3>📦 资源内容包括：</h3>
<ul>
<li>高品质音乐文件</li>
<li>多格式支持（MP3/FLAC等）</li>
<li>转存即听，方便快捷</li>
</ul>

<h3>👥 适合谁：</h3>
<ul>
<li>音乐爱好者</li>
<li>车载音乐需求者</li>
<li>想收藏经典歌曲的朋友</li>
</ul>

<h3>📥 下载链接：</h3>
<p><strong>夸克网盘：</strong> <a href="{link}">{link}</a></p>
<blockquote><p>💡 提示：复制链接打开夸克APP即可保存</p></blockquote>

<style>
.comments-area, #comments, .comment-respond {{ display: none !important; }}
</style>'''

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
success_count = 0

for i, res in enumerate(resources):
    print(f"[{i+1}/{len(resources)}] Publishing: {res['title'][:30]}...")
    
    title = res['title'].replace("'", "''")
    content = generate_content(res['title'], res['desc'], res['link'])
    content_escaped = content.replace("\\", "\\\\").replace("'", "''")
    post_name = f"music-{i+1}-{datetime.now().strftime('%Y%m%d')}"
    
    sql1 = f"""INSERT INTO wp_posts (
        post_author, post_date, post_date_gmt, post_content, post_title,
        post_excerpt, post_status, comment_status, ping_status,
        post_password, post_name, to_ping, pinged, post_modified,
        post_modified_gmt, post_content_filtered, post_parent, guid,
        menu_order, post_type, post_mime_type, comment_count
    ) VALUES (
        1, '{now}', '{now}', '{content_escaped}', '{title}',
        '', 'publish', 'open', 'open',
        '', '{post_name}', '', '', '{now}',
        '{now}', '', 0, '',
        0, 'post', '', 0
    );"""
    
    cmd1 = f"mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"{sql1}\""
    stdin, stdout, stderr = ssh.exec_command(cmd1)
    err = stderr.read().decode()
    
    if err and 'error' in err.lower():
        print(f"  Failed: {err[:100]}")
        continue
    
    cmd2 = "mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"SELECT MAX(ID) FROM wp_posts WHERE post_type='post';\""
    stdin, stdout, stderr = ssh.exec_command(cmd2)
    result = stdout.read().decode()
    post_id = result.strip().split('\n')[-1]
    
    sql3 = f"INSERT INTO wp_term_relationships (object_id, term_taxonomy_id, term_order) VALUES ({post_id}, {res['cat']}, 0);"
    cmd3 = f"mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"{sql3}\""
    ssh.exec_command(cmd3)
    
    sql4 = f"UPDATE wp_term_taxonomy SET count = count + 1 WHERE term_id = {res['cat']};"
    cmd4 = f"mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"{sql4}\""
    ssh.exec_command(cmd4)
    
    print(f"  Success! ID: {post_id}")
    success_count += 1

ssh.close()

print(f"\n{'='*50}")
print(f"Done! Published {success_count}/{len(resources)} articles.")
