import paramiko
from datetime import datetime

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# 分类ID
CAT_HEALTH = 87   # 健康养生
CAT_EDU = 84      # 教育资源
CAT_TOOL = 85     # 工具合集

# 资源列表
resources = [
    # 健康养生
    {'title': '健身房私教内部视频课程', 'desc': '健身房私教内部培训课程，专业教练带你科学健身，从入门到进阶全覆盖。', 'link': 'https://pan.quark.cn/s/fa4f12ba4f7c', 'cat': CAT_HEALTH},
    {'title': '健身新手入门训练经验视频课程【37讲】', 'desc': '37节健身入门课程，零基础也能快速上手，科学训练避免运动损伤。', 'link': 'https://pan.quark.cn/s/cc6f76c8985a', 'cat': CAT_HEALTH},
    {'title': '颈椎保养课｜保重身体要紧', 'desc': '专为久坐办公族设计的颈椎保养课程，缓解颈椎疼痛，预防颈椎病。', 'link': 'https://pan.quark.cn/s/1115387cc15a', 'cat': CAT_HEALTH},
    {'title': '上班族必备的瑜伽减肥训练营【完结】', 'desc': '专为上班族设计的瑜伽减肥课程，每天20分钟，轻松瘦身减压。', 'link': 'https://pan.quark.cn/s/661e745e054b', 'cat': CAT_HEALTH},
    {'title': '八段锦详细视频课程', 'desc': '传统养生功法八段锦详细教学，动作分解+呼吸配合，强身健体必备。', 'link': 'https://pan.quark.cn/s/c603076f2b88', 'cat': CAT_HEALTH},
    
    # 教育资源 - 商业/创业
    {'title': '一人公司：失业潮中的高新技术工作者', 'desc': '万相出品，教你如何以一人之力打造高收入技术工作室，实现财务自由。', 'link': 'https://pan.quark.cn/s/6c9ce3c3c605', 'cat': CAT_EDU},
    {'title': '27种盈利模式课程合集', 'desc': '系统学习27种商业模式，找到适合自己的赚钱路径，商业思维必修课。', 'link': 'https://pan.quark.cn/s/3c56ea959744', 'cat': CAT_EDU},
    {'title': '年赚百万的知识付费网站搭建超详细教程', 'desc': '手把手教你搭建知识付费网站，从零到百万营收的完整路径。', 'link': 'https://pan.quark.cn/s/e2ae374d9a34', 'cat': CAT_EDU},
    {'title': '66个赚钱技巧合集', 'desc': '66个实用赚钱技巧，涵盖副业、投资、理财等多领域，总有一个适合你。', 'link': 'https://pan.quark.cn/s/db28c0dec87b', 'cat': CAT_EDU},
    {'title': '副业起跑营第2期｜挑一门好副业三周干起来', 'desc': '系统副业课程，帮你找到适合的副业方向，三周时间快速启动变现。', 'link': 'https://pan.quark.cn/s/c5bc2b28e963', 'cat': CAT_EDU},
    {'title': '小白创业指南老板商业必修课', 'desc': '创业小白必看，从商业思维到实操落地，系统学习创业核心技能。', 'link': 'https://pan.quark.cn/s/1fe9318ee7ef', 'cat': CAT_EDU},
    {'title': '未来三十年我们该如何积累自己的财富', 'desc': '深度分析未来财富趋势，教你做好长期财富规划，抓住时代红利。', 'link': 'https://pan.quark.cn/s/5a09445a02e5', 'cat': CAT_EDU},
    {'title': '写在天下剧变爆发前你还来得及准备的事儿', 'desc': '付费文章精华，洞察时代变革，提前做好准备，从容应对未来。', 'link': 'https://pan.quark.cn/s/966b96b09b6b', 'cat': CAT_EDU},
    
    # 教育资源 - 技能提升
    {'title': '零基础趣学Linux', 'desc': 'Linux入门教程，轻松有趣的方式学习Linux，小白也能快速上手。', 'link': 'https://pan.quark.cn/s/d05b550f64cd', 'cat': CAT_EDU},
    {'title': '八节课帮你攻克社交障碍', 'desc': '社交恐惧症克星，8节课帮你建立自信，轻松应对各种社交场合。', 'link': 'https://pan.quark.cn/s/03e566da8c8a', 'cat': CAT_EDU},
    {'title': '高情商沟通技巧视频课程', 'desc': '提升情商的沟通技巧课程，学会说话的艺术，职场人际关系双赢。', 'link': 'https://pan.quark.cn/s/8f5fa4334622', 'cat': CAT_EDU},
    {'title': '学习有说服力的工作汇报课程', 'desc': '职场必备技能，学会做有说服力的工作汇报，升职加薪利器。', 'link': 'https://pan.quark.cn/s/b6e2dfc3a371', 'cat': CAT_EDU},
    {'title': '普通人的精致生活修炼手册技能宝典', 'desc': '电子书合集，教你从生活细节入手，提升生活品质，活出精致人生。', 'link': 'https://pan.quark.cn/s/6716561e194d', 'cat': CAT_EDU},
    {'title': '女性必备的20堂情趣指南课【完结】', 'desc': '女性专属课程，提升生活情趣，学会爱自己，活出精彩人生。', 'link': 'https://pan.quark.cn/s/c48e0855d272', 'cat': CAT_EDU},
    {'title': '心理控制术', 'desc': '心理学经典课程，学会控制自己的心理状态，提升自我认知和情绪管理能力。', 'link': 'https://pan.quark.cn/s/c7edd747378f', 'cat': CAT_EDU},
    {'title': '12堂视频课程教你最全脱单穿搭技巧', 'desc': '形象改造必修课，12节课教你穿搭技巧，提升魅力，轻松脱单。', 'link': 'https://pan.quark.cn/s/46f9e0c6b08e', 'cat': CAT_EDU},
    
    # 教育资源 - 旅游
    {'title': '国内34省近300个城市景区旅游攻略', 'desc': '全国34省近300个城市旅游攻略，吃喝玩乐全攻略，旅行必备。', 'link': 'https://pan.quark.cn/s/b7d74f000894', 'cat': CAT_EDU},
    {'title': '全国旅游攻略｜国内穷游自驾游旅行地图', 'desc': '电子版旅游地图+美食指南，穷游自驾游必备，省钱又省心。', 'link': 'https://pan.quark.cn/s/bcca02404735', 'cat': CAT_EDU},
    
    # 工具合集
    {'title': '办公设计教程合集', 'desc': '办公软件+设计工具教程合集，提升工作效率，职场技能必备。', 'link': 'https://pan.quark.cn/s/a324c03e677b', 'cat': CAT_TOOL},
    {'title': '软件插件汇总', 'desc': '各类软件插件合集，涵盖设计、办公、开发等领域，提升工作效率神器。', 'link': 'https://pan.quark.cn/s/819d4b636ab2', 'cat': CAT_TOOL},
    {'title': '168套Android项目源码', 'desc': '168套Android开发项目源码，学习参考、二次开发皆可，开发者必备。', 'link': 'https://pan.quark.cn/s/4b2637204452', 'cat': CAT_TOOL},
    {'title': '188套微信小程序源码', 'desc': '188套微信小程序源码，涵盖电商、工具、社交等多种类型，直接可用。', 'link': 'https://pan.quark.cn/s/122f78a65970', 'cat': CAT_TOOL},
    {'title': '从0开发一款iOS App', 'desc': 'iOS开发完整教程，从零基础到上架App Store，手把手教学。', 'link': 'https://pan.quark.cn/s/13079dee3823', 'cat': CAT_TOOL},
    {'title': '知识星球付费课程精选【130篇】', 'desc': '知识星球精选130篇付费内容，涵盖商业、技术、成长等多领域精华。', 'link': 'https://pan.quark.cn/s/20e197e619a4', 'cat': CAT_EDU},
    {'title': '餐饮人轻松同城引流必学课', 'desc': '餐饮店老板必学，教你同城引流获客，提升门店营业额。', 'link': 'https://pan.quark.cn/s/c560187d512a', 'cat': CAT_EDU},
    {'title': '108套别墅新农村自建房图纸', 'desc': '108套自建房设计图纸，别墅/农村自建房全覆盖，建房必备参考。', 'link': 'https://pan.quark.cn/s/7ced192117e0', 'cat': CAT_EDU},
    {'title': '离婚合同离婚协议书模板', 'desc': '专业离婚协议书模板，涵盖各种情况，法律参考必备。', 'link': 'https://pan.quark.cn/s/00cd9458778d', 'cat': CAT_EDU},
    {'title': '性感黑丝图片合集', 'desc': '精选性感黑丝图片合集，高清美图收藏。', 'link': 'https://pan.quark.cn/s/41b4f3e6f9e9', 'cat': 86},  # 影视娱乐
]

def generate_content(title, desc, link):
    return f'''<p><strong>{desc}</strong></p>

<h3>📦 资源内容包括：</h3>
<ul>
<li>完整视频/文档教程</li>
<li>配套学习资料</li>
<li>实操案例分享</li>
</ul>

<h3>👥 适合谁：</h3>
<ul>
<li>想提升相关技能的学习者</li>
<li>需要实操指导的实践者</li>
<li>想系统学习的爱好者</li>
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
    post_name = f"resource-{i+1}-{datetime.now().strftime('%Y%m%d')}"
    
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
