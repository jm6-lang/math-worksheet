import paramiko, sys, re, json
sys.stdout.reconfigure(encoding='utf-8')

# 解析用户发来的链接数据
raw = """
「🤖人工智能AIGC专题资源汇总」链接：https://pan.quark.cn/s/1091f03c9413
「人人必修的AI启蒙课，启蒙课程，不含工具】」链接：https://pan.quark.cn/s/8ed9effac7cc
「Midjourney入门到精通 AI绘图作画教学」链接：链接：https://pan.quark.cn/s/293192759124
「百度·文心一言AI·运营变现」链接：https://pan.quark.cn/s/92b230f749d9
「AI课程合集+行业报告专区【134GB】」链接：https://pan.quark.cn/s/07684d08490f
「【AI绘画软件】NovelAI最终版 webui版 无需额外下载安装！（汉化+可更新+已训练）」 链接：https://pan.quark.cn/s/370e486d444d
「野菩萨AI绘画资深课，全新课程，全新视野，知识重构，引领未来」 链接：https://pan.quark.cn/s/74d832834ae1
「玩赚ChatGPT课程」链接：https://pan.quark.cn/s/6353e53bd8ed
「ChatGPT运营秘诀与变现攻略（100节课）」链接：https://pan.quark.cn/s/9a94e6adb0dd
「ChatGPT大师班 从入门到精通」链接：https://pan.quark.cn/s/ca850d6b809f
「北京大学Deepseek教程资料最新版」，链接：https://pan.quark.cn/s/2cc410fcc3cb
「DeepSeek使用技巧大全」链接：https://pan.quark.cn/s/f9161bd8c994
「《AI智能写作+爆款公式》2025头条爆文速成 轻松抢占流量红利」， 链接：https://pan.quark.cn/s/82da18415e11
「老照片转视频实战营，一线玩家教你 AI 老照片转视频」链接：https://pan.quark.cn/s/56bbd08ec77a
「 最新蓝海赛道，AI素描育儿项目，一发即火，多渠道发布，日入1000 」 链接：https://pan.quark.cn/s/5b88655d0b1c
「AI+自媒体+RPA自动化变现训练营：写作、SEO、全平台运营一站式实战课」 链接：https://pan.quark.cn/s/35f835cf9cf6
「AI生成古代英雄故事，撸视频号分成计划，可稳定多号操作」 链接：https://pan.quark.cn/s/345b77c5eacd
「U盘车载专用音乐 3068 首 24G」链接：https://pan.quark.cn/s/b3bf3381be57
「欧美节奏控音乐(100首)」链接：https://pan.quark.cn/s/d24a3fb36173
「低音炮车载360首」链接：https://pan.quark.cn/s/e63b50e9015a
「网易云评论超10万的歌曲」链接：https://pan.quark.cn/s/eabd1416b3ed
「[夜店劲爆慢摇舞曲中英文串烧+精选粤语热歌榜300首][转存即听] 链接：https://pan.quark.cn/s/aeb4c9bd7292
「抖音快手热歌榜750首」转存就可听，链接：https://pan.quark.cn/s/af4527f7974d
「读书学习听的音乐合集」，链接：https://pan.quark.cn/s/ef0a2faac6f8
「车载音乐U盘无损格式」。链接：https://pan.quark.cn/s/c5d2aaf7e516
「发烧人声音乐歌曲(340首)」链接：https://pan.quark.cn/s/7ac17fc10fca
「MTV精选1万首（自带卡拉ok音轨，可以自己在家唱歌）」链接：https://pan.quark.cn/s/c6e9eac10d79
「国语经典成名曲(100首)，转存即听」链接：https://pan.quark.cn/s/21c3cc764f9b
「经典香港乐坛70-80-90歌曲」链接：https://pan.quark.cn/s/a7049a5ccf84
「英文流行歌曲(150首)」链接：https://pan.quark.cn/s/85a951dc657b
「〖李健11CD〗」链接：https://pan.quark.cn/s/8c714df70baf
「【刀郎】新歌《罗刹海市》+《辉煌十年绝版珍藏》无损3CD」链接：https://pan.quark.cn/s/dd76e37fd8bc
「精选千首音乐（中日韩英车载夜店都有）」链接：https://pan.quark.cn/s/16a51bd663f3
「健身房私教内部视频课程」链接：https://pan.quark.cn/s/fa4f12ba4f7c
「健身新手入门训练经验视频课程（37讲）」链接：https://pan.quark.cn/s/cc6f76c8985a
「一人公司：失业潮中的高新技术工作者（万相）」链接：https://pan.quark.cn/s/6c9ce3c3c605
「27种盈利模式课程合集」链接：https://pan.quark.cn/s/3c56ea959744
「年赚百万的知识付费网站搭建 超详细教程」链接：https://pan.quark.cn/s/e2ae374d9a34
「《颈椎保养课 保重身体要紧》视频课程 坐办公室 看电脑多的必备身体调节[mp4]」 链接：https://pan.quark.cn/s/1115387cc15a
「女性必备的20堂情趣指南课（完结）」链接：https://pan.quark.cn/s/c48e0855d272
「【心理控制术】 」链接：https://pan.quark.cn/s/c7edd747378f
「66个赚钱技巧」链接：https://pan.quark.cn/s/db28c0dec87b
「零基础趣学Linux」链接：https://pan.quark.cn/s/d05b550f64cd
「八节课帮你攻克社交障碍」链接：https://pan.quark.cn/s/03e566da8c8a
「高情商沟通技巧视频课程」链接：https://pan.quark.cn/s/8f5fa4334622
「国内34个省的近300个城市景区旅游攻略分享」链接：https://pan.quark.cn/s/b7d74f000894
「全国旅游攻略 国内穷游自驾游旅行地图电子版美食指南」链接：https://pan.quark.cn/s/bcca02404735
「副业起跑营第2期，挑一门好副业，三周干起来」链接：https://pan.quark.cn/s/c5bc2b28e963
「上班族必备的瑜伽减肥训练营【完结】」链接：https://pan.quark.cn/s/661e745e054b
「普通人的精致生活修炼手册技能宝典 电子书籍 合集」链接：https://pan.quark.cn/s/6716561e194d
「学习有说服力的工作汇报课程」链接：https://pan.quark.cn/s/b6e2dfc3a371
「办公设计教程合集」链接：https://pan.quark.cn/s/a324c03e677b
「知识星球 付费课程（精选130篇）」 链接：https://pan.quark.cn/s/20e197e619a4
「小白创业指南老板商业必修课」链接：https://pan.quark.cn/s/1fe9318ee7ef
「某公众号付费文《未来三十年，我们该如何积累自己的财富》」链接：https://pan.quark.cn/s/5a09445a02e5
「某付费文章：写在天下剧变爆发前，你还来得及准备的事儿 」链接：https://pan.quark.cn/s/966b96b09b6b
「从 0 开发一款 iOS App」链接：https://pan.quark.cn/s/13079dee3823
「12堂视频课程，教你最全脱单穿搭技巧」链接：https://pan.quark.cn/s/46f9e0c6b08e
「性感黑丝」链接：https://pan.quark.cn/s/41b4f3e6f9e9
「软件插件汇总」链接：https://pan.quark.cn/s/819d4b636ab2
「餐饮人轻松同城引流必学课」链接：https://pan.quark.cn/s/c560187d512a
「【八段锦详细视频课程】」链接：https://pan.quark.cn/s/c603076f2b88
「168套Android项目源码」链接：https://pan.quark.cn/s/4b2637204452
「188套微信小程序源码」链接：https://pan.quark.cn/s/122f78a65970
「《108套别墅新农村自建房图纸》」链接：https://pan.quark.cn/s/7ced192117e0
「离婚合同离婚协议书模板」链接：https://pan.quark.cn/s/00cd9458778d
"""

