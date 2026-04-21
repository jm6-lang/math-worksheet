import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

print("=== 添加登录/注册/找回密码按钮 ===\n")

sftp = c.open_sftp()

# 读取header.php
with sftp.file('/www/wwwroot/skillxm.cn/public/wp-content/themes/puock/header.php', 'r') as f:
    header = f.read().decode('utf-8', errors='replace')

# 在导航栏右侧（搜索按钮前）插入用户按钮
# 找到 d-none d-lg-block puock-links 这个div，在其后插入用户按钮
user_nav_html = '''
                <div class="d-none d-lg-flex align-items-center puock-user-nav" style="gap:8px;">
                    <?php if (is_user_logged_in()) : ?>
                        <?php $u = wp_get_current_user(); ?>
                        <a href="<?php echo home_url('/user-center/'); ?>" class="puock-user-btn puock-user-avatar" title="用户中心">
                            <span class="avatar-circle"><?php echo mb_substr($u->display_name, 0, 1); ?></span>
                            <span class="user-name"><?php echo esc_html($u->display_name); ?></span>
                        </a>
                        <a href="<?php echo wp_logout_url(home_url()); ?>" class="puock-user-btn puock-logout-btn">退出</a>
                    <?php else : ?>
                        <a href="#" class="puock-user-btn puock-login-btn" onclick="showAuthModal('login');return false;">登录</a>
                        <a href="#" class="puock-user-btn puock-register-btn" onclick="showAuthModal('register');return false;">注册</a>
                    <?php endif; ?>
                </div>'''

# 在 </div>\n                <div class="mobile-menus 之前插入
old_str = '                <div class="mobile-menus d-block d-lg-none'
new_str = user_nav_html + '\n                <div class="mobile-menus d-block d-lg-none'

if old_str in header:
    header = header.replace(old_str, new_str, 1)
    print("已在导航栏插入用户按钮")
else:
    print("未找到插入点，尝试其他位置")

