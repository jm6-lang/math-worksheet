import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

print("=== 清理首页后台链接 ===\n")

# 1. 添加CSS隐藏后台相关元素
hide_admin_css = '''
/* 隐藏后台相关链接 */
a[href*="wp-admin"],
a[href*="wp-login.php"],
.navbar-nav .menu-item:has(a[href*="wp-admin"]) {
    display: none !important;
}

/* 隐藏顶部工具栏 */
#wpadminbar {
    display: none !important;
}
body.admin-bar {
    margin-top: 0 !important;
}
'''

# 读取现有CSS
sftp = c.open_sftp()
try:
    with sftp.file('/www/wwwroot/skillxm.cn/public/wp-content/themes/puock/assets/css/custom-style.css', 'r') as f:
        existing_css = f.read().decode()
except:
    existing_css = ""

# 添加新CSS
if '隐藏后台' not in existing_css:
    with sftp.file('/www/wwwroot/skillxm.cn/public/wp-content/themes/puock/assets/css/custom-style.css', 'w') as f:
        f.write(existing_css + hide_admin_css)
    print("已添加隐藏后台链接的CSS")
else:
    print("CSS已存在")

sftp.close()

# 2. 在functions.php中添加移除后台链接的函数
stdin, out, err = c.exec_command('grep "skillxm_remove_wp_admin" /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php 2>&1')
if 'skillxm_remove_wp_admin' not in out.read().decode():
    cmd = '''cat >> /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php << 'EOF'

// 移除导航中的后台链接
function skillxm_remove_wp_admin_menu($items, $menu) {
    foreach ($items as $key => $item) {
        if (strpos($item->url, 'wp-admin') !== false || strpos($item->url, 'wp-login') !== false) {
            unset($items[$key]);
        }
    }
    return $items;
}
add_filter('wp_get_nav_menu_items', 'skillxm_remove_wp_admin_menu', 10, 2);
EOF'''
    stdin, out, err = c.exec_command(cmd)
    print("已添加移除后台链接函数")
else:
    print("函数已存在")

# 3. 清除缓存
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp cache flush --allow-root 2>&1')
print(f"清除缓存: {out.read().decode()[:50]}")

# 4. 清除浏览器可能的缓存 - 更新CSS版本号
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp option update puock_css_version date("YmdHis") --allow-root 2>&1 || echo "OK"')
print("更新CSS版本号")

c.close()
print("\n完成！后台链接已被隐藏。")