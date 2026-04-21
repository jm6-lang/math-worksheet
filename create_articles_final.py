#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量创建未匹配的文章"""
import paramiko, json, sys
sys.stdout.reconfigure(encoding='utf-8')

# 所有未匹配的资源
all_unmatched = [
    {"title": "剪映预设专场+蒙版+调色合集", "url": "https://pan.xunlei.com/s/VOOaMF1xtx2hjdy5BesUfrv4A1", "code": "9hv2", "source": "迅雷网盘"},
    {"title": "李银河这才是你想要的性", "url": "https://pan.xunlei.com/s/VOQ6Kt9-LVQRsktvQtBSUTdjA1", "code": "rn95", "source": "迅雷网盘"},
    {"title": "微信机器人工具+视频教程", "url": "https://pan.xunlei.com/s/VOQBYMouy5qFuBJcHF8Opc-yA1", "code": "wch8", "source": "迅雷网盘"},
    {"title": "书法教程教你零基础写出一手漂亮好字完结", "url": "https://pan.xunlei.com/s/VOQB_XeOc5OUVTauZez_fwDUA1", "code": "77ez", "source": "迅雷网盘"},
    {"title": "U盘重装系统到电脑系统维护维修视频", "url": "https://pan.xunlei.com/s/VOYJVgSoUAhvX4E4C5QPoo0wA1", "code": "7khq", "source": "迅雷网盘"},
    {"title": "富爸爸系列全集纪念新版共32册", "url": "https://pan.xunlei.com/s/VOP3rnoD-wEAtCmsdBlggRXRA1", "code": "4m5x", "source": "迅雷网盘"},
    {"title": "富爸爸点石成金套装共五册", "url": "https://pan.xunlei.com/s/VOQ6KI9A7MK-8MadlJlaxMUgA1", "code": "re3g", "source": "迅雷网盘"},
    {"title": "解锁版软件合集每日更新", "url": "https://pan.xunlei.com/s/VOOaMJ54DvaNOzRoOLlxR5o2A1", "code": "a6ub", "source": "迅雷网盘"},
    {"title": "夸克网盘批量转存分享工具", "url": "https://pan.xunlei.com/s/VOQ6LIBchwbqjdXwYUw4zaeBA1", "code": "n8hd", "source": "迅雷网盘"},
    {"title": "国外最火应用App合集", "url": "https://pan.xunlei.com/s/VOVVM2TMrCI1e6xO09VDc1JuA1", "code": "m4eu", "source": "迅雷网盘"},
    {"title": "AI写作鱼手机号登录终身VIP", "url": "https://pan.xunlei.com/s/VOVun5tFShvSW39OHUi_mDjQA1", "code": "vaxg", "source": "迅雷网盘"},
    {"title": "3D动态照片v4.0.0.6解锁版", "url": "https://pan.xunlei.com/s/VOVz9TwDFoIhJcrKIoZuY1vHA1", "code": "s489", "source": "迅雷网盘"},
    {"title": "Zapya快牙v6.5.5解锁版", "url": "https://pan.xunlei.com/s/VOWIs-iGNCOKKEYQ-SO7zRKZA1", "code": "j5d3", "source": "迅雷网盘"},
    {"title": "作业帮v13.61.0解锁绿化版", "url": "https://pan.xunlei.com/s/VOWOBNPwn0pAejN8kN4ulJJ9A1", "code": "vgq4", "source": "迅雷网盘"},
    {"title": "酷我音乐6.0.1.0车机解锁版", "url": "https://pan.xunlei.com/s/VOWYC39PkmCwNNOZD-ixu68QA1", "code": "8nbv", "source": "迅雷网盘"},
    {"title": "Youtube油管视频下载器", "url": "https://pan.xunlei.com/s/VOWYEH0EkmCwNNOZD-ixvJFYA1", "code": "jjj2", "source": "迅雷网盘"},
    {"title": "查企业查信息送5年SVIP", "url": "https://pan.xunlei.com/s/VOY--vv8UsLDxjyOGMSyLOd5A1", "code": "48gy", "source": "迅雷网盘"},
    {"title": "TVBOX最新接口合集", "url": "https://pan.xunlei.com/s/VOYdALqV30NTW53quTQfWHhmA1", "code": "beb8", "source": "迅雷网盘"},
    {"title": "AI唱歌软件AI翻唱克隆声音", "url": "https://pan.xunlei.com/s/VOYiL6cH2GCVrbv91FRy7uEZA1", "code": "whn8", "source": "迅雷网盘"},
    {"title": "6天掌握MySQL基础视频教程", "url": "https://drive.uc.cn/s/4d9b7c9b416a4", "code": "", "source": "UC网盘"},
    {"title": "Web前端全栈HTML5大神之路", "url": "https://drive.uc.cn/s/2f1e49b28a674", "code": "", "source": "UC网盘"},
    {"title": "全套高清Photoshop收费教程", "url": "https://drive.uc.cn/s/144eaaa307314", "code": "", "source": "UC网盘"},
    {"title": "AI软件系统教程矢量魔法", "url": "https://drive.uc.cn/s/1500f5a08f744", "code": "", "source": "UC网盘"},
    {"title": "电商合成案例教程", "url": "https://drive.uc.cn/s/5458d031f4cc4", "code": "", "source": "UC网盘"},
    {"title": "Python全套教程", "url": "https://drive.uc.cn/s/786079f453dc4", "code": "", "source": "UC网盘"},
    {"title": "下半年瑞思拜四六级讲义", "url": "https://drive.uc.cn/s/b58cb4261b5e4", "code": "", "source": "UC网盘"},
    {"title": "小程序开发教程从零到精通", "url": "https://drive.uc.cn/s/5e7c7ed278b04", "code": "", "source": "UC网盘"},
    {"title": "抖音电商最新玩法完结", "url": "https://drive.uc.cn/s/c553800a1e144", "code": "", "source": "UC网盘"},
    {"title": "宅男深夜小确幸合集", "url": "https://drive.uc.cn/s/23b8b1f486fd4", "code": "", "source": "UC网盘"},
    {"title": "高颜值小姐姐视频素材合集", "url": "https://drive.uc.cn/s/91239ba5aff14", "code": "", "source": "UC网盘"},
    {"title": "精品韩国电影合集", "url": "https://drive.uc.cn/s/c898b296d06d4", "code": "", "source": "UC网盘"},
    {"title": "首尔之春蓝光原盘REMUX", "url": "https://drive.uc.cn/s/089d02ae8ef04", "code": "", "source": "UC网盘"},
    {"title": "同人漫画合集", "url": "https://drive.uc.cn/s/740f6eb0c39a4", "code": "", "source": "UC网盘"},
    {"title": "AI老照片修复懒人包", "url": "https://pan.baidu.com/s/1OKRcT07QHKdxeCMzlmxCng", "code": "y15h", "source": "百度网盘"},
    {"title": "AI智能去水印FliFlik", "url": "https://pan.baidu.com/s/1K6rDuhewZwOMGKVFIQctBg", "code": "1c3d", "source": "百度网盘"},
    {"title": "开源AI批量抠图工具rembg", "url": "https://pan.baidu.com/s/1Kk3YqKHxfx5RVZ8eXUZDmw", "code": "yt5o", "source": "百度网盘"},
    {"title": "小智AI详细教程WIFI版", "url": "https://pan.baidu.com/s/1KWwllYZmMJaXsYFoSWKtpQ", "code": "qwjs", "source": "百度网盘"},
    {"title": "Topaz Video Enhance AI视频增强", "url": "https://pan.baidu.com/s/1zJQT_pA1M_xmHsXF8hYENQ", "code": "wn6u", "source": "百度网盘"},
    {"title": "Luminar Neo AI人工智能修图", "url": "https://pan.baidu.com/s/1U7DiqY22VaqudcuhGT0EcQ", "code": "rbeh", "source": "百度网盘"},
    {"title": "Radiant Photo AI智能修图插件", "url": "https://pan.baidu.com/s/1Ua8GEAzM6sH_Vg4ilv2l4g", "code": "dtvi", "source": "百度网盘"},
    {"title": "视频号AI美女6.0玩法教程", "url": "https://pan.baidu.com/s/1BoalugDLmEa1EDhaqkvpZA", "code": "1234", "source": "百度网盘"},
    {"title": "DeepSeek实战手册120集", "url": "https://pan.baidu.com/s/1uPlNW-PweWfOFplQCfzg1Q", "code": "1234", "source": "百度网盘"},
    {"title": "DeepSeek变现小红书引流私域", "url": "https://pan.baidu.com/s/1mc_cPDVtnHeM5AqbCWfo4g", "code": "1234", "source": "百度网盘"},
    {"title": "DeepSeek公众号流量主日入四位数", "url": "https://pan.baidu.com/s/1b_wtxHwY6DgUfE3fSg70SA", "code": "1234", "source": "百度网盘"},
    {"title": "DeepSeek今日头条爆款文章", "url": "https://pan.baidu.com/s/1OyMTW2fOwzysbfQeZfOYHQ", "code": "1234", "source": "百度网盘"},
    {"title": "变频空调维修技术资料教程", "url": "https://pan.baidu.com/s/13fn_zLJgSkcV6phBeZA9Dg", "code": "1234", "source": "百度网盘"},
    {"title": "AI扣子Coze自动化工作流教程", "url": "https://pan.baidu.com/s/1K6auy23mhGe8Ab2J8St7ag", "code": "1234", "source": "百度网盘"},
    {"title": "爆款电影解说教程", "url": "https://pan.baidu.com/s/1edQS5ssNBN64NwozUzpN8g", "code": "1234", "source": "百度网盘"},
    {"title": "闲鱼Keep代跑冷门项目", "url": "https://pan.baidu.com/s/1nm32PbjqybgSh-fEb4Mguw", "code": "1234", "source": "百度网盘"},
    {"title": "AI图文带货实操课", "url": "https://pan.baidu.com/s/1vtmiXvBWCq9B37ckyZApUg", "code": "1234", "source": "百度网盘"},
    {"title": "电影窒恋4K高清", "url": "https://pan.baidu.com/s/1w_0I2QynscpT843Et7aQtw", "code": "1234", "source": "百度网盘"},
]

