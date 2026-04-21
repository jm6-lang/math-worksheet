import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'

# Verify categories first
stdin, stdout, stderr = ssh.exec_command(
    f"wp term list category --allow-root --path={wp} --fields=term_id,name,slug,count --format=table",
    timeout=15
)
out = stdout.read().decode('utf-8', errors='replace').strip()
print("分类列表:")
print(out)
print()

# Clear menu 2 and rebuild
stdin, stdout, stderr = ssh.exec_command(
    f"wp menu item list 2 --allow-root --path={wp} --fields=db_id --format=csv | tail -n +2",
    timeout=10
)
existing = stdout.read().decode('utf-8', errors='replace').strip().split('\n')
existing = [x.strip() for x in existing if x.strip()]

print(f"删除旧菜单项: {len(existing)}个")
for item_id in existing:
    stdin, stdout, stderr = ssh.exec_command(
        f"wp menu item delete {item_id} --allow-root --path={wp}",
        timeout=10
    )

# Add new menu items: 首页 / 教育资源 / 影视娱乐 / 工具合集 / 网赚项目 / 渠道资源
menu_items = [
    ("首页", "https://skillxm.cn/"),
    ("教育资源", "https://skillxm.cn/category/jiaoyu"),
    ("影视娱乐", "https://skillxm.cn/category/yingshi"),
    ("工具合集", "https://skillxm.cn/category/gongju"),
    ("网赚项目", "https://skillxm.cn/category/wangzhuan"),
    ("渠道资源", "https://skillxm.cn/category/qudao"),
]

for title, url in menu_items:
    stdin, stdout, stderr = ssh.exec_command(
        f"wp menu item add-post-type-menu-item 2 --title='{title}' --url='{url}' --allow-root --path={wp}",
        timeout=10
    )
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    print(f"添加 {title}: {out if out else err}")

ssh.close()
print("\n菜单重建完成")
