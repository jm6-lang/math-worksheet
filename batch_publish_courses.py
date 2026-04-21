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
    pn = "res-{}-{}".format(int(time.time()), abs(hash(title)) % 10000)
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

# 动漫小说类 -> 影视娱乐(86)
anime_resources = [
    ('国漫心动的声音', '国漫心动的声音全集，热门国产动画推荐。', 'https://pan.xunlei.com/s/VOOaNI3XfMGla7ryiVqmjeh2A1?pwd=8idb#', 86),
    ('国漫一醉经年', '国漫一醉经年全集，经典国产漫画。', 'https://pan.xunlei.com/s/VOOaLLaebOjliyh3J4n57KFrA1?pwd=97x7#', 86),
    ('海外动漫大合集', '海外动漫大合集，日韩美动画全集。', 'https://pan.xunlei.com/s/VOQ6HmfTqOKXA42tDmbjtuHRA1?pwd=mi6x#', 86),
    ('动漫影视', '动漫影视作品合集，动画电影推荐。', 'https://pan.xunlei.com/s/VOQ6INjfEA2Y8YjpMwYDCF93A1?pwd=2qmt#', 86),
    ('爆燃动漫剪辑', '爆燃动漫剪辑合集，经典片段集锦。', 'https://pan.xunlei.com/s/VOQBYxq24u-CygjX9Tcm0_vaA1?pwd=g9vy#', 86),
]

# 音乐类 -> 影视娱乐(86)
music_resources = [
    ('超全音乐合集', '超全音乐合集，热门歌曲一次听够。', 'https://pan.xunlei.com/s/VOQ6EmI-iQ_8twVbXwFaP3siA1?pwd=bmzr#', 86),
    ('上万首音乐合集', '上万首音乐合集，海量歌曲资源。', 'https://pan.xunlei.com/s/VOQ6F5Yc2esiP0XWBKwJilRRA1?pwd=vqud#', 86),
    ('003车载高清MV持续更新', '003车载高清MV合集，持续更新中。', 'https://pan.xunlei.com/s/VOQ6FJquhmy4r_XKAnK9GkWqA1?pwd=wx67#', 86),
    ('经典老歌1020首', '经典老歌1020首，怀旧金曲合集。', 'https://pan.xunlei.com/s/VOQ6JtR3TsH5kZ03S1gE8TPWA1?pwd=pf6k#', 86),
    ('零基础学唱粤语歌曲', '零基础学唱粤语歌曲KTV教程。', 'https://pan.xunlei.com/s/VOQ6K-KHNSmMb1YsHO_RG5U5A1?pwd=6kmd#', 86),
]

