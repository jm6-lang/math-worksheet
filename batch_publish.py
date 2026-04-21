import paramiko
from datetime import datetime

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# 资源列表
resources = [
    {
        'title': '人人必修的AI启蒙课｜AI基础认知入门',
        'desc': '适合零基础小白的AI入门课程，从AI概念、原理到应用场景，系统建立AI认知框架，为深入学习打下基础。',
        'link': 'https://pan.quark.cn/s/8ed9effac7cc',
        'cat': 80
    },
    {
        'title': 'Midjourney入门到精通｜AI绘图作画完整教程',
        'desc': '从注册账号到高级提示词技巧，手把手教你用Midjourney生成高质量AI绘画作品，涵盖人像、风景、商业设计等场景。',
        'link': 'https://pan.quark.cn/s/293192759124',
        'cat': 80
    },
    {
        'title': '百度文心一言AI运营变现课程',
        'desc': '国产AI大模型文心一言的运营攻略，教你如何用文心一言做内容创作、自媒体运营，实现AI变现。',
        'link': 'https://pan.quark.cn/s/92b230f749d9',
        'cat': 80
    },
    {
        'title': 'AI课程合集+行业报告专区【134GB】',
        'desc': '超大容量AI学习资源包，包含国内外主流AI工具教程、行业研究报告、学习路线图，一站式AI学习资料库。',
        'link': 'https://pan.quark.cn/s/07684d08490f',
        'cat': 80
    },
    {
        'title': 'NovelAI绘画软件最终版｜WebUI汉化版',
        'desc': 'AI绘画神器NovelAI完整版，无需额外安装，已汉化+可更新+预训练模型，解压即用，轻松生成二次元风格作品。',
        'link': 'https://pan.quark.cn/s/370e486d444d',
        'cat': 80
    },
    {
        'title': '野菩萨AI绘画资深课｜全新视野知识重构',
        'desc': '资深AI绘画玩家进阶课程，全新视角解读AI绘画，知识体系重构，带你突破创作瓶颈，引领AI艺术未来。',
        'link': 'https://pan.quark.cn/s/74d832834ae1',
        'cat': 80
    },
    {
        'title': '玩赚ChatGPT课程｜从入门到变现',
        'desc': 'ChatGPT实战变现课程，教你用ChatGPT做内容创作、自媒体运营、副业赚钱，真正把AI变成生产力。',
        'link': 'https://pan.quark.cn/s/6353e53bd8ed',
        'cat': 80
    },
    {
        'title': 'ChatGPT运营秘诀与变现攻略【100节课】',
        'desc': '100节系统课程，全面覆盖ChatGPT运营技巧，从提示词优化到商业变现，打造你的AI赚钱机器。',
        'link': 'https://pan.quark.cn/s/9a94e6adb0dd',
        'cat': 80
    },
    {
        'title': 'ChatGPT大师班｜从入门到精通',
        'desc': 'ChatGPT系统学习课程，从基础操作到高级应用，覆盖写作、编程、翻译、营销等多场景，快速成为ChatGPT高手。',
        'link': 'https://pan.quark.cn/s/ca850d6b809f',
        'cat': 80
    },
    {
        'title': '北京大学Deepseek教程资料最新版',
        'desc': '北大官方Deepseek教程，系统学习国产AI大模型Deepseek的使用方法和应用技巧，紧跟AI前沿。',
        'link': 'https://pan.quark.cn/s/2cc410fcc3cb',
        'cat': 80
    },
    {
        'title': 'DeepSeek使用技巧大全',
        'desc': 'Deepseek实用技巧合集，覆盖提示词优化、场景应用、效率提升等，助你快速掌握国产AI神器。',
        'link': 'https://pan.quark.cn/s/f9161bd8c994',
        'cat': 80
    },
    {
        'title': 'AI智能写作+爆款公式｜2025头条爆文速成',
        'desc': 'AI写作+爆款公式双剑合璧，轻松抢占头条流量红利，教你用AI写出10W+爆文，实现内容变现。',
        'link': 'https://pan.quark.cn/s/82da18415e11',
        'cat': 80
    },
    {
        'title': '老照片转视频实战营｜AI一键让照片动起来',
        'desc': '一线玩家手把手教你用AI把老照片转成视频，修复+动画+配音一站式实操，让珍贵回忆"活"过来。',
        'link': 'https://pan.quark.cn/s/56bbd08ec77a',
        'cat': 80
    },
    {
        'title': 'AI素描育儿项目｜蓝海赛道一发即火',
        'desc': '最新蓝海赛道，AI素描育儿内容，多平台分发，可多号操作，日入1000+，带你抓住AI内容红利。',
        'link': 'https://pan.quark.cn/s/5b88655d0b1c',
        'cat': 80
    },
    {
        'title': 'AI+自媒体+RPA自动化变现训练营',
        'desc': '写作、SEO、全平台运营一站式实战课，AI+RPA双引擎驱动，实现自媒体自动化变现，解放双手躺赚。',
        'link': 'https://pan.quark.cn/s/35f835cf9cf6',
        'cat': 80
    },
    {
        'title': 'AI生成古代英雄故事｜视频号分成计划',
        'desc': 'AI生成古代英雄故事内容，撸视频号分成计划，可稳定多号操作，轻松实现被动收入。',
        'link': 'https://pan.quark.cn/s/345b77c5eacd',
        'cat': 80
    }
]

def generate_content(title, desc, link):
    return f'''<p><strong>{desc}</strong></p>

<h3>📦 资源内容包括：</h3>
<ul>
<li>完整视频教程</li>
<li>配套学习资料</li>
<li>实操案例分享</li>
</ul>

<h3>👥 适合谁：</h3>
<ul>
<li>想系统学习AI技能的新手</li>
<li>想提升工作效率的打工人</li>
<li>想通过AI变现的自由职业者</li>
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
    post_name = f"ai-course-{i+1}-{datetime.now().strftime('%Y%m%d')}"
    
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
    
    # Get post ID
    cmd2 = "mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"SELECT MAX(ID) FROM wp_posts WHERE post_type='post';\""
    stdin, stdout, stderr = ssh.exec_command(cmd2)
    result = stdout.read().decode()
    post_id = result.strip().split('\n')[-1]
    
    # Set category
    sql3 = f"INSERT INTO wp_term_relationships (object_id, term_taxonomy_id, term_order) VALUES ({post_id}, {res['cat']}, 0);"
    cmd3 = f"mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"{sql3}\""
    ssh.exec_command(cmd3)
    
    # Update category count
    sql4 = f"UPDATE wp_term_taxonomy SET count = count + 1 WHERE term_id = {res['cat']};"
    cmd4 = f"mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"{sql4}\""
    ssh.exec_command(cmd4)
    
    print(f"  Success! ID: {post_id}")
    success_count += 1

ssh.close()

print(f"\n{'='*50}")
print(f"Done! Published {success_count}/{len(resources)} articles.")
