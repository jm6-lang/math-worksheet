import paramiko
from datetime import datetime
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

css = "<style>.comments-area,#comments,.comment-respond{display:none!important;}</style>"

def publish(title, desc, link, cat_id):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    body = "<p><strong>{}</strong></p><h3>资源介绍：</h3><p>{}</p><h3>下载链接：</h3><p><strong>链接：</strong> <a href=\"{}\">{}</a></p><blockquote><p>提示：复制链接打开对应APP即可保存。资源来自网络，仅供学习交流。</p></blockquote>".format(desc, desc, link, link) + css
    t = title.replace("\\", "\\\\").replace("'", "\\'")
    c = body.replace("\\", "\\\\").replace("'", "\\'")
    pn = "book-{}-{}".format(int(time.time()), abs(hash(title)) % 10000)
    sql = "INSERT INTO wp_posts (post_author,post_date,post_date_gmt,post_content,post_title,post_excerpt,post_status,comment_status,ping_status,post_password,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered,post_parent,guid,menu_order,post_type,post_mime_type,comment_count) VALUES (1,'{}','{}','{}','{}','','publish','open','open','','{}','','','{}','{}','',0,'',0,'post','',0);".format(now, now, c, t, pn, now, now)
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/wp_p.sql', 'w') as f:
        f.write(sql)
    sftp.close()
    stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm < /tmp/wp_p.sql 2>&1")
    err = stderr.read().decode().strip()
    if err and 'error' in err.lower():
        print("  SQL ERR: {}".format(err[:60]), flush=True)
        return None
    stdin, stdout, stderr = ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT MAX(ID) FROM wp_posts WHERE post_type='post';\"")
    pid = stdout.read().decode().strip()
    cat_sql = "INSERT INTO wp_term_relationships (object_id,term_taxonomy_id,term_order) VALUES ({},{},0); UPDATE wp_term_taxonomy SET count=count+1 WHERE term_id={};".format(pid, cat_id, cat_id)
    sftp = ssh.open_sftp()
    with sftp.open('/tmp/wp_c.sql', 'w') as f:
        f.write(cat_sql)
    sftp.close()
    ssh.exec_command("mysql -uwpuser -p'WpPass2024!' wp_skillxm < /tmp/wp_c.sql 2>&1")
    return pid

# 书籍资料(81)
book_resources = [
    ('中国古玩鉴识知识系列书籍', '中国古玩鉴识知识系列书籍，文物鉴赏指南。', 'https://pan.xunlei.com/s/VOOk9ly0JBu9rQyGiwv31UsnA1?pwd=uy8e#', 81),
    ('创业优质教程合集', '创业优质教程合集，爱看书读好书系列。', 'https://pan.xunlei.com/s/VOOuKbEkRTmQCQcZcBrRvcYtA1?pwd=y96q#', 81),
    ('百病食疗大全彩图精装', '百病食疗大全彩图精装版，食疗养生必备。', 'https://pan.xunlei.com/s/VOOuKiYOFPUtXUKuIOgMhb4yA1?pwd=nidc#', 81),
    ('用声音修炼气场完结', '用声音修炼气场课程完结版。', 'https://pan.xunlei.com/s/VOOuLYoTRTmQCQcZcBrRvzs-A1?pwd=2xtq#', 81),
    ('梅花易数白话解', '梅花易数白话解，象数思维的智慧。', 'https://pan.xunlei.com/s/VOOuLe65NaBNlzRDdqMF43NUA1?pwd=kk74#', 81),
    ('富爸爸系列全集32册', '富爸爸系列全集纪念新版共32册。', 'https://pan.xunlei.com/s/VOP3rnoD-wEAtCmsdBlggRXRA1?pwd=4m5x#', 81),
    ('书库合集', '书库合集，电子书资源大全。', 'https://pan.xunlei.com/s/VOQ6I4rzezacrOCmZ3xzNozIA1?pwd=dmnj#', 81),
    ('顶级思维法套装7册', '人人都可以学的顶级思维法套装共7册。', 'https://pan.xunlei.com/s/VOQ6KC01-caw75eeiJRzVHXPA1?pwd=2474#', 81),
    ('富爸爸套装五册', '富爸爸点石成金等套装共五册。', 'https://pan.xunlei.com/s/VOQ6KI9A7MK-8MadlJlaxMUgA1?pwd=re3g#', 81),
    ('中医补肾壮阳秘方', '中医补肾壮阳秘方，传统养生知识。', 'https://pan.xunlei.com/s/VOQ6MNnRpklQNxGL9FDLjXYdA1?pwd=wqx2#', 81),
    ('父与子的X教尬聊', '父与子的X教尬聊，育儿话题。', 'https://pan.xunlei.com/s/VOQ6Mi03829Ak4YZiGHD5x7yA1?pwd=cy93#', 81),
    ('MBA课程', 'MBA课程资源合集。', 'https://pan.xunlei.com/s/VOQ6MoEjeF5hzjNz8XoKo6nVA1?pwd=mv75#', 81),
    ('中医古籍合集超全系列', '中医古籍合集超全系列，中医配方资料。', 'https://pan.xunlei.com/s/VOQBckc4OoRRo7e7hTVWQymaA1?pwd=7fqn#', 81),
    ('农村自建房图纸合集', '最新上千套农村自建房图纸合集。', 'https://pan.xunlei.com/s/VOVjp6cmrCI1e6xO09VM77mAA1?pwd=emit#', 81),
]

