import paramiko, sys
from datetime import datetime
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

css = "<style>.comments-area,#comments,.comment-respond{display:none!important;}</style>"

def publish(title, desc, link, cat_id):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    body = "<p><strong>{}</strong></p><p>{}</p><h3>下载链接：</h3><p><strong>夸克网盘：</strong> <a href=\"{}\">{}</a></p><blockquote><p>提示：复制链接打开夸克APP即可保存。资源来自网络，仅供学习交流。</p></blockquote>".format(desc, desc, link, link) + css
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
        print("  SQL ERR: {}".format(err[:80]), flush=True)
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

# 传统文化(90)
传统文化 = [
    ('韩国首尔大学奎章阁藏汉籍1823册', '韩国首尔大学奎章阁珍藏中国汉籍文献，1823册PDF，10.49GB珍贵古籍资料。', 'https://pan.quark.cn/s/39482eba6d3c', 90),
    ('说郛系列古籍', '说郛系列古籍文献汇编，明代陶宗仪编纂的大型丛书。', 'https://pan.quark.cn/s/9932029b51c6', 90),
    ('四库全书子部医家类489本', '文渊阁四库全书子部医家类全套489本，中医药古籍宝库。', 'https://pan.quark.cn/s/d9e1edff7bea', 90),
    ('文渊阁四库全书史部', '文渊阁四库全书史部全套，中国古典史学文献集大成。', 'https://pan.quark.cn/s/22196e306bea', 90),
    ('四庫全書薈要500册台湾版', '四库全书荟要500册，台湾世界书局出版版本，精选四库精华。', 'https://pan.quark.cn/s/daefd5535fcc', 90),
    ('哈佛燕京图书馆藏明代史料277册', '哈佛燕京图书馆珍藏明代史料汇编，277册PDF共16.91GB。', 'https://pan.quark.cn/s/767e9885525d', 90),
    ('哈佛大学图书馆藏中文古籍善本', '哈佛大学图书馆馆藏中文古籍善本文献合集，学术研究珍贵资料。', 'https://pan.quark.cn/s/f818b1203d40', 90),
    ('德国巴伐利亚图书馆中国汉籍728册', '德国巴伐利亚州立图书馆藏中国汉籍，728册PDF共125GB。', 'https://pan.quark.cn/s/010ea76b4091', 90),
    ('皇明理学名臣言行録明写本', '明代杨廉著皇明理学名臣言行録，江户初写本珍贵影印。', 'https://pan.quark.cn/s/a96a4fb30d0f', 90),
    ('道教道藏书籍合集40G', '道教道藏全套书籍合集40GB，道家经典文献完整收录。', 'https://pan.quark.cn/s/11b34ce35d92', 90),
    ('易经类国学文化合集', '易经相关国学文化书籍合集，含六爻、梅花易数、风水等。', 'https://pan.quark.cn/s/e5dd41f29fc4', 90),
    ('古典著作合集', '中国古典著作合集，涵盖经史子集各类经典文献。', 'https://pan.quark.cn/s/842b251055fd', 90),
    ('古图类古籍合集', '古代图谱类古籍合集，含地图、星图、建筑图等珍贵古图。', 'https://pan.quark.cn/s/8b1921a44eed', 90),
    ('民间秘术大全', '民间秘术秘法大全，收录民间流传的各种术数和秘方。', 'https://pan.quark.cn/s/e0235f7937f2', 90),
    ('各地县志合集', '全国各地县志地方志合集，研究地方历史文化必备资料。', 'https://pan.quark.cn/s/b50132ec550a', 90),
    ('图解经典系列合集', '图解经典系列，涵盖老庄、易经、风水、术数、奇门遁甲、道教、佛教等。', 'https://pan.quark.cn/s/a2b8a6f9a3b0', 90),
    ('中华玄学文化书系', '中华玄学文化系列丛书，系统介绍中国传统玄学文化。', 'https://pan.quark.cn/s/0e7cc71c170e', 90),
    ('经典珍藏古代文献藏书15000册', '经典珍藏版古代文献藏书大合集15000册，超大规模古籍图书馆。', 'https://pan.quark.cn/s/061ba1710d7a', 90),
    ('博物志10卷', '晋代张华撰博物志十卷，中国古代博物学经典著作。', 'https://pan.quark.cn/s/2f79ac0be1c6', 90),
    ('古籍十二大类专题135GB', '古籍文献十二大类专题合集135GB，全面覆盖经史子集。', 'https://pan.quark.cn/s/4d5f4815adc9', 90),
    ('鬼谷子明刊本', '鬼谷子明刊本影印版，兵家纵横家经典原版文献。', 'https://pan.quark.cn/s/817823ae77e4', 90),
    ('中华现代学术名著丛书279种', '中华现代学术名著丛书279种，收录中国现代学术经典著作。', 'https://pan.quark.cn/s/9f83e92fcd56', 90),
    ('普林斯顿大学馆藏中文古籍300册', '普林斯顿大学图书馆馆藏中文古籍300册PDF共109GB。', 'https://pan.quark.cn/s/2043f8e6d8c0', 90),
    ('台北故宫博物院甲库善本100册', '台北故宫博物院甲库善本100册33GB，宫廷珍藏善本影印。', 'https://pan.quark.cn/s/d406e5a6b62c', 90),
    ('周易相关古籍合集', '周易易经相关古籍文献合集，术数易学研究者必备。', 'https://pan.quark.cn/s/f924de51d6bf', 90),
    ('千本古籍合集', '千本中国古典古籍合集PDF，大规模古籍数字化成果。', 'https://pan.quark.cn/s/511b46015566', 90),
    ('佛教佛藏电子书合集', '佛教大藏经及相关佛学电子书合集，佛学研究者必备。', 'https://pan.quark.cn/s/87c5fce28b5a', 90),
    ('永乐大典', '永乐大典影印版，中国古代最大的类书，中华文化瑰宝。', 'https://pan.quark.cn/s/6096ccbd5b66', 90),
    ('珍藏稀有道家资料522本', '522本稀有道家文献资料合集，涵盖内丹、符箓、科仪等。', 'https://pan.quark.cn/s/d278b26a984e', 90),
    ('中华武术合集', '中国传统武术全套合集，涵盖各门各派武学典籍。', 'https://pan.quark.cn/s/f8eea850c270', 90),
    ('天下第一奇书', '天下第一奇书合集，收录中国古代各种奇书秘籍。', 'https://pan.quark.cn/s/ab9a420579a7', 90),
    ('天下第一相书云谷山人著', '天下第一相书，云谷山人著，传统相术经典。', 'https://pan.quark.cn/s/9694d8b12d2e', 90),
    ('民国摄影合集', '民国时期珍贵老照片合集，记录近代中国社会历史。', 'https://pan.quark.cn/s/7d7ca1f53b60', 90),
    ('风水学入门到精通', '风水学系统教程，从入门到精通全面讲解风水知识。', 'https://pan.quark.cn/s/79eba9118e5e', 90),
    ('风水玄学合集', '风水玄学类资料合集，含堪舆、命理、择吉等传统文化内容。', 'https://pan.quark.cn/s/0c74d5077d75', 90),
    ('围棋古棋谱丛书', '中国围棋古棋谱丛书合集，收录历代名局棋谱。', 'https://pan.quark.cn/s/fa6092987b38', 90),
    ('最全古钱谱', '最全中国古代钱币图谱，钱币收藏爱好者和研究者的必备工具书。', 'https://pan.quark.cn/s/3e67ac41fe35', 90),
    ('全网最全珍藏图鉴系列大全', '全网最全的珍藏版图鉴系列大全，涵盖百科、动植物、矿物等各类图鉴。', 'https://pan.quark.cn/s/85f8e32f2810', 90),
]

