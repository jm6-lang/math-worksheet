import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Create custom CSS file for GeneratePress theme to match jichuanglm.cn style
css_content = '''
/* Custom CSS for GeneratePress - Matching jichuanglm.cn style */

/* Header */
.site-header {
    background: #fff;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.main-navigation {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.main-nav ul li a {
    color: #fff;
    font-weight: 500;
}

.main-nav ul li a:hover {
    background: rgba(255,255,255,0.1);
}

/* Hero/Banner Section */
.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 60px 20px;
    text-align: center;
    color: #fff;
    margin-bottom: 30px;
}

.hero-section h1 {
    font-size: 2.5em;
    margin-bottom: 15px;
}

.hero-section p {
    font-size: 1.2em;
    opacity: 0.9;
}

/* Search Box */
.search-box {
    background: #fff;
    border-radius: 50px;
    padding: 15px 25px;
    max-width: 600px;
    margin: 20px auto;
    box-shadow: 0 5px 30px rgba(0,0,0,0.2);
}

.search-box input {
    border: none;
    outline: none;
    font-size: 16px;
    width: calc(100% - 50px);
}

.search-box button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    color: #fff;
    padding: 10px 20px;
    border-radius: 25px;
    cursor: pointer;
}

/* Category Icons */
.category-section {
    display: flex;
    justify-content: center;
    gap: 20px;
    padding: 30px 20px;
    background: #f8f9fa;
}

.category-item {
    text-align: center;
    padding: 20px;
    background: #fff;
    border-radius: 10px;
    width: 120px;
    transition: transform 0.3s, box-shadow 0.3s;
}

.category-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
}

.category-item i {
    font-size: 2em;
    color: #667eea;
}

.category-item span {
    display: block;
    margin-top: 10px;
    font-size: 14px;
}

/* Article List - Card Style */
.posts-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    padding: 20px;
}

.post-card {
    background: #fff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    transition: transform 0.3s, box-shadow 0.3s;
}

.post-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}

.post-card .thumbnail {
    position: relative;
    padding-top: 60%;
    overflow: hidden;
}

.post-card .thumbnail img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s;
}

.post-card:hover .thumbnail img {
    transform: scale(1.05);
}

.post-card .content {
    padding: 15px;
}

.post-card h2 {
    font-size: 16px;
    margin: 0 0 10px;
    line-height: 1.4;
}

.post-card h2 a {
    color: #333;
    text-decoration: none;
}

.post-card h2 a:hover {
    color: #667eea;
}

.post-card .meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 12px;
    color: #999;
}

.post-card .tag {
    display: inline-block;
    padding: 3px 10px;
    background: #f0f0f0;
    border-radius: 15px;
    font-size: 12px;
    color: #667eea;
}

/* VIP Button */
.vip-button {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: #fff;
    padding: 10px 20px;
    border-radius: 25px;
    text-decoration: none;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}

.vip-button:hover {
    opacity: 0.9;
}

/* Footer */
.site-footer {
    background: #1a1a2e;
    color: #fff;
    padding: 40px 20px;
    text-align: center;
}

.site-footer a {
    color: #667eea;
}

/* Responsive */
@media (max-width: 768px) {
    .category-section {
        flex-wrap: wrap;
    }

    .posts-list {
        grid-template-columns: 1fr;
    }
}
'''

# Write CSS to WordPress theme directory
stdin, out, err = c.exec_command(f'cat > /www/wwwroot/skillxm.cn/public/wp-content/themes/generatepress/custom.css << \'CSSEOF\'\n{css_content}\nCSSEOF')
print(out.read().decode())

# Add custom CSS to theme
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp option update generatepress_settings --allow-root 2>&1')
print(out.read().decode()[:200])

c.close()
print("Custom CSS added!")