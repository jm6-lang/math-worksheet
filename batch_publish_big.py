import paramiko
from datetime import datetime

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# 分类ID
CAT_SELF_MEDIA = 83  # 自媒体运营
CAT_EDU = 84         # 教育资源
CAT_CROSS = 82       # 跨境电商
CAT_TOOL = 85        # 工具合集

# 资源列表
resources = [
    # 自媒体运营
    {'title': '小红书玩法教程最全攻略【24套课】', 'desc': '24套小红书运营课程，从账号注册到爆款笔记，从小白到大神全覆盖。', 'link': 'https://pan.quark.cn/s/cb0de89979a8', 'cat': CAT_SELF_MEDIA},
    {'title': 'TikTok玩法教程最全攻略【27套课】', 'desc': '27套TikTok运营课程，海外短视频爆款玩法，出海必学。', 'link': 'https://pan.quark.cn/s/44a65ca8c8cd', 'cat': CAT_SELF_MEDIA},
    {'title': '抖音玩法教程最全攻略【21套课】', 'desc': '21套抖音运营课程，从0到百万粉丝的完整路径。', 'link': 'https://pan.quark.cn/s/f17ab4fd435d', 'cat': CAT_SELF_MEDIA},
    {'title': '小红书带货42天训练营【无压货】', 'desc': '42天小红书带货实战训练，无需压货，教你低成本起号变现。', 'link': 'https://pan.quark.cn/s/60e57dc22ac8', 'cat': CAT_SELF_MEDIA},
    {'title': '旅行小红书起号运营课程', 'desc': '深入浅出讲解旅行赛道在小红书如何起号、涨粉、引流、变现。', 'link': 'https://pan.quark.cn/s/b6406d8001a1', 'cat': CAT_SELF_MEDIA},
    {'title': '小红书爆款文案【指令+教程】', 'desc': '小红书爆款文案写作技巧，AI指令+详细教程，轻松写出10万+笔记。', 'link': 'https://pan.quark.cn/s/a0eb204cecb7', 'cat': CAT_SELF_MEDIA},
    {'title': '影视解说训练营', 'desc': '从新手进阶到成熟自媒体达人，影视解说全流程实战教学。', 'link': 'https://pan.quark.cn/s/74d6f6d286e4', 'cat': CAT_SELF_MEDIA},
    {'title': '起号：给自媒体人的60条实操干货', 'desc': '60条自媒体起号实操经验，少走弯路，快速起号变现。', 'link': 'https://pan.quark.cn/s/9ad9f6c8a9cf', 'cat': CAT_SELF_MEDIA},
    {'title': '新媒体流量变现运营课程', 'desc': '系统学习新媒体流量获取与变现，从流量到收益的完整闭环。', 'link': 'https://pan.quark.cn/s/af324f13eeaf', 'cat': CAT_SELF_MEDIA},
    {'title': 'TikTok海外影视课程全套', 'desc': 'TikTok海外影视赛道全套课程，出海搞钱必学。', 'link': 'https://pan.quark.cn/s/fd97bad234ed', 'cat': CAT_SELF_MEDIA},
    {'title': '带货短视频文案脚本公式进阶班', 'desc': '带货短视频文案写作公式，脚本模板+案例分析，提升转化率。', 'link': 'https://pan.quark.cn/s/bd65e40662fa', 'cat': CAT_SELF_MEDIA},
    {'title': '视频号风口21天从0到1视频课程', 'desc': '21天视频号从0到1实战课程，抓住微信视频号红利期。', 'link': 'https://pan.quark.cn/s/22dad9ef0225', 'cat': CAT_SELF_MEDIA},
    {'title': '视频号运营实战课程', 'desc': '视频号运营全攻略，从内容创作到商业变现的完整路径。', 'link': 'https://pan.quark.cn/s/0637528c7bd1', 'cat': CAT_SELF_MEDIA},
    {'title': '公众号运营零基础入门全方位讲解', 'desc': '公众号运营完整教程，从注册到排版到涨粉到变现全覆盖。', 'link': 'https://pan.quark.cn/s/0b22c3599f3b', 'cat': CAT_SELF_MEDIA},
    {'title': '付费群流出写作教程【16合集】', 'desc': '16套写作教程合集，提升文案能力，打造爆款内容。', 'link': 'https://pan.quark.cn/s/0177baad81d4', 'cat': CAT_SELF_MEDIA},
    {'title': '《从流量到留量：让你的产品实现低成本持续增长》', 'desc': '流量运营核心方法论，教你低成本获取并留住用户。', 'link': 'https://pan.quark.cn/s/7bf2401503bd', 'cat': CAT_SELF_MEDIA},
    {'title': '生财有术上千条付费资源合集', 'desc': '生财有术社群精华资源，上千条付费内容合集，搞钱必备。', 'link': 'https://pan.quark.cn/s/5cb9b0429874', 'cat': CAT_SELF_MEDIA},
    
    # 跨境电商
    {'title': '电商课程·拼多多运营必听10节课', 'desc': '拼多多运营核心课程，10节课掌握店铺运营技巧。', 'link': 'https://pan.quark.cn/s/b486d9d3c3d7', 'cat': CAT_CROSS},
    {'title': '跨境电商实操课程从零到精通', 'desc': '人人都适合的跨境电商课，从零基础到精通的完整路径。', 'link': 'https://pan.quark.cn/s/d09808093993', 'cat': CAT_CROSS},
    {'title': '阿里巴巴国际站课程', 'desc': '阿里巴巴国际站运营基础课程，B2B外贸入门必学。', 'link': 'https://pan.quark.cn/s/9f32d229f7f0', 'cat': CAT_CROSS},
    {'title': '外贸线上实战训练营', 'desc': '外贸实战培训，从获客到成交的完整流程。', 'link': 'https://pan.quark.cn/s/b6782807e7da', 'cat': CAT_CROSS},
    
    # 教育资源 - 考证
    {'title': '2025一建二建全科各机构最新网课', 'desc': '2025年一建二建全科备考资料，各机构最新课程合集。', 'link': 'https://pan.quark.cn/s/349bbce69e86', 'cat': CAT_EDU},
    {'title': '销售营销学顶级精英教学视频课程【18套】', 'desc': '18套销售营销课程，顶级销售精英的实战经验分享。', 'link': 'https://pan.quark.cn/s/749dd7db6608', 'cat': CAT_EDU},
    {'title': '孩子必听的100个历史故事【完结】', 'desc': '100个精选历史故事，培养孩子历史兴趣和人文素养。', 'link': 'https://pan.quark.cn/s/260d646d91d5', 'cat': CAT_EDU},
    {'title': '孕期全攻略【完结】', 'desc': '孕期必备知识全攻略，从备孕到生产的完整指南。', 'link': 'https://pan.quark.cn/s/1de29234509d', 'cat': CAT_EDU},
    {'title': '全球外语26门小语种零基础全套学习资料', 'desc': '26门小语种学习资料，日语韩语法语德语等全覆盖。', 'link': 'https://pan.quark.cn/s/f67180336b4e', 'cat': CAT_EDU},
    {'title': '雪梨老师学英语全套【80GB】', 'desc': '自然拼读+音标课+语法课+新概念全套，英语学习必备。', 'link': 'https://pan.quark.cn/s/37db7af0aad7', 'cat': CAT_EDU},
    {'title': '鬼谷子的心理学诡计', 'desc': '章岩著作，教你读懂人心，掌握处世智慧。', 'link': 'https://pan.quark.cn/s/fd1d8a5e21a9', 'cat': CAT_EDU},
    {'title': '最新版公考面试课程', 'desc': '公务员考试面试技巧课程，助你顺利上岸。', 'link': 'https://pan.quark.cn/s/ba2cb4ccc858', 'cat': CAT_EDU},
    {'title': '十三天快速通关高中历史', 'desc': '高中历史快速复习课程，13天掌握核心考点。', 'link': 'https://pan.quark.cn/s/9618fa92528a', 'cat': CAT_EDU},
    {'title': '超级记忆力训练课程【16天】', 'desc': '16天记忆力训练，掌握记忆宫殿等核心技巧。', 'link': 'https://pan.quark.cn/s/00fa9188dd84', 'cat': CAT_EDU},
    {'title': '国考公考省考资料合辑【2024-2025】', 'desc': '2024-2025年公考资料大全，行测申论全覆盖。', 'link': 'https://pan.quark.cn/s/3ff435f62136', 'cat': CAT_EDU},
    {'title': '2025考研英语词汇闪过【10本】', 'desc': '考研英语词汇闪过系列，10本电子书合集。', 'link': 'https://pan.quark.cn/s/1e01ab58bdaf', 'cat': CAT_EDU},
    {'title': '2025年7节课搞定国考常识', 'desc': '国考常识判断速成课程，7节课掌握高频考点。', 'link': 'https://pan.quark.cn/s/d5ed5281d50c', 'cat': CAT_EDU},
    {'title': '初中各科知识点梳理', 'desc': '初中全科知识点整理，复习备考必备资料。', 'link': 'https://pan.quark.cn/s/74153e93c83e', 'cat': CAT_EDU},
    {'title': '高中教辅资源汇总合集', 'desc': '高中各科教辅资料合集，涵盖各科目各版本。', 'link': 'https://pan.quark.cn/s/4807ab495ed8', 'cat': CAT_EDU},
    {'title': '雅思旗舰VIP直达7分班', 'desc': '雅思7分课程，听说读写全科备考资料。', 'link': 'https://pan.quark.cn/s/4d63fc4a67d1', 'cat': CAT_EDU},
    {'title': '2025年考研复试必备资料', 'desc': '复试流程+英语+专业课，考研复试通关必备。', 'link': 'https://pan.quark.cn/s/6f91441b54ef', 'cat': CAT_EDU},
    {'title': '初中九科学霸笔记【无水印】', 'desc': '学霸整理的初中九科笔记，知识点清晰易理解。', 'link': 'https://pan.quark.cn/s/79183bb66cc5', 'cat': CAT_EDU},
    {'title': '初级社工教材【2025年】', 'desc': '2025年初级社会工作者考试教材，备考必备。', 'link': 'https://pan.quark.cn/s/9de8457192dc', 'cat': CAT_EDU},
    {'title': '中级社工教材【2025年】', 'desc': '2025年中级社会工作者考试教材，备考必备。', 'link': 'https://pan.quark.cn/s/7f8f7bf7076d', 'cat': CAT_EDU},
    {'title': '法考资料【2025年】', 'desc': '2025年司法考试备考资料，法考通关必备。', 'link': 'https://pan.quark.cn/s/25eaee3c01c2', 'cat': CAT_EDU},
    {'title': '乔伯伯5500词汇系统英语课【127节】', 'desc': '系统学习5500词汇，127节课程全面覆盖。', 'link': 'https://pan.quark.cn/s/fe1f2edbbb28', 'cat': CAT_EDU},
    {'title': '2025自考+专升本+学位英语合集', 'desc': '自考、专升本、学位英语备考资料合集。', 'link': 'https://pan.quark.cn/s/cf39d8b82e38', 'cat': CAT_EDU},
    {'title': '985学霸逆袭学习方法+提分经验', 'desc': '学霸学习方法论，教你高效学习快速提分。', 'link': 'https://pan.quark.cn/s/6c1fc54308ad', 'cat': CAT_EDU},
    {'title': '高考能力提升卷', 'desc': '高考冲刺提分试卷，刷题必备资料。', 'link': 'https://pan.quark.cn/s/873a9bb68de4', 'cat': CAT_EDU},
    {'title': '相命学课程全集', 'desc': '传统相命学课程合集，了解传统文化。', 'link': 'https://pan.quark.cn/s/6df1ce12f8c3', 'cat': CAT_EDU},
    {'title': '考神大牛韩语零基础0-TOPIK4全程班', 'desc': '韩语零基础到TOPIK4级全程课程，系统学习韩语。', 'link': 'https://pan.quark.cn/s/9fdfb7c2b17e', 'cat': CAT_EDU},
    {'title': '启蒙英语动画', 'desc': '儿童英语启蒙动画合集，寓教于乐学英语。', 'link': 'https://pan.quark.cn/s/58476c46e35e', 'cat': CAT_EDU},
    {'title': '可打印教育资源合集', 'desc': '可打印的学习资料合集，方便孩子学习使用。', 'link': 'https://pan.quark.cn/s/9d3a3de94c1d', 'cat': CAT_EDU},
    
    # 工具合集 - 个人技能
    {'title': '各种酿酒教程合集', 'desc': '各类酒品酿造教程，家庭酿酒从小白到精通。', 'link': 'https://pan.quark.cn/s/73e248320385', 'cat': CAT_TOOL},
    {'title': '八十种各种快餐类美食做法技术大全', 'desc': '80种快餐美食做法，开小吃店必备技术。', 'link': 'https://pan.quark.cn/s/416411e8cb11', 'cat': CAT_TOOL},
    {'title': '笔记本电脑维修完全手册', 'desc': '笔记本维修技术手册，硬件故障诊断与维修。', 'link': 'https://pan.quark.cn/s/0b28a167e109', 'cat': CAT_TOOL},
    {'title': '美食实体店配方【合集】', 'desc': '实体店餐饮配方合集，价值上万的商业配方。', 'link': 'https://pan.quark.cn/s/5b7444819477', 'cat': CAT_TOOL},
    {'title': '99套小吃配方+创业落地指南', 'desc': '99种小吃配方+创业指导，摆摊开店必备。', 'link': 'https://pan.quark.cn/s/1866e2ec8103', 'cat': CAT_TOOL},
    {'title': '美食实体店配方专题【价值上万】', 'desc': '实体店配方精选，商业级配方分享。', 'link': 'https://pan.quark.cn/s/e8d828090e8f', 'cat': CAT_TOOL},
    {'title': '30多套小吃技术全套视频教程合集', 'desc': '30+小吃技术视频教程，学完即可开店。', 'link': 'https://pan.quark.cn/s/2153af3ea584', 'cat': CAT_TOOL},
    {'title': '手办制作视频教程', 'desc': '手办制作技术教学，从零开始学手办制作。', 'link': 'https://pan.quark.cn/s/f26e42bd23ca', 'cat': CAT_TOOL},
    {'title': '超详细生存指南', 'desc': '户外生存技能指南，紧急情况应对手册。', 'link': 'https://pan.quark.cn/s/e82d53c5a7ef', 'cat': CAT_TOOL},
    {'title': '编绳手工坊：编绳基础结法', 'desc': '编绳基础教学，各种结法图解教程。', 'link': 'https://pan.quark.cn/s/aba89bae4edb', 'cat': CAT_TOOL},
    {'title': '零基础钩针教程【视频+PDF】', 'desc': '钩针编织入门教程，视频+图文教学。', 'link': 'https://pan.quark.cn/s/bfd2acf4b881', 'cat': CAT_TOOL},
    {'title': '麻将学技术训练与技巧【完结】', 'desc': '麻将技巧教学，提升牌技的实战指南。', 'link': 'https://pan.quark.cn/s/de4f133a1549', 'cat': CAT_TOOL},
    {'title': '厨师长教你做菜系列合集【71GB】', 'desc': '专业厨师做菜教学，71GB视频教程合集。', 'link': 'https://pan.quark.cn/s/8363225a0eed', 'cat': CAT_TOOL},
    {'title': '精品凉拌菜系列热卤系列课程', 'desc': '凉拌菜+热卤制作技术，餐饮创业者必备。', 'link': 'https://pan.quark.cn/s/e91162128386', 'cat': CAT_TOOL},
    {'title': '饭店常点的35套菜详细视频教学', 'desc': '35道饭店热门菜品教学，学会做大厨。', 'link': 'https://pan.quark.cn/s/83a2aface3a4', 'cat': CAT_TOOL},
    {'title': '招牌菜36套教学视频', 'desc': '36道招牌菜教学，人人变大厨系列。', 'link': 'https://pan.quark.cn/s/c5cf90a62b23', 'cat': CAT_TOOL},
    {'title': '摄影超全付费课程合集【335GB】', 'desc': '335GB摄影课程合集，从入门到精通全覆盖。', 'link': 'https://pan.quark.cn/s/d24f483a8390', 'cat': CAT_TOOL},
    {'title': '创业资料小吃美食教程【522道美食】', 'desc': '522道美食教程，价值几万的创业资料。', 'link': 'https://pan.quark.cn/s/2cc0a730c8d4', 'cat': CAT_TOOL},
    {'title': '国宴大师教做菜【120道菜合集】', 'desc': '国宴大师亲授，120道经典菜品教程。', 'link': 'https://pan.quark.cn/s/d9177079608f', 'cat': CAT_TOOL},
    {'title': '普通人翻身逆袭指南50讲', 'desc': '建立认知和赚钱的完整体系，翻身必学。', 'link': 'https://pan.quark.cn/s/9a4c600af5de', 'cat': CAT_EDU},
    {'title': '花束花艺教程', 'desc': '花艺制作教程，花束设计与包装技巧。', 'link': 'https://pan.quark.cn/s/f03e2660a537', 'cat': CAT_TOOL},
    {'title': '汽车新能源汽车三电实战维修【106节】', 'desc': '新能源汽车维修技术，三电系统实战教学。', 'link': 'https://pan.quark.cn/s/c4c14e2d4eed', 'cat': CAT_TOOL},
    {'title': '民谣吉他课程入门+进阶【139集】', 'desc': '吉他入门到进阶139集，系统学习民谣吉他。', 'link': 'https://pan.quark.cn/s/d2d214209334', 'cat': CAT_TOOL},
    {'title': '小白一学就会的短视频剪辑课', 'desc': '短视频剪辑入门课程，小白也能快速上手。', 'link': 'https://pan.quark.cn/s/bc481341f362', 'cat': CAT_SELF_MEDIA},
    {'title': '制作超有爱迷你宠物玩法', 'desc': '1张图涨粉1W的宠物内容制作教程，多元化变现。', 'link': 'https://pan.quark.cn/s/34e5cfb0c69c', 'cat': CAT_SELF_MEDIA},
    {'title': '职场办公技能总教程', 'desc': '职场办公软件技能大全，提升工作效率。', 'link': 'https://pan.quark.cn/s/329d2145d56d', 'cat': CAT_TOOL},
    {'title': 'PS教程初、中、高合集', 'desc': 'Photoshop教程合集，从入门到精通全覆盖。', 'link': 'https://pan.quark.cn/s/8db083799b67', 'cat': CAT_TOOL},
    {'title': '用搜索提升收入，掌握最热门的职场技能', 'desc': '搜索技能提升课程，职场必备核心能力。', 'link': 'https://pan.quark.cn/s/a9939f39515f', 'cat': CAT_TOOL},
    {'title': '龙舌兰放克iPad基础人物插画课程', 'desc': 'iPad人物插画课程，数字绘画入门教学。', 'link': 'https://pan.quark.cn/s/e30142534809', 'cat': CAT_TOOL},
    {'title': 'Blender3.0零基础快速入门课程', 'desc': 'Blender 3D建模入门教程，零基础快速上手。', 'link': 'https://pan.quark.cn/s/84812fc41aac', 'cat': CAT_TOOL},
    {'title': 'office教程和office模板合集', 'desc': 'Office软件教程+模板素材，办公必备。', 'link': 'https://pan.quark.cn/s/965b309d3a40', 'cat': CAT_TOOL},
    {'title': '职场102项技能课程合集', 'desc': '102项职场技能课程，全面提升职业能力。', 'link': 'https://pan.quark.cn/s/2d934cc344c9', 'cat': CAT_TOOL},
    {'title': '沙雕动画制作教学课程', 'desc': '0基础从文案配音到素材制作，沙雕动画全流程。', 'link': 'https://pan.quark.cn/s/819283319088', 'cat': CAT_SELF_MEDIA},
    {'title': '付费声乐技巧唱歌技巧乐理课程合集', 'desc': '全网最全声乐课程，唱歌技巧+视唱练耳。', 'link': 'https://pan.quark.cn/s/1fcd03215800', 'cat': CAT_TOOL},
    {'title': 'Pr速成3小时学会视频剪辑', 'desc': 'Premiere速成课程，3小时快速上手视频剪辑。', 'link': 'https://pan.quark.cn/s/3f552246e46b', 'cat': CAT_TOOL},
    {'title': 'StableDiffusion零基础入门课', 'desc': 'AI绘画入门教程，零基础学会Stable Diffusion。', 'link': 'https://pan.quark.cn/s/ae7ba4bd1999', 'cat': CAT_TOOL},
    {'title': '摄影剪辑教程大合集', 'desc': '摄影+剪辑教程合集，从拍摄到后期全覆盖。', 'link': 'https://pan.quark.cn/s/e8d651ec735d', 'cat': CAT_TOOL},
    {'title': '大万万老师PS功能精通课', 'desc': 'PS功能详解课程，系统掌握Photoshop。', 'link': 'https://pan.quark.cn/s/df4f8acc5070', 'cat': CAT_TOOL},
    {'title': '短剧剪辑解说课实操班【29节】', 'desc': '短剧剪辑解说实战课程，29节实操教学。', 'link': 'https://pan.quark.cn/s/eea2c124596b', 'cat': CAT_SELF_MEDIA},
    {'title': '谷歌优化师部落GoogleSEO零基础入门教程', 'desc': 'Google SEO入门课程，搜索引擎优化必学。', 'link': 'https://pan.quark.cn/s/afdf5a0a2b2c', 'cat': CAT_CROSS},
    {'title': '少儿编程scratch3.0全套课程【214节】', 'desc': 'Scratch编程全套课程，儿童编程启蒙必备。', 'link': 'https://pan.quark.cn/s/8969377e00eb', 'cat': CAT_EDU},
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
    post_name = f"resource-{i+1}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
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