# 健康养生(87)
健康养生 = [
    ('图解古代名仕养生第一经典', '古代名仕养生经典图解版，图文并茂讲解传统养生之道。', 'https://pan.quark.cn/s/7f08fb285764', 87),
    ('国医绝学家庭使用手册', '国医绝学家庭实用手册，涵盖中医常识、按摩、拔罐、刮痧、艾灸等养生方法。', 'https://pan.quark.cn/s/ac801fe3f522', 87),
    ('中医古法家传秘方药膳大全', '中医古法家传秘方合集，补肾壮阳药膳大全180余种。', 'https://pan.quark.cn/s/333f9584e39c', 87),
    ('杏林医学苑穴位232集全', '杏林医学苑穴位讲解232集全，一病一讲轻松自学人体250个穴位。', 'https://pan.quark.cn/s/420c9f59db65', 87),
    ('古法美颜术', '传统古法美颜术，古代宫廷美容养颜秘法汇编。', 'https://pan.quark.cn/s/0c589d041f5e', 87),
    ('秘功回春术详细版', '秘功回春术完整版，传统道家养生功法详解。', 'https://pan.quark.cn/s/a95deb1a2f99', 87),
    ('台湾图书馆特藏中医古籍288本', '台湾图书馆特藏中医古籍288本，两岸中医药文献珍贵收藏。', 'https://pan.quark.cn/s/70183a025174', 87),
    ('中医类抄本100本', '中医古籍珍稀抄本100本，手抄本中医文献合集。', 'https://pan.quark.cn/s/85429893c3c8', 87),
    ('本草纲目原色图谱800例', '本草纲目原色图谱800例，图文对照认识中草药。', 'https://pan.quark.cn/s/8d9812ba1a24', 87),
    ('中国传统道家养生文化经典', '中国传统道家养生文化经典文献合集，内丹导引养生术。', 'https://pan.quark.cn/s/a81000411461', 87),
    ('倪海厦课程汇总', '中医名师倪海厦全套课程汇总，含黄帝内经、神农本草经、伤寒论等。', 'https://pan.quark.cn/s/8ff1fc2a192e', 87),
    ('倪海厦资源全集收藏版', '倪海厦全部资源收藏版，中医学习者的宝库。', 'https://pan.quark.cn/s/914679cdbdf4', 87),
    ('古籍医书汇总', '中国古籍医书汇总合集，传统中医典籍大全。', 'https://pan.quark.cn/s/952f287cd7b8', 87),
    ('100套中医课程582G', '100套中医培训课程教程合集582GB，涵盖各科中医教学。', 'https://pan.quark.cn/s/f9e85e83f289', 87),
    ('中医古籍珍稀抄本精选', '中医古籍珍稀抄本精选合集，孤本善本中医文献。', 'https://pan.quark.cn/s/8c1eedf8da05', 87),
    ('上千本医学类书籍48GB', '上千本医学类书籍大合集48GB，中西医学全覆盖。', 'https://pan.quark.cn/s/1443f17a9463', 87),
    ('绝版中医课程资料1.18TB', '原价59880元绝版中医课程资料大全收藏版1.18TB，中医培训终极资源。', 'https://pan.quark.cn/s/f6c8f89be7f9', 87),
    ('自学中医之路丛书16册', '自学中医之路丛书全套16册，系统学习中医的入门经典。', 'https://pan.quark.cn/s/b95439565e58', 87),
    ('四大名医传人说养生', '四大国医名师传人讲解养生之道，传统养生智慧传承。', 'https://pan.quark.cn/s/902a7232ca6d', 87),
]

