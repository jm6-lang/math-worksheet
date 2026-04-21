import paramiko
from datetime import datetime
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# 文章内容
title = '「AIGC专题资源汇总」人工智能全套教程｜提示词工程+工具实操+变现案例'
category_id = 80  # AI知识
download_link = 'https://pan.quark.cn/s/1091f03c9413'

content = '''<p><strong>一份资料，搞定AI从入门到变现的完整路径。</strong></p>

<h3>📦 资源内容包括：</h3>

<p><strong>🤖 AI工具教程</strong></p>
<ul>
<li>ChatGPT 完整使用指南</li>
<li>Midjourney 绘画从0到精通</li>
<li>Claude、文心一言等国内外AI工具对比评测</li>
<li>AI工具合集+安装包</li>
</ul>

<p><strong>📝 提示词工程</strong></p>
<ul>
<li>1000+ 精选提示词模板</li>
<li>分场景提示词库（写作、编程、翻译、营销）</li>
<li>提示词优化技巧实战课</li>
</ul>

<p><strong>💰 AI变现案例</strong></p>
<ul>
<li>50+ 真实副业变现案例拆解</li>
<li>AI写作变现路径</li>
<li>AI绘画接单教程</li>
<li>AI工具开发变现指南</li>
</ul>

<p><strong>📚 配套资料</strong></p>
<ul>
<li>AI行业研究报告</li>
<li>学习路线图</li>
<li>常见问题解答</li>
</ul>

<h3>👥 适合谁：</h3>
<ul>
<li>想系统学习AI工具的新手</li>
<li>想用AI提升工作效率的打工人</li>
<li>想靠AI技能变现的自由职业者</li>
<li>对AIGC领域感兴趣的创业者</li>
</ul>

<h3>✅ 你将获得：</h3>
<ol>
<li>国内外主流AI工具使用教程</li>
<li>1000+ 可直接复制使用的提示词模板</li>
<li>50+ 真实可复制的变现案例</li>
<li>持续更新的资源库</li>
</ol>

<h3>📥 下载链接：</h3>
<p><strong>夸克网盘：</strong> <a href="''' + download_link + '''">''' + download_link + '''</a></p>

<blockquote><p>💡 提示：建议使用夸克网盘APP扫码保存，速度更快</p></blockquote>
'''

# 转义
title_escaped = title.replace("'", "''")
content_escaped = content.replace("\\", "\\\\").replace("'", "''")

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
post_name = 'aigc-resource-collection'

# 插入文章
sql1 = f"""INSERT INTO wp_posts (
    post_author, post_date, post_date_gmt, post_content, post_title,
    post_excerpt, post_status, comment_status, ping_status,
    post_password, post_name, to_ping, pinged, post_modified,
    post_modified_gmt, post_content_filtered, post_parent, guid,
    menu_order, post_type, post_mime_type, comment_count
) VALUES (
    1, '{now}', '{now}', '{content_escaped}', '{title_escaped}',
    '', 'publish', 'open', 'open',
    '', '{post_name}', '', '', '{now}',
    '{now}', '', 0, '',
    0, 'post', '', 0
);"""

cmd1 = f"mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"{sql1}\""
stdin, stdout, stderr = ssh.exec_command(cmd1)
err = stderr.read().decode()
if err and 'error' in err.lower():
    print(f"插入文章失败: {err}")
    ssh.close()
    exit(1)

# 获取文章ID
cmd2 = "mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"SELECT MAX(ID) as id FROM wp_posts WHERE post_type='post';\""
stdin, stdout, stderr = ssh.exec_command(cmd2)
result = stdout.read().decode()
lines = result.strip().split('\n')
post_id = lines[-1] if len(lines) > 1 else '0'
print(f"文章ID: {post_id}")

# 设置分类
sql3 = f"INSERT INTO wp_term_relationships (object_id, term_taxonomy_id, term_order) VALUES ({post_id}, {category_id}, 0);"
cmd3 = f"mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"{sql3}\""
stdin, stdout, stderr = ssh.exec_command(cmd3)

# 更新分类计数
sql4 = f"UPDATE wp_term_taxonomy SET count = count + 1 WHERE term_id = {category_id};"
cmd4 = f"mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"{sql4}\""
stdin, stdout, stderr = ssh.exec_command(cmd4)

ssh.close()

print(f"\n✅ 发布成功！")
print(f"   查看地址: https://skillxm.cn/?p={post_id}")
