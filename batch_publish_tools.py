import paramiko, sys
from datetime import datetime
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

css = "<style>.comments-area,#comments,.comment-respond{display:none!important;}</style>"

def publish(title, desc, link, cat_id):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    body = "<p><strong>{}</strong></p><h3>软件功能介绍：</h3><p>{}</p><h3>下载链接：</h3><p><strong>夸克网盘：</strong> <a href=\"{}\">{}</a></p><blockquote><p>提示：复制链接打开夸克APP即可保存。资源来自网络，仅供学习交流，禁止商用。</p></blockquote>".format(desc, desc, link, link) + css
    t = title.replace("\\", "\\\\").replace("'", "\\'")
    c = body.replace("\\", "\\\\").replace("'", "\\'")
    pn = "tool-{}-{}".format(int(time.time()), hash(title) % 10000)
    sql = "INSERT INTO wp_posts (post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,comment_status,ping_status,post_password,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered,post_parent,guid,menu_order,post_type,post_mime_type,comment_count) VALUES (1,'{}','{}','{}','{}','','publish','open','open','','{}','','','{}','{}','',0,'',0,'post','',0);".format(now, now, c, t, pn, now, now)
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/wp_p.sql', 'w') as f:
        f.write(sql)
    sftp.close()
    stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm < /tmp/wp_p.sql 2>&1")
    err = stderr.read().decode().strip()
    if err and 'error' in err.lower():
        return None
    stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT MAX(ID) FROM wp_posts WHERE post_type='post';\"")
    pid = stdout.read().decode().strip()
    cat_sql = "INSERT INTO wp_term_relationships (object_id,term_taxonomy_id,term_order) VALUES ({},0,0); UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id={};".format(pid, cat_id)
    # fix: VALUES needs (pid, cat_id, 0)
    cat_sql = "INSERT INTO wp_term_relationships (object_id,term_taxonomy_id,term_order) VALUES ({},{},0); UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id={};".format(pid, cat_id, cat_id)
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/wp_c.sql', 'w') as f:
        f.write(cat_sql)
    sftp.close()
    ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm < /tmp/wp_c.sql 2>&1")
    return pid

