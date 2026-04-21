import paramiko
from datetime import datetime
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

CAT_MOVIE = 86   # 影视娱乐
CAT_ONLINE = 88  # 影视在线

css_hide = "<style>.comments-area,#comments,.comment-respond{display:none!important;}</style>"

def generate_content(title, desc, link):
    body = f"<p><strong>{desc}</strong></p><h3>资源内容包括：</h3><ul><li>高清视频资源</li><li>完整版/未删减版</li><li>多格式/多清晰度</li></ul><h3>下载链接：</h3><p><strong>夸克网盘：</strong> <a href=\"{link}\">{link}</a></p><blockquote><p>提示：复制链接打开夸克APP即可保存</p></blockquote>"
    return body + css_hide

resources = [
    {'title': '高分R剧合集', 'desc': '精选高分限制级剧集合集，品质之选，影迷必收。', 'link': 'https://pan.quark.cn/s/50d8a466cff8', 'cat': CAT_MOVIE},
    {'title': '无耻之徒1-11季【高清未删减版】', 'desc': '经典美剧无耻之徒全11季，高清未删减完整版。', 'link': 'https://pan.quark.cn/s/49ffb153d7ed', 'cat': CAT_MOVIE},
    {'title': '世界十大超高分丧尸电影', 'desc': '全球评分最高的十大丧尸题材电影，丧尸片迷必看。', 'link': 'https://pan.quark.cn/s/fee99c1cf8d5', 'cat': CAT_MOVIE},
    {'title': '韩国最出色的十一部R限制【39.7GB】', 'desc': '韩国影坛11部顶级限制级电影，精挑细选。', 'link': 'https://pan.quark.cn/s/bdcc69393882', 'cat': CAT_MOVIE},
    {'title': '儿童动画片合集', 'desc': '精选儿童动画大片合集，陪伴孩子快乐成长。', 'link': 'https://pan.quark.cn/s/73ce18d63ad1', 'cat': CAT_MOVIE},
    {'title': '25年短剧合集', 'desc': '2025年热门短剧合集，追剧必备。', 'link': 'https://pan.quark.cn/s/ba980fa4111f', 'cat': CAT_ONLINE},
    {'title': '评分最高的恐怖片合集', 'desc': '全球评分最高的恐怖片精选，胆小勿入。', 'link': 'https://pan.quark.cn/s/d9e7970df78c', 'cat': CAT_MOVIE},
    {'title': '这辈子必看的灾难电影大片', 'desc': '影史经典灾难片合集，震撼视觉体验。', 'link': 'https://pan.quark.cn/s/bd4befba8051', 'cat': CAT_MOVIE},
    {'title': '韩剧合集', 'desc': '精选热门韩剧合集，韩剧迷不容错过。', 'link': 'https://pan.quark.cn/s/96401fd08a3d', 'cat': CAT_MOVIE},
    {'title': '七部经典大尺度影视剧合集【超清】', 'desc': '七部经典大尺度影视作品，超清画质。', 'link': 'https://pan.quark.cn/s/5171fb2f66a2', 'cat': CAT_MOVIE},
    {'title': '影视合集更新6月', 'desc': '6月最新影视资源合集，持续更新中。', 'link': 'https://pan.quark.cn/s/5f8d038e64e9', 'cat': CAT_ONLINE},
    {'title': '影视合集更新5月', 'desc': '5月影视资源合集，热门影视剧全覆盖。', 'link': 'https://pan.quark.cn/s/e43dca5a0a99', 'cat': CAT_ONLINE},
    {'title': '全球记录片合集', 'desc': '全球精选纪录片合集，开阔视野了解世界。', 'link': 'https://pan.quark.cn/s/1ff111c917c2', 'cat': CAT_MOVIE},
    {'title': '全网最全恐怖片合集【1.7TB】', 'desc': '1.7TB恐怖片大全，恐怖片爱好者终极收藏。', 'link': 'https://pan.quark.cn/s/c3c77ed22f43', 'cat': CAT_MOVIE},
    {'title': '人人影视全站电影合集【600部1TB珍藏版】', 'desc': '人人影视精选600部电影，1TB珍藏版，影迷宝库。', 'link': 'https://pan.quark.cn/s/b5eb2f729110', 'cat': CAT_MOVIE},
    {'title': '豆瓣电影Top250【723GB】', 'desc': '豆瓣评分Top250电影合集，723GB高清珍藏版。', 'link': 'https://pan.quark.cn/s/bd494ceae934', 'cat': CAT_MOVIE},
    {'title': '19禁电影合集', 'desc': '精选19禁级别电影合集，成人向内容。', 'link': 'https://pan.quark.cn/s/d05533554d40', 'cat': CAT_MOVIE},
    {'title': '欧美大尺度电影60部', 'desc': '60部欧美经典大尺度电影合集。', 'link': 'https://pan.quark.cn/s/11b2dee2f3ec', 'cat': CAT_MOVIE},
    {'title': '025吃瓜合集（2024年）', 'desc': '2024年热门吃瓜事件合集，懂的都懂。', 'link': 'https://pan.quark.cn/s/d18fd592cb83', 'cat': CAT_MOVIE},
    {'title': '美女集中营3（羞涩短剧电影）', 'desc': '美女主题短剧电影合集，精彩不容错过。', 'link': 'https://pan.quark.cn/s/bc1c588b4a71', 'cat': CAT_MOVIE},
    {'title': '各平台汽车直播走光视频合集', 'desc': '各平台汽车直播精彩瞬间合集。', 'link': 'https://pan.quark.cn/s/646d4600c928', 'cat': CAT_MOVIE},
    {'title': '欧美剧限制级合集', 'desc': '欧美限制级剧集精选，品质之选。', 'link': 'https://pan.quark.cn/s/9859c6e37805', 'cat': CAT_MOVIE},
    {'title': '深夜必看韩国电影【40部】', 'desc': '40部深夜必看韩国电影合集，经典收藏。', 'link': 'https://pan.quark.cn/s/8386290d0b82', 'cat': CAT_MOVIE},
    {'title': '女神们的电影合集', 'desc': '女神主演经典电影合集，颜值与演技并存。', 'link': 'https://pan.quark.cn/s/403f548fb740', 'cat': CAT_MOVIE},
    {'title': '世界十大超高分丧尸电影【123GB】', 'desc': '123GB超清丧尸电影合集，十大经典丧尸片。', 'link': 'https://pan.quark.cn/s/bf732d4edf3a', 'cat': CAT_MOVIE},
    {'title': 'R级日剧合集', 'desc': '日本限制级剧集精选合集。', 'link': 'https://pan.quark.cn/s/d7a74a75e8ab', 'cat': CAT_MOVIE},
    {'title': '泰剧合集', 'desc': '精选热门泰剧合集，追泰剧必备。', 'link': 'https://pan.quark.cn/s/0566f6e392e6', 'cat': CAT_MOVIE},
    {'title': '欧美剧合集', 'desc': '热门欧美剧集合集，美剧英剧全覆盖。', 'link': 'https://pan.quark.cn/s/7ad55b2f0d36', 'cat': CAT_MOVIE},
    {'title': '三部限制级惊悚片', 'desc': '三部经典限制级惊悚片，高血压远离。', 'link': 'https://pan.quark.cn/s/671dca4a6b43', 'cat': CAT_MOVIE},
    {'title': '神楽坂真冬合集', 'desc': '神楽坂真冬作品合集，珍藏版。', 'link': 'https://pan.quark.cn/s/28a5d683ad90', 'cat': CAT_MOVIE},
]

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
success_count = 0