# 在 </header> 前添加登录/注册/找回密码弹窗
auth_modal = '''
    <!-- 登录/注册/找回密码弹窗 -->
    <div id="auth-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; z-index:99999; background:rgba(0,0,0,0.5); backdrop-filter:blur(4px);">
        <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); background:white; border-radius:20px; padding:40px; width:420px; max-width:90vw; box-shadow:0 20px 60px rgba(0,0,0,0.3);">
            
            <!-- 关闭按钮 -->
            <button onclick="closeAuthModal()" style="position:absolute; top:15px; right:20px; background:none; border:none; font-size:24px; cursor:pointer; color:#999; line-height:1;">&times;</button>
            
            <!-- Tab切换 -->
            <div style="display:flex; gap:0; margin-bottom:30px; border-bottom:2px solid #f0f0f0;">
                <button id="tab-login" onclick="switchTab('login')" style="flex:1; padding:12px; background:none; border:none; font-size:16px; font-weight:600; cursor:pointer; color:#6366f1; border-bottom:2px solid #6366f1; margin-bottom:-2px;">登录</button>
                <button id="tab-register" onclick="switchTab('register')" style="flex:1; padding:12px; background:none; border:none; font-size:16px; font-weight:600; cursor:pointer; color:#9ca3af; border-bottom:2px solid transparent; margin-bottom:-2px;">注册</button>
                <button id="tab-forgot" onclick="switchTab('forgot')" style="flex:1; padding:12px; background:none; border:none; font-size:16px; font-weight:600; cursor:pointer; color:#9ca3af; border-bottom:2px solid transparent; margin-bottom:-2px;">找回密码</button>
            </div>
            
            <!-- 登录表单 -->
            <div id="form-login">
                <form method="post" action="<?php echo wp_login_url(home_url('/user-center/')); ?>">
                    <div style="margin-bottom:16px;">
                        <input type="text" name="log" placeholder="用户名或邮箱" required
                            style="width:100%; padding:14px 16px; border:1.5px solid #e5e7eb; border-radius:12px; font-size:15px; box-sizing:border-box; outline:none; transition:border-color 0.2s;"
                            onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#e5e7eb'">
                    </div>
                    <div style="margin-bottom:8px;">
                        <input type="password" name="pwd" placeholder="密码" required
                            style="width:100%; padding:14px 16px; border:1.5px solid #e5e7eb; border-radius:12px; font-size:15px; box-sizing:border-box; outline:none; transition:border-color 0.2s;"
                            onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#e5e7eb'">
                    </div>
                    <div style="text-align:right; margin-bottom:20px;">
                        <a href="#" onclick="switchTab('forgot');return false;" style="color:#6366f1; font-size:13px; text-decoration:none;">忘记密码？</a>
                    </div>
                    <input type="hidden" name="redirect_to" value="<?php echo home_url('/user-center/'); ?>">
                    <?php wp_nonce_field('login_nonce', 'login_nonce_field'); ?>
                    <button type="submit" style="width:100%; padding:15px; background:linear-gradient(135deg,#667eea,#764ba2); color:white; border:none; border-radius:12px; font-size:16px; font-weight:600; cursor:pointer; letter-spacing:1px;">登 录</button>
                </form>
                <p style="text-align:center; margin-top:20px; color:#9ca3af; font-size:14px;">还没有账号？<a href="#" onclick="switchTab('register');return false;" style="color:#6366f1; text-decoration:none; font-weight:600;">立即注册</a></p>
            </div>
            
            <!-- 注册表单 -->
            <div id="form-register" style="display:none;">
                <form method="post" action="<?php echo site_url('wp-login.php?action=register'); ?>">
                    <div style="margin-bottom:16px;">
                        <input type="text" name="user_login" placeholder="用户名" required
                            style="width:100%; padding:14px 16px; border:1.5px solid #e5e7eb; border-radius:12px; font-size:15px; box-sizing:border-box; outline:none; transition:border-color 0.2s;"
                            onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#e5e7eb'">
                    </div>
                    <div style="margin-bottom:16px;">
                        <input type="email" name="user_email" placeholder="邮箱地址" required
                            style="width:100%; padding:14px 16px; border:1.5px solid #e5e7eb; border-radius:12px; font-size:15px; box-sizing:border-box; outline:none; transition:border-color 0.2s;"
                            onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#e5e7eb'">
                    </div>
                    <input type="hidden" name="redirect_to" value="<?php echo home_url('/user-center/'); ?>">
                    <?php wp_nonce_field('register_nonce', 'register_nonce_field'); ?>
                    <button type="submit" style="width:100%; padding:15px; background:linear-gradient(135deg,#f093fb,#f5576c); color:white; border:none; border-radius:12px; font-size:16px; font-weight:600; cursor:pointer; letter-spacing:1px;">立即注册</button>
                </form>
                <p style="text-align:center; margin-top:20px; color:#9ca3af; font-size:14px;">已有账号？<a href="#" onclick="switchTab('login');return false;" style="color:#6366f1; text-decoration:none; font-weight:600;">立即登录</a></p>
            </div>
            
            <!-- 找回密码表单 -->
            <div id="form-forgot" style="display:none;">
                <p style="color:#6b7280; font-size:14px; margin-bottom:20px; text-align:center;">输入注册邮箱，我们将发送密码重置链接</p>
                <form method="post" action="<?php echo site_url('wp-login.php?action=lostpassword'); ?>">
                    <div style="margin-bottom:20px;">
                        <input type="email" name="user_login" placeholder="注册邮箱" required
                            style="width:100%; padding:14px 16px; border:1.5px solid #e5e7eb; border-radius:12px; font-size:15px; box-sizing:border-box; outline:none; transition:border-color 0.2s;"
                            onfocus="this.style.borderColor='#6366f1'" onblur="this.style.borderColor='#e5e7eb'">
                    </div>
                    <?php wp_nonce_field('retrieve_password', 'wp-forgot-pass-nonce'); ?>
                    <input type="hidden" name="redirect_to" value="">
                    <button type="submit" name="wp-submit" style="width:100%; padding:15px; background:linear-gradient(135deg,#4facfe,#00f2fe); color:white; border:none; border-radius:12px; font-size:16px; font-weight:600; cursor:pointer; letter-spacing:1px;">发送重置邮件</button>
                </form>
                <p style="text-align:center; margin-top:20px; color:#9ca3af; font-size:14px;"><a href="#" onclick="switchTab('login');return false;" style="color:#6366f1; text-decoration:none; font-weight:600;">返回登录</a></p>
            </div>
            
        </div>
    </div>
    
    <script>
    function showAuthModal(tab) {
        document.getElementById('auth-modal').style.display = 'block';
        document.body.style.overflow = 'hidden';
        switchTab(tab || 'login');
    }
    function closeAuthModal() {
        document.getElementById('auth-modal').style.display = 'none';
        document.body.style.overflow = '';
    }
    function switchTab(tab) {
        ['login','register','forgot'].forEach(function(t) {
            document.getElementById('form-' + t).style.display = t === tab ? 'block' : 'none';
            var btn = document.getElementById('tab-' + t);
            if (btn) {
                btn.style.color = t === tab ? '#6366f1' : '#9ca3af';
                btn.style.borderBottomColor = t === tab ? '#6366f1' : 'transparent';
            }
        });
    }
    // 点击遮罩关闭
    document.getElementById('auth-modal').addEventListener('click', function(e) {
        if (e.target === this) closeAuthModal();
    });
    // ESC关闭
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeAuthModal();
    });
    </script>'''

