import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'

# First check what menu locations the yymarket theme registers
cmds = [
    # Check theme registered nav locations
    f"grep -r 'register_nav_menus\\|register_nav_menu' /www/wwwroot/resource_site/wp-content/themes/yymarket/functions.php 2>/dev/null | head -5",
    # Check header template for nav
    f"grep -n 'wp_nav_menu\\|has_nav_menu\\|primary\\|top-bar\\|navbar\\|mobile-nav' /www/wwwroot/resource_site/wp-content/themes/yymarket/header.php 2>/dev/null | head -20",
    # Check all PHP files for nav menu
    f"grep -rn 'wp_nav_menu\\|has_nav_menu' /www/wwwroot/resource_site/wp-content/themes/yymarket/*.php 2>/dev/null | head -20",
    # Check menu items
    f"wp menu list --allow-root --path={wp} --fields=term_id,name,slug,locations --format=csv",
    # List menu items in menu 2
    f"wp menu item list 2 --allow-root --path={wp} --fields=db_id,menu_item_parent,title,object,type --format=csv | head -20",
    # List menu items in menu 52
    f"wp menu item list 52 --allow-root --path={wp} --fields=db_id,menu_item_parent,title,object,type --format=csv | head -20",
]

for c in cmds:
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    print(f">>> {c[:80]}")
    print(out[:600] if out else (err[:200] if err else '(empty)'))
    print("---")

ssh.close()