# 书籍资料(81)
书籍资料 = [
    ('世界顶级畅销书900本', '世界顶级畅销书900本合集，涵盖文学、商业、心理学等各领域。', 'https://pan.quark.cn/s/7d161e804874', 81),
    ('喜玛拉雅精读全球好书300本', '喜玛拉雅精读全球好书300本三季全，有声读物精装合集。', 'https://pan.quark.cn/s/60ba000cfa12', 81),
    ('顶级销售必读24本书PDF', '顶级销售必读的24本书电子书PDF，销售精英修炼手册。', 'https://pan.quark.cn/s/79e6d5a86953', 81),
    ('豆瓣评分最高170本精选', '豆瓣评分最高的170本书精选合集，高质量阅读推荐。', 'https://pan.quark.cn/s/f0e51fb487ec', 81),
    ('新知文库合集4000册', '新知文库精选4000册合集，总有你爱看的书。', 'https://pan.quark.cn/s/27b5597985a2', 81),
    ('股票期货外汇期权投资书籍56本', '金融投资类书籍56本，涵盖股票、期货、ETF、外汇、期权等。', 'https://pan.quark.cn/s/9fd8bba3faf6', 81),
    ('终身学习与认知升级经典套装', '终身学习与认知升级畅销经典套装，提升思维能力的必读书单。', 'https://pan.quark.cn/s/97d44d2ce87c', 81),
    ('董宇辉推荐至少读3遍的10本书', '董宇辉推荐的10本好书，值得反复阅读的经典之作。', 'https://pan.quark.cn/s/4c0c0ab24417', 81),
    ('毛泽东选集', '毛泽东选集电子版，重要政治理论著作。', 'https://pan.quark.cn/s/cebc470daa24', 81),
    ('超级好玩的科普书套装4册', '超级好玩的科普书套装共4册，让科学变得有趣。', 'https://pan.quark.cn/s/9802d9840d25', 81),
    ('曾国藩智慧精髓大合集', '曾国藩智慧精髓大合集套装三册，曾国藩家书与处世智慧。', 'https://pan.quark.cn/s/cf9d21fb7451', 81),
    ('心理学书籍301本', '心理学书籍301本大合集，从入门到专业全覆盖。', 'https://pan.quark.cn/s/44938c1dd0e5', 81),
    ('黑客技术学习书籍合集', '黑客网络安全技术学习书籍大合集，信息安全入门到进阶。', 'https://pan.quark.cn/s/f4d72aa149f0', 81),
    ('电子书网站关闭留下整个书库', '一个电子书网站被关闭后留下的完整书库资源，海量电子书。', 'https://pan.quark.cn/s/e9bde4b4632e', 81),
    ('金融行业书籍合集', '金融行业专业书籍合集，银行、证券、保险等领域全覆盖。', 'https://pan.quark.cn/s/db57c42acf33', 81),
    ('中国国家地理百科全书10册', '中国国家地理百科全书珍藏版套装共10册，图文并茂介绍中国地理。', 'https://pan.quark.cn/s/868a96ea1589', 81),
    ('古代房事秘籍大全25本', '中国古代房中术秘籍大全25本，传统文化研究资料。', 'https://pan.quark.cn/s/d68428f86d90', 87),
    ('男性性技宝典', '男性健康养生宝典，传统房中术相关资料。', 'https://pan.quark.cn/s/97021033b43c', 87),
    ('萌版X动作讲解', '两性关系科普教育资料，健康知识讲解。', 'https://pan.quark.cn/s/11df9365a292', 87),
]