for i, res in enumerate(resources):
    print(f"[{i+1}/{len(resources)}] Publishing: {res['title'][:25]}...")
    
    title = res['title'].replace("\\", "\\\\").replace("'", "\\'")
    content = generate_content(res['title'], res['desc'], res['link'])
    content = content.replace("\\", "\\\\").replace("'", "\\'")
    post_name = f"movie-{i+1}-{int(time.time())}"
    
    sql = f"INSERT INTO wp_posts (post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt, post_status, comment_status, ping_status, post_password, post_name, to_ping, pinged, post_modified, post_modified_gmt, post_content_filtered, post_parent, guid, menu_order, post_type, post_mime_type, comment_count) VALUES (1, '{now}', '{now}', '{content}', '{title}', '', 'publish', 'open', 'open', '', '{post_name}', '', '', '{now}', '{now}', '', 0, '', 0, 'post', '', 0);"
    
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/wp_publish.sql', 'w') as f:
        f.write(sql)
    sftp.close()
    
    cmd = "mysql -uwpuser -p'WpPass2024!' wp_skillxm < /tmp/wp_publish.sql 2>&1"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    err = stderr.read().decode().strip()
    
    if err and 'error' in err.lower():
        print(f"  Failed: {err[:100]}")
        continue
    
    cmd2 = "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT MAX(ID) FROM wp_posts WHERE post_type='post';\""
    stdin, stdout, stderr = ssh.exec_command(cmd2)
    post_id = stdout.read().decode().strip()
    
    cat_sql = f"INSERT INTO wp_term_relationships (object_id, term_taxonomy_id, term_order) VALUES ({post_id}, {res['cat']}, 0); UPDATE wp_term_taxonomy SET count = count + 1 WHERE term_id = {res['cat']};"
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/wp_cat.sql', 'w') as f:
        f.write(cat_sql)
    sftp.close()
    ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm < /tmp/wp_cat.sql 2>&1")
    
    print(f"  Success! ID: {post_id}")
    success_count += 1

ssh.close()
print(f"\n{'='*50}")
print(f"Done! Published {success_count}/{len(resources)} articles.")
