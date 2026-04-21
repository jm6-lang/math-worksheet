import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

print("=== 创建中文菜单 ===")

# 获取正确的分类ID
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp term list category --fields=term_id,name,slug --allow-root 2>&1')
cats = out.read().decode()
print(f"当前分类:\n{cats}")

# 创建菜单项 - 使用正确的中文分类
menu_items = [
    ('首页', 'https://skillxm.cn'),
    ('副业项目', 'https://skillxm.cn/category/fuye'),
    ('创业项目', 'https://skillxm.cn/category/chuangye'),
    ('网赚项目', 'https://skillxm.cn/category/wangzhuan'),
    ('自媒体运营', 'https://skillxm.cn/category/zimeiti'),
    ('短视频运营', 'https://skillxm.cn/category/duanshipin'),
]

for title, url in menu_items:
    stdin, out, err = c.exec_command(f'cd /www/wwwroot/skillxm.cn/public && wp menu item add-custom 2 "{title}" "{url}" --allow-root 2>&1')
    result = out.read().decode()
    print(f"添加 {title}: {result[:50] if result else 'OK'}")

# 分配菜单位置
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp menu location assign 2 primary --allow-root 2>&1')
print(f"分配菜单位置: {out.read().decode()[:50]}")

# 清除缓存
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp cache flush --allow-root 2>&1')
print(f"清除缓存: {out.read().decode()[:50]}")

c.close()
print("\n菜单创建完成！")