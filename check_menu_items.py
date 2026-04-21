import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'

# 查看所有菜单及其项目
cmds = [
    f"wp menu list --allow-root --path={wp} --format=table",
    f"wp menu item list 2 --allow-root --path={wp} --fields=db_id,menu_item_parent,title,url,object,object_id --format=table",
    f"wp menu item list 52 --allow-root --path={wp} --fields=db_id,menu_item_parent,title,url,object,object_id --format=table",
    # 查看所有分类
    f"wp term list category --allow-root --path={wp} --fields=term_id,name,slug --format=table | head -20",
]

for c in cmds:
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    print(f">>> {c[:60]}")
    print(out[:800])
    print()

ssh.close()
