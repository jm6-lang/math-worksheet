import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

print("=== 添加用户中心功能 ===\n")

# 读取functions.php内容
sftp = c.open_sftp()
with sftp.file('/www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php', 'r') as f:
    content = f.read().decode()

# 检查是否已添加
if 'skillxm_redirect_non_admin' not in content:
    # 添加代码
    new_code = '''

// ===== 技能项目网 - 用户中心功能 =====

// 禁用普通用户访问后台
function skillxm_redirect_non_admin() {
    if (is_admin() && !current_user_can("manage_options") && !(defined("DOING_AJAX") && DOING_AJAX)) {
        wp_redirect(home_url("/user-center/"));
        exit;
    }
}
add_action("admin_init", "skillxm_redirect_non_admin");

// 登录后跳转到用户中心
function skillxm_login_redirect($redirect_to, $request, $user) {
    if (!is_wp_error($user) && !current_user_can("manage_options")) {
        return home_url("/user-center/");
    }
    return $redirect_to;
}
add_filter("login_redirect", "skillxm_login_redirect", 10, 3);

// 移除顶部工具栏后台链接
function skillxm_remove_admin_bar() {
    if (!current_user_can("manage_options")) {
        show_admin_bar(false);
    }
}
add_action("after_setup_theme", "skillxm_remove_admin_bar");
'''
    
    with sftp.file('/www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php', 'w') as f:
        f.write(content + new_code)
    print("已添加用户中心功能代码")
else:
    print("功能代码已存在，跳过")

sftp.close()

# 创建用户中心页面
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp post list --post_type=page --fields=post_name --allow-root 2>&1')
pages = out.read().decode()

if 'user-center' not in pages:
    stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp post create --post_type=page --post_title="用户中心" --post_name="user-center" --post_status=publish --allow-root 2>&1')
    print(f"创建页面: {out.read().decode()[:100]}")
else:
    print("用户中心页面已存在")

# 清除缓存
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp cache flush --allow-root 2>&1')
print(f"清除缓存: {out.read().decode()}")

# 验证用户中心页面
print("\n=== 验证 ===")
stdin, out, err = c.exec_command('curl -s -o /dev/null -w "%{http_code}" https://skillxm.cn/user-center/ 2>&1')
print(f"用户中心页面HTTP状态: {out.read().decode()}")

c.close()
print("\n完成！用户中心已配置，普通用户不会跳转到后台了。")