# 教育资源(84)
教育资源 = [
    ('各行业精选付费课程资料1TB', '各行业精选付费课程资料合集1TB，吐血整理干货满满。', 'https://pan.quark.cn/s/21172135a29b', 84),
    ('各行各业源码1900套合集', '各行各业项目源码1900套资料大合集，开发者学习宝库。', 'https://pan.quark.cn/s/b946c48d22f6', 84),
    ('最新监理资料精整合集', '建筑工程监理资料精整大合集，监理从业者必备。', 'https://pan.quark.cn/s/cc69d090f713', 84),
    ('看看有惊喜综合资源包', '综合资源大礼包，打开看看有惊喜，多类资源合集。', 'https://pan.quark.cn/s/f15a8f504cba', 84),
]

# 工具合集(85) + 自媒体(83)
其他 = [
    ('万套PPT模板合集', '一万套PPT模板大合集，工作汇报、教学课件、商业计划全覆盖。', 'https://pan.quark.cn/s/21dd84f73737', 85),
    ('900份各行各业实用合同', '900份各行各业实用合同模板合集，法律文书模板库。', 'https://pan.quark.cn/s/faa0599fce1a', 85),
    ('经典励志哲理文案系列', '经典励志哲理文案素材系列，自媒体创作者文案灵感库。', 'https://pan.quark.cn/s/173ce7a9a277', 83),
    ('情感文案情感语录系列', '情感文案情感语录素材系列，适合朋友圈和短视频使用。', 'https://pan.quark.cn/s/9adf7760b57c', 83),
    ('伤感文案系列', '伤感文案素材系列，情感类自媒体创作素材库。', 'https://pan.quark.cn/s/048d888a46cc', 83),
]

all_resources = 传统文化 + 健康养生 + 书籍资料 + 教育资源 + 其他
ok = 0
total = len(all_resources)
print("Total: {} resources to publish".format(total), flush=True)

for i, (t, d, l, c) in enumerate(all_resources):
    print("[{}/{}] {}...".format(i+1, total, t[:25]), flush=True)
    pid = publish(t, d, l, c)
    if pid:
        print("  OK ID:{}".format(pid), flush=True)
        ok += 1
    else:
        print("  FAILED", flush=True)
    time.sleep(0.2)

ssh.close()
print("\nDone: {}/{}".format(ok, total), flush=True)
