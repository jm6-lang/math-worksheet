import paramiko
import random

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Sample posts data
posts = [
    {
        'title': '手机短视频剪辑赚钱攻略 - 每天2小时月入3000+',
        'content': '短视频剪辑是目前最火的副业项目之一。本教程详细讲解如何通过手机剪辑短视频赚钱，包括剪辑技巧、素材获取、平台选择等完整流程。',
        'category': 11,  # fuye
        'tags': '短视频,剪辑,副业,赚钱'
    },
    {
        'title': '闲鱼无货源开店教程 - 小白也能月入5000',
        'content': '闲鱼无货源模式是目前门槛最低的电商创业项目。本教程从选品、上架、客服、售后全方位讲解，帮助你快速上手闲鱼赚钱。',
        'category': 11,  # fuye
        'tags': '闲鱼,无货源,电商,副业'
    },
    {
        'title': 'AI写作变现项目 - 利用ChatGPT日入200+',
        'content': '利用AI工具进行内容创作变现，是目前最热门的网赚项目。本教程教你如何使用ChatGPT等AI工具进行文案创作、文章代写、自媒体运营等变现方式。',
        'category': 13,  # wangzhuan
        'tags': 'AI,ChatGPT,写作,变现'
    },
    {
        'title': '小红书带货赚钱攻略 - 从0到月入过万',
        'content': '小红书是目前最适合个人创业的平台之一。本教程详细讲解小红书账号定位、内容创作、带货技巧、变现方法等完整流程。',
        'category': 14,  # zimeiti
        'tags': '小红书,带货,自媒体,变现'
    },
    {
        'title': '抖音直播带货入门指南 - 新手必看',
        'content': '抖音直播带货是目前最火爆的电商模式。本教程从直播间搭建、产品选择、话术技巧、流量获取等方面全面讲解。',
        'category': 15,  # duanshipin
        'tags': '抖音,直播,带货,电商'
    },
    {
        'title': '私域流量运营全套方案 - 社群变现指南',
        'content': '私域流量是目前最有价值的流量类型。本教程教你如何搭建私域流量池、社群运营、转化变现的完整方法论。',
        'category': 16,  # yingxiao
        'tags': '私域,社群,流量,变现'
    },
]

print("=== Creating sample posts ===")
for i, post in enumerate(posts):
    cmd = f'''cd /www/wwwroot/skillxm.cn/public && wp post create \\
        --post_title="{post['title']}" \\
        --post_content="{post['content']}" \\
        --post_status=publish \\
        --post_category={post['category']} \\
        --tags_input="{post['tags']}" \\
        --allow-root 2>&1'''
    
    stdin, out, err = c.exec_command(cmd)
    result = out.read().decode()
    print(f"Post {i+1}: {result[:50] if result else 'OK'}")

# List posts
print("\n=== Posts created ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp post list --allow-root 2>&1')
print(out.read().decode())

c.close()
print("\nDone!")