# 工具合集(85)
tool_resources = [
    ('解锁版软件合集', '解锁版软件每日更新实用软件合集。', 'https://pan.xunlei.com/s/VOOaMJ54DvaNOzRoOLlxR5o2A1?pwd=a6ub#', 85),
    ('TikTokMod解除限制版', 'TikTokMod解除限制版。', 'https://pan.xunlei.com/s/VOU7rQiMuAdJSBAnyq_Nm2ZtA1?pwd=ky3z#', 85),
    ('一键迁移网盘资源', '一键迁移网盘资源百度转迅雷工具。', 'https://pan.xunlei.com/s/VOOaMRjWtx2hjdy5BesUfxSnA1?pwd=cjtj#', 85),
    ('迅雷最新不限速版', 'win版迅雷最新不限速版。', 'https://pan.xunlei.com/s/VOOaMd0Syh9lX_tN9sdXs7xcA1?pwd=475j#', 85),
    ('wifi万能钥匙SVIP版', 'wifi万能钥匙SVIP版。', 'https://pan.xunlei.com/s/VOOuLKYI6SticUyS536Y85X2A1?pwd=sdm8#', 85),
    ('UC网盘批量转存工具', 'UC网盘批量转存工具。', 'https://pan.xunlei.com/s/VOQ6LDS8IEc-3wd4nNsUs6ZpA1?pwd=6ezx#', 85),
    ('夸克网盘批量转存工具', '夸克网盘批量转存分享工具。', 'https://pan.xunlei.com/s/VOQ6LIBchwbqjdXwYUw4zaeBA1?pwd=n8hd#', 85),
    ('金铲铲单机版', '金铲铲单机版超详细教程9999+金币。', 'https://pan.xunlei.com/s/VOQ6Mckoft4N8Zuq13Rr67HKA1?pwd=hvcq#', 85),
    ('骗子酒馆手机版', '骗子酒馆手机版。', 'https://pan.xunlei.com/s/VOQBZq70LnlUbHA45Jg4GXKcA1?pwd=x4sh#', 85),
    ('可灵无限灵感值', '可灵无限灵感值。', 'https://pan.xunlei.com/s/VOQBZwUyKUAl4DNNfMGcsABPA1?pwd=c2g4#', 85),
    ('机顶盒视频教程', '全网最全机顶盒视频教程。', 'https://pan.xunlei.com/s/VOQB_yHrz7MdEh5qGBzMq6KiA1?pwd=9fn3#', 85),
    ('迅雷VIP解锁版', '迅雷VIP解锁版。', 'https://pan.xunlei.com/s/VOUCp8cC0hTpuOaP6-RwTTTjA1?pwd=psyh#', 85),
    ('微信好友检测工具', '微信好友检测工具李跳跳真实好友。', 'https://pan.xunlei.com/s/VOUCs9zzzro06gxXj-OeRpgeA1?pwd=zayh#', 85),
    ('影梭定位修改大师', '影梭定位修改大师。', 'https://pan.xunlei.com/s/VOUIMuAtd8aW70HVfIb_pG62A1?pwd=5fh6#', 85),
    ('抢福袋工具', '抢福袋工具。', 'https://pan.xunlei.com/s/VOUIqHXWiH86exGXkPLRSPDtA1?pwd=8v5z#', 85),
    ('微粉大师', '微粉大师。', 'https://pan.xunlei.com/s/VOUNDvC01nsSdn0t7wIaNlyCA1?pwd=8d5r#', 85),
    ('李跳跳跳广告神器', '李跳跳跳广告神器非常好用。', 'https://pan.xunlei.com/s/VOUNExYviH86exGXkPLTs92OA1?pwd=jve7#', 85),
    ('WPS解锁版', 'WPS解锁版。', 'https://pan.xunlei.com/s/VOUNGDCYsyKaLN-PfIQOX7_3A1?pwd=2ygu#', 85),
    ('Windows纯净版系统镜像', 'Windows纯净版系统镜像大合集。', 'https://pan.xunlei.com/s/VOVQ1ijdL8qAx5s7vkZ5kTQuA1?pwd=e5c9#', 85),
    ('国外最火app合集', '国外最火应用app合集。', 'https://pan.xunlei.com/s/VOVVM2TMrCI1e6xO09VDc1JuA1?pwd=m4eu#', 85),
    ('电脑系统安装工具包', '电脑系统安装工具包。', 'https://pan.xunlei.com/s/VOVeYGpND22zWV5oqAn7nqJJA1?pwd=4qa9#', 85),
    ('抖音短视频下载', '抖音短视频下载提取工具。', 'https://pan.xunlei.com/s/VOVjsNkfZafTzbx1_YscGDyYA1?pwd=399y#', 85),
    ('去除马赛克', '去除马赛克工具。', 'https://pan.xunlei.com/s/VOVp3RqvUtVuXKoLFgchvdgPA1?pwd=6h68#', 85),
    ('AI写作鱼终身VIP', 'AI写作鱼手机号登录终身VIP。', 'https://pan.xunlei.com/s/VOVun5tFShvSW39OHUi_mDjQA1?pwd=vaxg#', 85),
    ('3D动态照片解锁版', '3D动态照片v4.0.0.6解锁版。', 'https://pan.xunlei.com/s/VOVz9TwDFoIhJcrKIoZuY1vHA1?pwd=s489#', 85),
    ('变声器大师破解版', '变声器大师破解版。', 'https://pan.xunlei.com/s/VOW3JS-k4-8tmbnwfgZfFBqFA1?pwd=qijb#', 85),
    ('梨园行戏曲TV版', '梨园行戏曲TV版v995.7.2解锁会员版。', 'https://pan.xunlei.com/s/VOW8VTmvEiWTwdiuF1dxE9pyA1?pwd=spnp#', 85),
    ('马克全能去水印', '马克全能去水印v1.1.5绿化解锁版。', 'https://pan.xunlei.com/s/VOWD_nrQwZcva3xhSMZUf062A1?pwd=j3ed#', 85),
    ('Zapya快牙解锁版', 'Zapya快牙v6.5.5解锁版无限制跨平台文件互传。', 'https://pan.xunlei.com/s/VOWIs-iGNCOKKEYQ-SO7zRKZA1?pwd=j5d3#', 85),
    ('作业帮修改版', '作业帮v13.61.0修改解锁绿化免费版。', 'https://pan.xunlei.com/s/VOWOBNPwn0pAejN8kN4ulJJ9A1?pwd=vgq4#', 85),
    ('TVBox_takagen99免费版', 'TVBox_takagen99免费版含影视源文件。', 'https://pan.xunlei.com/s/VOWTCi3XrUcu62wAnKAvVD4jA1?pwd=efu4#', 85),
    ('酷我音乐车机版', '酷我音乐_6.0.1.0-Mod车机版解锁会员。', 'https://pan.xunlei.com/s/VOWYC39PkmCwNNOZD-ixu68QA1?pwd=8nbv#', 85),
    ('Youtube视频下载器', 'Youtube油管视频下载器。', 'https://pan.xunlei.com/s/VOWYEH0EkmCwNNOZD-ixvJFYA1?pwd=jjj2#', 85),
    ('视频去水印神器', '视频去水印神器HitPaw Watermark Remover。', 'https://pan.xunlei.com/s/VOWYHlx03_HvPduhhAQFlYaLA1?pwd=edax#', 85),
    ('轻听音乐免费版', '轻听音乐v2.2.6免费版无限制多线路免费音乐。', 'https://pan.xunlei.com/s/VOWcbhIhc3ogRlnOhWz16z-lA1?pwd=3nbk#', 85),
    ('全球卫星电视TVgarden', '全球卫星电视TV garden。', 'https://pan.xunlei.com/s/VOWrpwtWTK_RkTvQWYTGJ2pJA1?pwd=s8a8#', 85),
    ('即梦AI破解版', '即梦Ai破解版无限积分。', 'https://pan.xunlei.com/s/VOWrq9oLeoQT89x8UX6ZS-cFA1?pwd=h48t#', 85),
    ('动物翻译器', '动物翻译器。', 'https://pan.xunlei.com/s/VOWrqDLfYa-Iuq5t6PKsOHgYA1?pwd=fi2t#', 85),
    ('搬运工具包', '搬运工具包。', 'https://pan.xunlei.com/s/VOX6JDhMOOp5Lb8QDfV7mxp4A1?pwd=cx78#', 85),
    ('电脑密码破解工具', '电脑密码破解工具。', 'https://pan.xunlei.com/s/VOXBRniSZWYhuK2DRAmIJ3HLA1?pwd=gy5h#', 85),
    ('闲鱼助手自动发货', '手机版闲鱼助手自动发货。', 'https://pan.xunlei.com/s/VOXGks0nYB0jDG4ROtTuoiJ0A1?pwd=edim#', 85),
    ('图片批量处理', '图片批量处理工具。', 'https://pan.xunlei.com/s/VOXW6jHtze9Rl3yZAc9OfK0tA1?pwd=6qcd#', 85),
    ('文件批量重命名', '文件批量重命名工具。', 'https://pan.xunlei.com/s/VOXW6r92yNaOLWrUcv2qljKzA1?pwd=7hza#', 85),
    ('手机刷机工具箱', '手机刷机工具箱。', 'https://pan.xunlei.com/s/VOXaFh7CRwAxaJVLO94ZJrKiA1?pwd=ppf6#', 85),
    ('CDR2023破解版', 'CDR2023中文破解版CorelDRAW。', 'https://pan.xunlei.com/s/VOXfSJnKcx4UdHEqZS9f5viOA1?pwd=2z4i#', 85),
    ('打卡软件神器', '打卡软件神器。', 'https://pan.xunlei.com/s/VOXumZU5y-6A2bPiWO5dRzkrA1?pwd=88aq#', 85),
    ('查企业查信息', '查企业查信息限制注册即送5年SVIP。', 'https://pan.xunlei.com/s/VOY--vv8UsLDxjyOGMSyLOd5A1?pwd=48gy#', 85),
    ('笔趣阁完美修改版', '笔趣阁完美修改去广告解锁高级版。', 'https://pan.xunlei.com/s/VOY42lVZqub9V_5XZd13WCacA1?pwd=g4yv#', 85),
    ('公众号爆文机器人', '公众号爆文机器人。', 'https://pan.xunlei.com/s/VOY9Bprql6UfhKDIxYVptHbWA1?pwd=pjji#', 85),
    ('七星虚拟机', '七星虚拟机。', 'https://pan.xunlei.com/s/VOYEPeKFTst6XWzYArT8HCa2A1?pwd=hqgu#', 85),
    ('电商图片采集工具', '电商图片采集工具。', 'https://pan.xunlei.com/s/VOYTyGNoQmx9ciEhFbMA1afdA1?pwd=zru2#', 85),
    ('场控助手', '场控助手。', 'https://pan.xunlei.com/s/VOYZ1P6cokb4EjBfQXAsjmo8A1?pwd=rkhe#', 85),
    ('TVBOX最新接口', 'TVBOX+最新接口。', 'https://pan.xunlei.com/s/VOYdALqV30NTW53quTQfWHhmA1?pwd=beb8#', 85),
    ('AI唱歌软件', 'AI翻唱Ai克隆自己声音唱歌软件。', 'https://pan.xunlei.com/s/VOYiL6cH2GCVrbv91FRy7uEZA1?pwd=whn8#', 85),
    ('SolidWorks2025', 'SolidWorks2025最新完整版。', 'https://pan.xunlei.com/s/VOYnT0SsriDNDGjCciy_H67PA1?pwd=9jbk#', 85),
]

all_resources = book_resources + tool_resources
ok = 0
total = len(all_resources)
print("Publishing {} resources ({} books + {} tools)...".format(total, len(book_resources), len(tool_resources)), flush=True)

for i, (t, d, l, c) in enumerate(all_resources):
    print("[{}/{}] {}...".format(i+1, total, t[:20]), flush=True)
    pid = publish(t, d, l, c)
    if pid:
        print("  OK ID:{}".format(pid), flush=True)
        ok += 1
    else:
        print("  FAILED", flush=True)

ssh.close()
print("\nDone: {}/{}".format(ok, total), flush=True)