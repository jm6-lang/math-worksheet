import paramiko
from datetime import datetime

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

# 更新文章 147 的内容
new_content = '''<p><strong>一份资料，搞定AI从入门到变现的完整路径。</strong></p>

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
<p><strong>夸克网盘：</strong> <a href="https://pan.quark.cn/s/1091f03c9413">https://pan.quark.cn/s/1091f03c9413</a></p>

<blockquote><p>💡 提示：复制链接打开夸克APP即可保存</p></blockquote>

<style>
.comments-area, #comments, .comment-respond { display: none !important; }
</style>
'''

# 转义
content_escaped = new_content.replace("\\", "\\\\").replace("'", "''")
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 更新文章
sql = f"""UPDATE wp_posts SET post_content = '{content_escaped}', post_modified = '{now}', post_modified_gmt = '{now}' WHERE ID = 147;"""
cmd = f"mysql -uwpuser -p'WpPass2024!' wp_skillxm -e \"{sql}\""

stdin, stdout, stderr = ssh.exec_command(cmd)
err = stderr.read().decode()

if err and 'error' in err.lower():
    print(f"Update failed: {err}")
else:
    print("Article 147 updated successfully")

ssh.close()
