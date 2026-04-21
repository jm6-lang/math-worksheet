import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'

# Check actual category slugs
stdin, stdout, stderr = ssh.exec_command(
    f"wp term list category --allow-root --path={wp} --fields=term_id,name,slug --format=csv",
    timeout=10
)
out = stdout.read().decode('utf-8', errors='replace').strip()
print("分类:", out)

# Add menu items using wp menu item add custom
items = [
    ("首页", "https://skillxm.cn/"),
    ("教育资源", "https://skillxm.cn/category/jiaoyu"),
    ("影视娱乐", "https://skillxm.cn/category/yingshi"),
    ("工具合集", "https://skillxm.cn/category/gongju"),
    ("网赚项目", "https://skillxm.cn/category/wangzhuan"),
    ("渠道资源", "https://skillxm.cn/qudao"),
]

for title, url in items:
    stdin, stdout, stderr = ssh.exec_command(
        f"wp menu item add-custom 2 '{title}' '{url}' --allow-root --path={wp}",
        timeout=15
    )
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    print(f"添加 {title}: {'OK' if 'Success' in out or 'Added' in out else out[:50]}")

ssh.close()
print("\n菜单重建完成")