resources = [
    ('Reface一键换脸 v4.5.0 AI换脸工具', 'Reface是一款基于AI技术的换脸应用，可以轻松将你的脸替换到视频和GIF中，操作简单效果逼真，支持短视频和表情包制作。', 'https://pan.quark.cn/s/a54960efcf08'),
    ('上班摸鱼老板键软件', '一键隐藏所有窗口的摸鱼神器，老板来了瞬间切换到工作界面，支持自定义快捷键和隐藏应用列表。', 'https://pan.quark.cn/s/19ea6c40d155'),
    ('Listen1全网音乐免费听', '聚合全网音乐平台资源，免费在线收听各大平台歌曲，支持搜索、播放列表、歌词显示等功能。', 'https://pan.quark.cn/s/0f19852eab83'),
    ('Autodesk AutoCAD 2024', 'Autodesk AutoCAD 2024专业版，全球领先的CAD设计软件，支持2D/3D设计、建筑制图、机械设计等。', 'https://pan.quark.cn/s/648e797ff85b'),
    ('酒店防窥检测1.26解锁会员版', '酒店隐藏摄像头检测工具，通过WiFi扫描和红外检测发现隐藏设备，出行住宿必备安全工具。', 'https://pan.quark.cn/s/a55f9d261f02'),
    ('去水印工具', '一键去除图片和视频水印，支持抖音、快手、微博等主流平台，批量处理效率高。', 'https://pan.quark.cn/s/24d6f26bb2d0'),
    ('AI Chat智能对话助手', 'AI智能聊天助手应用，支持多模型对话、文案生成、翻译、知识问答等多种AI功能。', 'https://pan.quark.cn/s/3ebb19f720cc'),
    ('驾考题库大全会员版', '驾照考试全科目题库，包含科目一到科目四全部题目，支持模拟考试、错题本、顺序练习等。', 'https://pan.quark.cn/s/9394c429b093'),
    ('呐噗助眠APP', '专业助眠应用，提供白噪音、自然声音、冥想引导等助眠内容，帮你快速入睡提升睡眠质量。', 'https://pan.quark.cn/s/8e95a99ab039'),
    ('嗅觉浏览器', '轻量级浏览器应用，界面简洁无广告，支持广告拦截、隐私保护、多标签浏览。', 'https://pan.quark.cn/s/e159f31feb5e'),
    ('扫描全能王解锁付费版', '手机扫描仪应用，将手机变成随身扫描仪，支持文档扫描、OCR识别、PDF导出、多页拼接。', 'https://pan.quark.cn/s/9f1a2cb69dcd'),
    ('洛雪音乐附最新可用音源', '洛雪音乐助手PC端，聚合多个音乐源，免费在线试听和下载全网音乐，附带最新可用音源配置。', 'https://pan.quark.cn/s/7d199c18f040'),
    ('尼卡音乐免费听歌软件', '全新推出的免费音乐软件，支持在线收听和下载，界面清爽无广告，海量歌曲资源。', 'https://pan.quark.cn/s/852813bc1eb9'),
    ('车机工具合集', '车载系统工具合集，包含导航、音乐、视频等常用车载应用，适配多种车机系统。', 'https://pan.quark.cn/s/1828d0268644'),
    ('漫漫漫画v5.2.43去广告版', '海量漫画追漫神器，千万级漫画资源库，去广告纯净版体验更佳，支持离线缓存。', 'https://pan.quark.cn/s/2c9aa2031ed5'),
    ('手机照片恢复管家VIP版', '专业手机照片恢复工具，支持误删照片、视频、文档等多种文件类型恢复，VIP版功能全解锁。', 'https://pan.quark.cn/s/6eb35751e6d1'),
    ('福昕高级PDF编辑器', '福昕PDF编辑器专业版，支持PDF编辑、转换、注释、表单填写、电子签名等全套功能。', 'https://pan.quark.cn/s/88398fa94928'),
    ('微信对话生成器', '生成逼真的微信聊天截图，支持自定义头像、昵称、消息内容，用于演示和创意制作。', 'https://pan.quark.cn/s/e681e222ae6c'),
    ('傻瓜英语VIP解锁版', '英语学习应用，通过情景对话和AI口语练习提升英语水平，VIP版解锁全部课程。', 'https://pan.quark.cn/s/0f69354ca70f'),
    ('酷我音乐破解版SVIP解锁', '酷我音乐破解版，解锁SVIP全部特权，支持无损音质、无损下载、付费歌曲免费听，兼容鸿蒙系统。', 'https://pan.quark.cn/s/2921e8a1b59c'),
    ('Windows系统永久激活密钥', 'Windows系统激活工具，支持Win7/10/11各版本永久激活，操作简单一键激活。', 'https://pan.quark.cn/s/275d58007c5e'),
    ('畅听FM免费收听全国电台', '电台收听应用，可收听全国各级广播电台，免费无广告，支持定时关闭和收藏频道。', 'https://pan.quark.cn/s/b7046489b6b0'),
    ('Android健身教练v1.1.5免费版', '手机健身应用，提供专业健身课程和训练计划，免费无广告，居家健身好帮手。', 'https://pan.quark.cn/s/1826d7020682'),
    ('开发全能工具箱He3', '开发者必备工具箱，集成JSON格式化、正则测试、编码转换、时间戳转换等30+开发常用工具。', 'https://pan.quark.cn/s/44ead176505a'),
    ('情侣飞行棋游戏', '双人对战飞行棋游戏，支持远程联机对战，情侣互动必备，先保存防和谐。', 'https://pan.quark.cn/s/e7686d3af590'),
    ('万能格式转换器', '全能格式转换工具，支持视频、音频、图片、文档等多种格式互转，一站式解决格式问题。', 'https://pan.quark.cn/s/bc01151338ab'),
    ('解析机器人破解版', '短视频解析工具，支持抖音、快手、皮皮虾等平台视频去水印下载，破解版功能全开。', 'https://pan.quark.cn/s/1a7eb2d5e97c'),
    ('GET漫画v2.1.1绿化版', '漫画阅读工具，支持多源搜索漫画资源，绿化版免安装，支持下载和离线阅读。', 'https://pan.quark.cn/s/7ecfc9951415'),
    ('任小聊天话术APP', '聊天话术助手，提供海量聊天话题和回复模板，帮你提升聊天技巧和社交能力。', 'https://pan.quark.cn/s/b3f5ed71e705'),
    ('视频音频批量格式转换器v2.0', '支持批量视频和音频格式转换，多线程处理速度快，支持自定义参数和预设方案。', 'https://pan.quark.cn/s/504ba86954a3'),
    ('微信聊天恢复4.6.0', '微信聊天记录恢复工具，支持恢复误删的聊天消息、图片、视频等，操作简单。', 'https://pan.quark.cn/s/422a8656030e'),
    ('万象聚搜v1.5多功能搜索', '多功能聚合搜索工具，支持小说搜索、漫画搜索、视频去水印等多种功能于一体。', 'https://pan.quark.cn/s/e5d3418ec0c1'),
    ('风云录屏大师VIP版', '高清录屏工具，VIP版无水印无广告，支持全屏录制、区域录制、摄像头录制。', 'https://pan.quark.cn/s/0cb1bbec039c'),
    ('视频去重工具', '短视频去重工具，通过修改视频参数实现二次创作，支持批量处理用于自媒体运营。', 'https://pan.quark.cn/s/ccee65cc166f'),
    ('黑神话悟空PC版', '国产3A大作黑神话悟空PC版，以西游记为背景的硬核动作RPG游戏。', 'https://pan.quark.cn/s/bf63e69e7ac4'),
    ('AutoGLM AI自动化工具', 'AI自动化操作工具，基于大模型实现手机和电脑的自动化操作，解放双手提升效率。', 'https://pan.quark.cn/s/2846843621eb'),
    ('博看书苑安卓附36个授权码', '电子书阅读应用，支持多种格式电子书阅读，附赠36个授权码解锁全部书源。', 'https://pan.quark.cn/s/a2daac82453e'),
    ('夸父工具箱', '安卓工具箱应用，集成多种实用小工具，界面简洁功能丰富。', 'https://pan.quark.cn/s/dc45d88e2e97'),
    ('工具魔盒2.4.2', '多功能工具合集应用，包含系统工具、媒体工具、网络工具等多种实用功能。', 'https://pan.quark.cn/s/cdce324e9439'),
    ('安卓解析机器人高级版', '高级版视频解析工具，支持更多平台和更高清的视频解析下载。', 'https://pan.quark.cn/s/e9e7a37395af'),
    ('太极工具箱', '安卓高级工具箱，支持免root实现Xposed模块功能，扩展手机能力。', 'https://pan.quark.cn/s/d8647b53e016'),
    ('快影剪辑纯净版', '快影视频剪辑工具纯净版，无广告无水印，支持视频剪辑、特效、字幕等功能。', 'https://pan.quark.cn/s/de8c3c44f755'),
    ('Xmind思维导图模板331个', '331个精美Xmind思维导图模板，覆盖商务、教育、生活等多个场景，直接套用高效制作。', 'https://pan.quark.cn/s/b31c5d0863d5'),
]

CAT = 85
ok = 0
total = len(resources)
for i, (t, d, l) in enumerate(resources):
    print("[{}/{}] {}...".format(i+1, total, t[:20]), flush=True)
    pid = publish(t, d, l, CAT)
    if pid:
        print("  OK ID:{}".format(pid), flush=True)
        ok += 1
    else:
        print("  FAILED", flush=True)
    time.sleep(0.3)

ssh.close()
print("\nDone: {}/{}".format(ok, total), flush=True)