# 解析
entries = []
for line in raw.strip().split('\n'):
    line = line.strip()
    if not line:
        continue
    # 提取标题和链接
    m = re.match(r'[「『【]?(.*?)[」』】]?\s*(?:，|。)?\s*(?:链接[：:]?)?\s*(?:链接[：:]?)?\s*(https?://\S+)', line)
    if m:
        title = m.group(1).strip().strip('「」『』【】').strip()
        url = m.group(2).strip()
        # 清理标题中的多余符号
        title = re.sub(r'^[「『【]+|[」』】]+$', '', title).strip()
        entries.append({'title': title, 'url': url})
    else:
        print(f"  未解析: {line[:80]}")

print(f"共解析 {len(entries)} 条链接")
for e in entries[:5]:
    print(f"  {e['title'][:40]} -> {e['url']}")
print(f"  ...")

# 保存到JSON供后续使用
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\links_batch1.json', 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

# 上传到服务器
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)
sftp = ssh.open_sftp()

local = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\links_batch1.json'
remote = '/www/wwwroot/resource_site/auto_collect/links_batch1.json'
sftp.put(local, remote)
sftp.close()

# 在服务器上匹配并更新文章
match_script = '''
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
        clean = re.sub(r'[【】「」『』《》【】\[\]()（）\\s]', '', link_title)
        for art_title, art_id in articles.items():
            art_clean = re.sub(r'[【】「」『』《》【】\[\]()（）\\s]', '', art_title)
            if clean in art_clean or art_clean in clean:
                found_id = art_id
                break
    
    if found_id:
        # 在文章末尾追加网盘链接
        cursor.execute("SELECT post_content FROM wp_posts WHERE ID = %s", (found_id,))
        content = cursor.fetchone()[0]
        
        # 检查是否已有链接
        if link_url not in content:
            link_html = '\\n\\n<h3>📥 资源下载</h3>\\n<p>网盘链接：<a href=\\"%s\\" target=\\"_blank\\" rel=\\"noopener\\">%s</a></p>' % (link_url, link_url)
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
print("\\n匹配成功: %d/%d" % (matched, len(entries)))
if not_matched:
    print("\\n未匹配:")
    for t in not_matched:
        print("  - %s" % t[:60])
'''

local_script = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\match_links.py'
with open(local_script, 'w', encoding='utf-8') as f:
    f.write(match_script)

sftp = ssh.open_sftp()
sftp.put(local_script, '/www/wwwroot/resource_site/auto_collect/match_links.py')
sftp.close()

stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site && python3 auto_collect/match_links.py 2>&1", timeout=30)
print("\n=== 匹配结果 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
