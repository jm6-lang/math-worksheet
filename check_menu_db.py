import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'

# Get menu items from DB directly
stdin, stdout, stderr = ssh.exec_command(
    f"mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT m.title, m.url FROM wp_posts p JOIN wp_postmeta pm ON p.ID=pm.post_id JOIN wp_posts m ON pm.meta_value=m.ID WHERE p.post_type='nav_menu_item' AND p.post_status='publish' AND pm.meta_key='_menu_item_menu_item_parent' AND pm.meta_value=0 AND m.post_type='nav_menu_item'\"",
    timeout=10
)
out = stdout.read().decode('utf-8', errors='replace').strip()
print("菜单项:")
print(out)

# Also check menu item urls from posts table directly
stdin, stdout, stderr = ssh.exec_command(
    f"mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT post_title, guid FROM wp_posts WHERE post_type='nav_menu_item' AND post_status='publish' ORDER BY ID\"",
    timeout=10
)
out = stdout.read().decode('utf-8', errors='replace').strip()
print("\n所有菜单项:")
print(out)

ssh.close()