# 在 </header> 后插入弹窗
if '</header>' in header:
    header = header.replace('</header>', '</header>\n' + auth_modal, 1)
    print("已插入登录/注册/找回密码弹窗")
else:
    print("未找到</header>标签")

# 写回文件
with sftp.file('/www/wwwroot/skillxm.cn/public/wp-content/themes/puock/header.php', 'w') as f:
    f.write(header)
print("header.php 已更新")

# 添加导航按钮样式到CSS
nav_css = '''
/* 导航栏用户按钮 */
.puock-user-nav {
    margin-left: 16px;
}
.puock-user-btn {
    display: inline-flex;
    align-items: center;
    padding: 7px 18px;
    border-radius: 50px;
    font-size: 14px;
    font-weight: 500;
    text-decoration: none !important;
    transition: all 0.2s;
    cursor: pointer;
    white-space: nowrap;
}
.puock-login-btn {
    color: #fff !important;
    border: 1.5px solid rgba(255,255,255,0.6);
    background: transparent;
}
.puock-login-btn:hover {
    background: rgba(255,255,255,0.15);
    border-color: #fff;
}
.puock-register-btn {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff !important;
    border: none;
    box-shadow: 0 4px 15px rgba(102,126,234,0.4);
}
.puock-register-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(102,126,234,0.5);
}
.puock-user-avatar {
    color: #fff !important;
    border: 1.5px solid rgba(255,255,255,0.6);
    gap: 8px;
}
.puock-user-avatar:hover {
    background: rgba(255,255,255,0.15);
}
.avatar-circle {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f093fb, #f5576c);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
    color: white;
}
.puock-logout-btn {
    color: rgba(255,255,255,0.7) !important;
    border: 1.5px solid rgba(255,255,255,0.3);
    background: transparent;
    font-size: 13px;
    padding: 6px 14px;
}
.puock-logout-btn:hover {
    color: #fff !important;
    border-color: rgba(255,255,255,0.6);
}
'''

# 读取现有CSS
try:
    with sftp.file('/www/wwwroot/skillxm.cn/public/wp-content/themes/puock/assets/css/custom-style.css', 'r') as f:
        existing_css = f.read().decode('utf-8', errors='replace')
except:
    existing_css = ""

if '.puock-user-btn' not in existing_css:
    with sftp.file('/www/wwwroot/skillxm.cn/public/wp-content/themes/puock/assets/css/custom-style.css', 'w') as f:
        f.write(existing_css + nav_css)
    print("导航按钮CSS已添加")

sftp.close()

# 开启用户注册
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp option update users_can_register 1 --allow-root 2>&1')
print(f"开启用户注册: {out.read().decode()[:50]}")

# 清除缓存
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp cache flush --allow-root 2>&1')
print(f"清除缓存: {out.read().decode()[:50]}")

c.close()
print("\n完成！登录/注册/找回密码按钮已添加到导航栏。")