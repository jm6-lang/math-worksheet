import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Create categories with English slugs first, then rename
categories = [
    ('fuye', '副业项目'),
    ('chuangye', '创业项目'),
    ('wangzhuan', '网赚项目'),
    ('zimeiti', '自媒体运营'),
    ('duanshipin', '短视频运营'),
    ('dianshang', '电商运营'),
    ('yingxiao', '营销推广'),
    ('aitools', 'AI工具'),
]

print("=== Creating categories ===")
for slug, name in categories:
    stdin, out, err = c.exec_command(f'cd /www/wwwroot/skillxm.cn/public && wp term create category {slug} --allow-root 2>&1')
    result = out.read().decode()
    print(f'{slug}: {result[:50] if result else "OK"}')

# List categories
print("\n=== Categories ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp term list category --fields=term_id,name,slug --allow-root 2>&1')
print(out.read().decode())

c.close()
print("\nDone!")