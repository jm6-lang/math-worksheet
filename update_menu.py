import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Get menu ID
print("=== Getting menu ID ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp menu list --fields=term_id,name --allow-root 2>&1')
print(out.read().decode())

# Delete old menu items and create new ones
print("\n=== Updating menu ===")

# Add menu items
menu_items = [
    ('首页', 'https://skillxm.cn'),
    ('副业项目', 'https://skillxm.cn/category/fuye'),
    ('创业项目', 'https://skillxm.cn/category/chuangye'),
    ('网赚项目', 'https://skillxm.cn/category/wangzhuan'),
    ('AI工具', 'https://skillxm.cn/category/ai-tools'),
    ('关于我们', 'https://skillxm.cn/about'),
]

for title, url in menu_items:
    stdin, out, err = c.exec_command(f'cd /www/wwwroot/skillxm.cn/public && wp menu item add-custom 2 "{title}" "{url}" --allow-root 2>&1')
    result = out.read().decode()
    print(f'{title}: {result[:50] if result else "OK"}')

# Check menu
print("\n=== Menu items ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp menu item list 2 --allow-root 2>&1')
print(out.read().decode()[:500])

c.close()
print("\nDone!")