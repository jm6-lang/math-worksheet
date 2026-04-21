import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Create categories
categories = [
    ('副业项目', 'fuye', '副业赚钱项目资源'),
    ('创业项目', 'chuangye', '创业项目资源'),
    ('网赚项目', 'wangzhuan', '网络赚钱项目'),
    ('自媒体运营', 'zimeiti', '自媒体运营资源'),
    ('短视频运营', 'duanshipin', '短视频运营项目'),
    ('电商运营', 'dianshang', '电商运营资源'),
    ('营销推广', 'yingxiao', '营销推广资源'),
    ('AI工具', 'ai-tools', 'AI工具资源'),
]

print("=== Creating categories ===")
for name, slug, desc in categories:
    stdin, out, err = c.exec_command(f'cd /www/wwwroot/skillxm.cn/public && wp term create category "{name}" --slug={slug} --description="{desc}" --allow-root 2>&1')
    result = out.read().decode()
    print(f'{name}: {result[:50] if result else "OK"}')

# Verify categories
print("\n=== Categories created ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp term list category --allow-root 2>&1')
print(out.read().decode())

c.close()
print("\nDone!")