print(f"共 {len(all_unmatched)} 篇文章需要创建")

# 连接服务器
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 直接执行Python代码
cmd = '''python3 << 'ENDSCRIPT'
import pymysql
from datetime import datetime

articles = ''' + json.dumps(all_unmatched, ensure_ascii=False) + '''

conn = pymysql.connect(host='localhost', user='wp_user', password='gMshA29CshK5', database='wp_skillxm', charset='utf8mb4')
cursor = conn.cursor()

cursor.execute("SELECT term_id FROM wp_terms WHERE name='教育资源'")
edu_cat = cursor.fetchone()
edu_cat_id = edu_cat[0] if edu_cat else 1

cursor.execute("SELECT term_id FROM wp_terms WHERE name='工具合集'")
tool_cat = cursor.fetchone()
tool_cat_id = tool_cat[0] if tool_cat else 1

cursor.execute("SELECT term_id FROM wp_terms WHERE name='AI知识'")
ai_cat = cursor.fetchone()
ai_cat_id = ai_cat[0] if ai_cat else 1

cursor.execute("SELECT term_id FROM wp_terms WHERE name='影视娱乐'")
movie_cat = cursor.fetchone()
movie_cat_id = movie_cat[0] if movie_cat else 1

created = 0
for article in articles:
    title = article['title']
    url = article['url']
    code = article.get('code', '')
    source = article.get('source', '网盘')
    
    content = "<h2>" + title + "资源介绍</h2>\\n"
    content += "<p>本资源为<strong>" + title + "</strong>完整版本，内容详实丰富，适合各类用户学习使用。资源经过精心整理，确保内容完整可用。</p>\\n\\n"
    content += "<h3>资源特点</h3>\\n<ul>\\n<li>内容完整，无缺失</li>\\n<li>格式清晰，方便学习</li>\\n<li>实时更新，紧跟最新版本</li>\\n<li>支持多设备使用</li>\\n</ul>\\n\\n"
    content += "<h3>适合人群</h3>\\n<p>本资源适合对相关领域感兴趣的初学者、进阶者以及专业人士使用。</p>\\n\\n"
    content += "<h3>使用说明</h3>\\n<p>下载后请按照说明进行操作，如遇到问题可以留言反馈。</p>\\n\\n"
    content += "<h3>📥 资源下载</h3>\\n<p><strong>网盘类型：</strong>" + source + "</p>\\n"
    content += "<p><strong>网盘链接：</strong><a href=\\\"" + url + "\\\" target=\\\"_blank\\\" rel=\\\"noopener\\\">" + url + "</a></p>"
    if code:
        content += "\\n<p><strong>提取码：</strong>" + code + "</p>"
    
    if any(k in title for k in ['AI', 'ai', 'DeepSeek', '智能', '人工智能']):
        cat_id = ai_cat_id
    elif any(k in title for k in ['教程', '学习', '课程', 'Python', 'Java', 'MySQL', 'Photoshop', 'PS']):
        cat_id = edu_cat_id
    elif any(k in title for k in ['电影', '视频', '4K', '漫画', '小说']):
        cat_id = movie_cat_id
    else:
        cat_id = tool_cat_id
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    post_name = title.lower().replace(' ', '-').replace('/', '-')[:200]
    
    sql = """INSERT INTO wp_posts 
             (post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt, 
              post_status, comment_status, ping_status, post_name, post_modified, post_modified_gmt, post_type) 
             VALUES (1, %s, %s, %s, %s, '', 'publish', 'open', 'open', %s, %s, %s, 'post')"""
    cursor.execute(sql, (now, now, content, title, post_name, now, now))
    post_id = cursor.lastrowid
    cursor.execute("INSERT INTO wp_term_relationships (object_id, term_taxonomy_id) VALUES (%s, %s)", (post_id, cat_id))
    cursor.execute("UPDATE wp_term_taxonomy SET count = count + 1 WHERE term_id = %s", (cat_id,))
    conn.commit()
    print(f"  [OK] ID={post_id} {title[:35]}")
    created += 1

cursor.close()
conn.close()
print(f"\\n成功创建 {created} 篇文章")
ENDSCRIPT'''

stdin, stdout, stderr = ssh.exec_command(cmd, timeout=120)
print("\n=== 创建结果 ===")
print(stdout.read().decode('utf-8', errors='ignore'))
err = stderr.read().decode('utf-8', errors='ignore')
if err:
    print("错误:", err)

ssh.close()
print("\n全部处理完成！")
