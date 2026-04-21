import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# 创建自定义 CSS - 完全对标 jichuanglm.cn 的样式
custom_css = '''
/* ========================================
   技能项目网 - 自定义样式
   对标 jichuanglm.cn 布局
   ======================================== */

/* === 全局配色 === */
:root {
    --primary-color: #6366f1;
    --primary-dark: #4f46e5;
    --primary-light: #818cf8;
    --gradient-start: #667eea;
    --gradient-end: #764ba2;
    --card-bg: #ffffff;
    --card-shadow: 0 2px 12px rgba(0,0,0,0.08);
    --text-primary: #1f2937;
    --text-secondary: #6b7280;
    --border-color: #e5e7eb;
}

/* === 顶部导航栏 === */
.navbar, .site-header, #header {
    background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%) !important;
    box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3) !important;
}

.navbar a, .site-header a, #header a,
.navbar .nav-link, .navbar .menu-item a {
    color: #ffffff !important;
    font-weight: 500;
}

.navbar a:hover, .site-header a:hover {
    background: rgba(255,255,255,0.15) !important;
    border-radius: 8px;
}

/* Logo 样式 */
.txt-logo, .site-title, .navbar-brand {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1.5rem !important;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* === Banner/轮播区域 === */
.header-slider-container,
.hero-section,
#carousel {
    background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%) !important;
    padding: 40px 0 !important;
}

/* 搜索框 */
.search-input, .header-slider-search {
    background: rgba(255,255,255,0.95) !important;
    border-radius: 50px !important;
    box-shadow: 0 8px 30px rgba(0,0,0,0.15) !important;
}

.search-input input {
    border: none !important;
    background: transparent !important;
}

.search-input button {
    background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%) !important;
    border-radius: 50px !important;
}

/* === 分类图标区域 === */
.widget-graphic-cover,
.category-section {
    background: #f8fafc !important;
    padding: 30px 0 !important;
}

.graphic, .category-item {
    border-radius: 16px !important;
    overflow: hidden !important;
    transition: all 0.3s ease !important;
    box-shadow: var(--card-shadow) !important;
}

.graphic:hover, .category-item:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 12px 30px rgba(99, 102, 241, 0.2) !important;
}

.graphic img {
    border-radius: 16px !important;
}

/* === 文章卡片样式 === */
.post-item, .post-card, article.card {
    background: var(--card-bg) !important;
    border-radius: 16px !important;
    border: none !important;
    box-shadow: var(--card-shadow) !important;
    transition: all 0.3s ease !important;
    overflow: hidden !important;
}

.post-item:hover, .post-card:hover, article.card:hover {
    transform: translateY(-8px) !important;
    box-shadow: 0 16px 40px rgba(0,0,0,0.12) !important;
}

/* 文章标题 */
.info-title a, .post-title a, .entry-title a {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    line-height: 1.5 !important;
}

.info-title a:hover, .post-title a:hover {
    color: var(--primary-color) !important;
}

/* 文章分类标签 */
.post-tags a, .cat-links a {
    background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%) !important;
    color: #ffffff !important;
    border-radius: 20px !important;
    padding: 4px 12px !important;
    font-size: 12px !important;
}

/* 文章摘要 */
.info-meta p, .post-excerpt, .entry-content p {
    color: var(--text-secondary) !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}

/* === VIP 会员按钮 === */
.vip-button, .payvip-icon, .btn-vip {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
    color: #ffffff !important;
    border-radius: 50px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4) !important;
    transition: all 0.3s ease !important;
}

.vip-button:hover, .payvip-icon:hover, .btn-vip:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(240, 147, 251, 0.5) !important;
}

/* === 侧边栏 === */
.sidebar, .widget-area, #sidebar {
    background: var(--card-bg) !important;
    border-radius: 16px !important;
    box-shadow: var(--card-shadow) !important;
    padding: 20px !important;
}

.widget-title {
    color: var(--primary-color) !important;
    font-weight: 700 !important;
    border-bottom: 2px solid var(--primary-color) !important;
    padding-bottom: 10px !important;
}

/* === 分页 === */
.pagination a, .nav-links a {
    background: var(--card-bg) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

.pagination a:hover, .nav-links a:hover,
.pagination .current, .nav-links .current {
    background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%) !important;
    color: #ffffff !important;
    border-color: transparent !important;
}

/* === 页脚 === */
.site-footer, #footer, footer {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%) !important;
    color: rgba(255,255,255,0.8) !important;
}

.site-footer a, #footer a, footer a {
    color: #a5b4fc !important;
}

.site-footer a:hover, #footer a:hover {
    color: #ffffff !important;
}

/* === 响应式优化 === */
@media (max-width: 768px) {
    .post-item, .post-card, article.card {
        margin-bottom: 16px !important;
    }
    
    .navbar, .site-header, #header {
        padding: 10px 0 !important;
    }
    
    .txt-logo, .site-title, .navbar-brand {
        font-size: 1.2rem !important;
    }
}

/* === 去除多余元素 === */
/* 隐藏英文内容 */
[class*="english"], [class*="English"],
a[href*="home"]:not([href*="/"]),
a[href*="fuye"]:not([href*="/category/"]) {
    display: none !important;
}

/* 优化卡片间距 */
.row.mr-0.ml-0 {
    gap: 20px !important;
}

.post-item {
    padding: 0 !important;
}

.p-block {
    padding: 16px !important;
}
'''

# 写入自定义CSS文件
cmd = f'''cat > /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/assets/css/custom-style.css << 'CSSEOF'
{custom_css}
CSSEOF'''

stdin, out, err = c.exec_command(cmd)
print(f"创建CSS文件: {'OK' if not err.read() else 'Error'}")

# 在主题中引入自定义CSS
inject_cmd = '''
cd /www/wwwroot/skillxm.cn/public && cat >> /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/functions.php << 'PHPEOF'

// 加载自定义样式
function skillxm_custom_styles() {
    wp_enqueue_style('skillxm-custom', get_template_directory_uri() . '/assets/css/custom-style.css', array(), '1.0.0');
}
add_action('wp_enqueue_scripts', 'skillxm_custom_styles', 99);
PHPEOF
'''

stdin, out, err = c.exec_command(inject_cmd)
print(f"注入CSS钩子: {'OK' if not err.read() else 'Error'}")

# 清除缓存
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp cache flush --allow-root 2>&1')
print(f"清除缓存: {out.read().decode()[:50]}")

# 验证CSS文件
stdin, out, err = c.exec_command('ls -la /www/wwwroot/skillxm.cn/public/wp-content/themes/puock/assets/css/custom-style.css')
print(f"CSS文件: {out.read().decode()}")

c.close()
print("\n自定义CSS已添加！")