# 学习课程类 -> 教育资源(84)
course_resources = [
    ('office全套学习资料', 'office全套学习资料，办公室一族必备技能。', 'https://pan.xunlei.com/s/VOOaLurmDvaNOzRoOLlxQu97A1?pwd=bzmd#', 84),
    ('创业副业引流必备', '创业副业引流必备教程，流量变现指南。', 'https://pan.xunlei.com/s/VOOaMBk3aNeIhBhmUKznB4VvA1?pwd=mtj5#', 84),
    ('剪映预设专场蒙版调色合集', '剪映预设专场+蒙版+调色合集，视频剪辑必备。', 'https://pan.xunlei.com/s/VOOaMF1xtx2hjdy5BesUfrv4A1?pwd=9hv2#', 84),
    ('瑜伽从初级到高级100课', '瑜伽从初级到高级100课全套教程。', 'https://pan.xunlei.com/s/VOOeoLyukJX_aZwoiNkWleI7A1?pwd=bzjp#', 84),
    ('小学初中教辅资料合集', '小学初中教辅资料合集，学习资料大全。', 'https://pan.xunlei.com/s/VOOetwrUNr60xSX58xAhyVOwA1?pwd=nhin#', 84),
    ('素材库合集音频音效视频CG图片', '素材库合集，音频音效视频CG图片素材。', 'https://pan.xunlei.com/s/VOOeu6UWYpy8J5er-4UwSJDjA1?pwd=m6yr#', 84),
    ('电工技术自学一本通', '电工技术自学一本通，实用电工教程。', 'https://pan.xunlei.com/s/VOOk9yp5rK69yZ7BxcLcQmvtA1?pwd=qz73#', 84),
    ('全新手机维修课程合集', '全新手机维修课程合集，技能学习教程。', 'https://pan.xunlei.com/s/VOOkA4PFdxoVSJw1VI9gXX--A1?pwd=ytaf#', 84),
    ('推拿手法技能中医护理', '推拿手法技能，中医护理教程。', 'https://pan.xunlei.com/s/VOOkAt1C_mrrD5nVVcf7R4naA1?pwd=wmtf#', 84),
    ('零基础化妆入门课程', '零基础化妆入门课程，美妆教程。', 'https://pan.xunlei.com/s/VOOkB-rFnr_4W6s7-XT9hDpkA1?pwd=dfe8#', 84),
    ('陈式太极拳视频教程', '陈式太极拳视频教程，传统武术学习。', 'https://pan.xunlei.com/s/VOOuKnMFlFjUlpMDhOty4N25A1?pwd=ac94#', 84),
    ('小红书图文批量生成', '小红书图文批量生成工具教程。', 'https://pan.xunlei.com/s/VOOuLP7RcTHXBSgoQ8TUE9u5A1?pwd=y5ey#', 84),
    ('木工雕刻学习课程', '木工雕刻学习课程，手工技能教程。', 'https://pan.xunlei.com/s/VOOuLibJYdubhdMd9PHS0dSGA1?pwd=ua49#', 84),
    ('老中医的传世小偏方', '老中医的传世小偏方，日常小病治疗秘方。', 'https://pan.xunlei.com/s/VOOuLxqpkJX_aZwoiNkd1ABcA1?pwd=jszc#', 84),
    ('家庭自制美味辣酱', '家庭实用菜谱，家庭自制美味辣酱制作教程。', 'https://pan.xunlei.com/s/VOOuM32D4_-Pa6ix4UC9NF-YA1?pwd=dn96#', 84),
    ('60种编程语言学习书籍', '60种编程语言学习书籍，编程学习资料。', 'https://pan.xunlei.com/s/VOP3plym1uIGNBJn5Z3gGQP4A1?pwd=qkn9#', 84),
    ('零基础理财入门课', '人人有用的零基础理财入门课。', 'https://pan.xunlei.com/s/VOP3qirJQOdVHsoV-juXOSLJA1?pwd=xwbm#', 84),
    ('零基础学剪映', '零基础学剪映，视频剪辑入门教程。', 'https://pan.xunlei.com/s/VOP3qubpQVZ1ur1_zvuQE3zEA1?pwd=mwc8#', 84),
    ('零基础学唱歌', '零基础学唱歌，歌唱入门教程。', 'https://pan.xunlei.com/s/VOP3r1GPeb6v-im-wVm3VuSSA1?pwd=ynhr#', 84),
    ('零基础学炒股', '零基础学炒股，理财投资教程。', 'https://pan.xunlei.com/s/VOP3rBMsNUlzBbd7cRYvoK_7A1?pwd=2izj#', 84),
    ('零基础学航拍', '零基础学航拍，无人机航拍教程。', 'https://pan.xunlei.com/s/VOP3rIlTNUlzBbd7cRYvoMgbA1?pwd=2t78#', 84),
    ('零基础摄影班', '零基础摄影班，摄影入门教程。', 'https://pan.xunlei.com/s/VOP3rRY7cT3EWLjpt5L_S4WGA1?pwd=embc#', 84),
    ('零基础学手语', '零基础学手语，特殊技能教程。', 'https://pan.xunlei.com/s/VOP3rYTukWzziTqwUC0y_PoFA1?pwd=safr#', 84),
    ('零基础学绘画', '零基础学绘画，艺术入门教程。', 'https://pan.xunlei.com/s/VOP3rdYA3WwJwAbr3_ZNNM-fA1?pwd=3yec#', 84),
    ('恋爱修炼秘籍', '恋爱修炼秘籍，情感提升教程。', 'https://pan.xunlei.com/s/VOP3s7G4eHRZY2IUihc2W4QTA1?pwd=m9bj#', 84),
    ('成人修炼手册', '成人修炼手册，个人成长教程。', 'https://pan.xunlei.com/s/VOP3sG8COZ7sHno8EpjIv6eyA1?pwd=zzz9#', 84),
    ('正妹博士性学教室', '正妹博士性学教室：男女那些羞羞事。', 'https://pan.xunlei.com/s/VOP3sN3WRLFd38dbpR7EvtPoA1?pwd=pjga#', 84),
    ('爱爱技巧', '爱爱技巧，情感知识教程。', 'https://pan.xunlei.com/s/VOP3sStc1dckpi3HngYIQBEGA1?pwd=9335#', 84),
    ('房中技巧班高级研修班', '房中技巧班-高级研修班SVIP课程。', 'https://pan.xunlei.com/s/VOP3sqXERLFd38dbpR7Ew2dUA1?pwd=xhkt#', 84),
    ('吴小飘15堂G点愉悦手册', '吴小飘15堂G点愉悦手册，打开高巢新世界。', 'https://pan.xunlei.com/s/VOP4439m8veTkcQsuuxTDzHfA1?pwd=hw2g#', 84),
    ('男性x技宝典', '男性x技宝典：14招实战Y女术。', 'https://pan.xunlei.com/s/VOP44rwnFXPj87MPK2PWwnuSA1?pwd=bgwe#', 84),
    ('公司文员必存资源', '公司文员必存资源，办公效率资源。', 'https://pan.xunlei.com/s/VOQ6FBWvNSmMb1YsHO_REEqUA1?pwd=3g3n#', 84),
    ('钓鱼视频教程实战大全', '钓鱼视频教程实战大全技巧。', 'https://pan.xunlei.com/s/VOQ6K54BUcNz3Mu_oHtAebFcA1?pwd=9xyj#', 84),
    ('计算机考证课程', '计算机考证课程，职业技能培训。', 'https://pan.xunlei.com/s/VOQ6KRJJPV5TjTtqcfU8aDB7A1?pwd=k25j#', 84),
    ('女性必备20堂情趣指南课', '女性必备的20堂情趣指南课完结版。', 'https://pan.xunlei.com/s/VOQ6KYFJOM4F_E1Lcbt86a6MA1?pwd=ay24#', 84),
    ('女生呵护指南', '女生呵护指南，健康护理教程。', 'https://pan.xunlei.com/s/VOQ6KdJB7MK-8MadlJlaxUbtA1?pwd=297e#', 84),
    ('李银河性学教室', '李银河：这才是你想要的性。', 'https://pan.xunlei.com/s/VOQ6Kt9-LVQRsktvQtBSUTdjA1?pwd=rn95#', 84),
    ('按摩教学', '按摩教学视频教程。', 'https://pan.xunlei.com/s/VOQ6LX14udm-6ik46ZifNZOkA1?pwd=x62q#', 84),
    ('医学课程', '医学课程资源合集。', 'https://pan.xunlei.com/s/VOQ6M187aY8k8FITC81_h0zEA1?pwd=txdg#', 84),
    ('教资', '教师资格证考试资料。', 'https://pan.xunlei.com/s/VOQ6M9e8DzxF93hrLeszFuS9A1?pwd=5gi7#', 84),
    ('美丽芭蕾孕期特辑', '美丽芭蕾孕期特辑视频。', 'https://pan.xunlei.com/s/VOQ6N8Wl829Ak4YZiGHD686aA1?pwd=m5xq#', 84),
    ('辨别渣男渣女训练营', '如何辨别渣男渣女训练营一套成神。', 'https://pan.xunlei.com/s/VOQBYCnJcn-7E-aYxlZZT0AJA1?pwd=z42e#', 84),
    ('微信机器人工具视频教程', '微信机器人工具+视频教程。', 'https://pan.xunlei.com/s/VOQBYMouy5qFuBJcHF8Opc-yA1?pwd=wch8#', 84),
    ('剪映从入门到精通100课', '最新剪映从入门到精通100课。', 'https://pan.xunlei.com/s/VOQBZ9_kWkj3fzJHr6mj76i4A1?pwd=sm8i#', 84),
    ('国际象棋入门教程', '国际象棋入门教程。', 'https://pan.xunlei.com/s/VOQBZOdbLnlUbHA45Jg4GN4FA1?pwd=adyz#', 84),
    ('扑克牌千术揭秘', '扑克牌千术揭秘，十赌九骗教程。', 'https://pan.xunlei.com/s/VOQBZfk-Cu0rmDZIdzUW2wcgA1?pwd=4kjj#', 84),
    ('围棋入门课程大全', '围棋入门课程大全。', 'https://pan.xunlei.com/s/VOQB_QhgUGArPcbdUIa6wLE9A1?pwd=ss7j#', 84),
    ('书法教程零基础写出一手好字', '书法教程：教你零基础写出一手漂亮好字。', 'https://pan.xunlei.com/s/VOQB_XeOc5OUVTauZez_fwDUA1?pwd=77ez#', 84),
    ('心理学通识看透人性', '用科学的心理学通识看透人性。', 'https://pan.xunlei.com/s/VOQB_osJCu0rmDZIdzUW3KrCA1?pwd=pb2e#', 84),
    ('日语零基础直达N1', '日语零基础直达N1课程。', 'https://pan.xunlei.com/s/VOU7snTWH66jxoSBFoNZopvAA1?pwd=4kfa#', 84),
    ('U盘重装系统电脑维修', 'U盘重装系统到电脑系统维护维修视频教程。', 'https://pan.xunlei.com/s/VOYJVgSoUAhvX4E4C5QPoo0wA1?pwd=7khq#', 84),
]

all_resources = anime_resources + music_resources + course_resources
ok = 0
total = len(all_resources)
print("Publishing {} resources (5 anime + 5 music + {} courses)...".format(total, len(course_resources)), flush=True)

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
