import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

print("=== 修复用户中心跳转问题 ===\n")

# 1. 创建前端用户中心页面模板
user_center_page = '''<?php
/**
 * Template Name: 用户中心
 */

get_header();
?>

<div class="user-center-container" style="max-width: 1200px; margin: 40px auto; padding: 0 20px;">
    <div class="user-center-header" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; padding: 40px; margin-bottom: 30px; color: white;">
        <h1 style="margin: 0 0 10px 0; font-size: 28px;">用户中心</h1>
        <p style="margin: 0; opacity: 0.9;">管理您的账户和会员信息</p>
    </div>
    
    <div class="user-center-content" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
        
        <?php if (is_user_logged_in()) : ?>
            <?php $current_user = wp_get_current_user(); ?>
            
            <div class="user-card" style="background: white; border-radius: 16px; padding: 30px; box-shadow: 0 2px 12px rgba(0,0,0,0.08);">
                <div class="user-avatar" style="width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; color: white; font-size: 32px; margin-bottom: 20px;">
                    <?php echo mb_substr($current_user->display_name, 0, 1); ?>
                </div>
                <h3 style="margin: 0 0 10px 0; font-size: 20px; color: #1f2937;"><?php echo esc_html($current_user->display_name); ?></h3>
                <p style="margin: 0; color: #6b7280; font-size: 14px;"><?php echo esc_html($current_user->user_email); ?></p>
                <div style="margin-top: 20px;">
                    <a href="<?php echo wp_logout_url(home_url()); ?>" style="display: inline-block; padding: 10px 24px; background: #ef4444; color: white; border-radius: 8px; text-decoration: none; font-size: 14px;">退出登录</a>
                </div>
            </div>
            
            <div class="vip-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 16px; padding: 30px; color: white;">
                <div style="font-size: 14px; opacity: 0.9; margin-bottom: 10px;">会员状态</div>
                <h3 style="margin: 0 0 20px 0; font-size: 24px;">普通会员</h3>
                <a href="#" style="display: inline-block; padding: 12px 30px; background: white; color: #f5576c; border-radius: 50px; text-decoration: none; font-weight: 600;">升级VIP会员</a>
            </div>
            
        <?php else : ?>
            
            <div class="auth-card" style="background: white; border-radius: 16px; padding: 40px; box-shadow: 0 2px 12px rgba(0,0,0,0.08);">
                <h3 style="margin: 0 0 30px 0; font-size: 24px; text-align: center; color: #1f2937;">欢迎回来</h3>
                <?php echo do_shortcode('[pms-login]'); ?>
                <div style="text-align: center; margin-top: 20px;">
                    <p style="color: #6b7280; font-size: 14px;">还没有账号？<a href="#" style="color: #6366f1; text-decoration: none;">立即注册</a></p>
                </div>
            </div>
            
            <div class="vip-intro" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 16px; padding: 40px; color: white;">
                <h3 style="margin: 0 0 20px 0; font-size: 24px;">成为VIP会员</h3>
                <ul style="list-style: none; padding: 0; margin: 0 0 30px 0;">
                    <li style="padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.2);">无限制查看所有资源</li>
                    <li style="padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.2);">专属VIP下载通道</li>
                    <li style="padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.2);">新资源第一时间通知</li>
                    <li style="padding: 10px 0;">专属客服支持</li>
                </ul>
                <a href="#" style="display: inline-block; padding: 15px 40px; background: white; color: #6366f1; border-radius: 50px; text-decoration: none; font-weight: 600;">立即开通</a>
            </div>
            
        <?php endif; ?>
        
    </div>
</div>

<style>
.user-center-container input[type="text"],
.user-center-container input[type="password"],
.user-center-container input[type="email"] {
    width: 100%;
    padding: 15px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    font-size: 14px;
    margin-bottom: 15px;
    box-sizing: border-box;
}
.user-center-container input[type="submit"] {
    width: 100%;
    padding: 15px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
}
</style>

<?php get_footer(); ?>
'''

# 写入用户中心模板
sftp = c.open_sftp()
with sftp.file('/www/wwwroot/skillxm.cn/public/wp-content/themes/puock/page-user-center.php', 'w') as f:
    f.write(user_center_page)
print("用户中心模板: 已创建")

# 2. 创建用户中心页面
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp post list --post_type=page --name=user-center --allow-root 2>&1')
result = out.read().decode()

if 'user-center' not in result:
    stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp post create --post_type=page --post_title="用户中心" --post_name="user-center" --post_status=publish --post_content="" --meta_input=\'{"_wp_page_template":"page-user-center.php"}\' --allow-root 2>&1')
    print(f"创建页面: {out.read().decode()[:100]}")
else:
    print("页面已存在")

# 3. 创建禁用后台跳转的PHP代码
disable_code = '''
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
'''

# 使用SFTP追加到functions.php
stdin, out, err = c.exec_command('cat /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php | tail -5')
print(f"functions.php末尾: {out.read().decode()}")

# 直接用shell追加
cmd = '''cat >> /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php << 'EOF'

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
EOF'''

stdin, out, err = c.exec_command(cmd)
print("禁用后台跳转: 已添加")

# 4. 清除缓存
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp cache flush --allow-root 2>&1')
print(f"清除缓存: {out.read().decode()[:50]}")

# 5. 验证页面
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp post list --post_type=page --allow-root 2>&1')
print(f"\n所有页面:\n{out.read().decode()[:500]}")

sftp.close()
c.close()
print("\n修复完成！")