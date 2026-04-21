import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 二维码图片URL
qr_image_url = "https://skillxm.cn/wp-content/uploads/2026/04/wechat_qr_reg_card-1.jpg"

# 新文章内容
new_content = '''<!-- 渠道资源介绍 -->
<div style="text-align: center; margin: 20px 0;">
    <img src="''' + qr_image_url + '''" alt="注册卡采购渠道二维码" style="max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
</div>

<h2>📱 注册卡采购渠道</h2>
<p>欢迎来到小二郎资源网！我们是专业的注册卡采购渠道，为您提供优质、实惠的注册卡产品。</p>

<h3>🌟 我们的优势</h3>
<ul>
<li>✅ 正规渠道，品质保障</li>
<li>✅ 价格实惠，量大从优</li>
<li>✅ 快速发货，售后无忧</li>
<li>✅ 多种面值，满足不同需求</li>
</ul>

<h3>📦 产品类型</h3>
<p>我们提供多种类型的注册卡，适用于各类平台和应用，欢迎咨询了解详情。</p>

<h3>💬 联系方式</h3>
<p style="background: #f5f5f5; padding: 15px; border-radius: 8px; border-left: 4px solid #07c160;">
<strong>扫描上方二维码添加微信</strong><br>
添加微信时，<span style="color: #e74c3c;"><strong>记得标注"在小二郎资源网获取"</strong></span>，我们将为您提供专属优惠！
</p>

<h3>⚠️ 温馨提示</h3>
<p>请认准小二郎资源网官方渠道，谨防假冒。如有疑问，请通过上方二维码联系客服确认。</p>

<div style="text-align: center; margin: 30px 0;">
    <img src="''' + qr_image_url + '''" alt="添加微信二维码" style="max-width: 300px; height: auto; border: 1px solid #ddd; border-radius: 8px;">
    <p style="color: #666; font-size: 14px; margin-top: 10px;">扫码添加微信 · 获取更多优惠</p>
</div>
'''

# 更新文章内容
cmd = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
UPDATE wp_posts SET post_content = %s WHERE ID = 779;
SELECT ID, post_title FROM wp_posts WHERE ID = 779;
" --safe-updates
'''
# 使用Python直接执行SQL
import json
cmd = f'''python3 << 'ENDSCRIPT'
import pymysql
conn = pymysql.connect(host='localhost', user='wp_user', password='gMshA29CshK5', database='wp_skillxm', charset='utf8mb4')
cursor = conn.cursor()

content = """{new_content}"""
cursor.execute("UPDATE wp_posts SET post_content = %s WHERE ID = 7749", (content,))
cursor.execute("UPDATE wp_posts SET post_content = %s WHERE ID = 779", (content,))
conn.commit()

# 确认更新
cursor.execute("SELECT ID, post_title, LEFT(post_content, 200) FROM wp_posts WHERE ID = 779")
row = cursor.fetchone()
print(f"更新成功: ID={row[0]}, 标题={row[1]}")

cursor.close()
conn.close()
ENDSCRIPT'''

# 正确的SQL更新
cmd = f'''python3 -c "
import pymysql
conn = pymysql.connect(host='localhost', user='wp_user', password='gMshA29CshK5', database='wp_skillxm', charset='utf8mb4')
cursor = conn.cursor()
content = '''{new_content}'''
cursor.execute('UPDATE wp_posts SET post_content = %s WHERE ID = 779', (content,))
conn.commit()
print('文章内容已更新')
cursor.execute('SELECT LEFT(post_content, 300) FROM wp_posts WHERE ID = 779')
print('内容预览:', cursor.fetchone()[0][:200])
cursor.close()
conn.close()
"'''

stdin, stdout, stderr = ssh.exec_command(cmd, timeout=60)
print("=== 更新结果 ===")
print(stdout.read().decode('utf-8', errors='ignore'))
err = stderr.read().decode('utf-8', errors='ignore')
if err:
    print("错误:", err)

# 更新特色图片为注册卡专用二维码
cmd2 = f'''mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
UPDATE wp_postmeta SET meta_value = '{qr_image_url}' WHERE post_id = 779 AND meta_key = 'fifu_image_url';
SELECT * FROM wp_postmeta WHERE post_id = 779 AND meta_key = 'fifu_image_url';
"'''
stdin, stdout, stderr = ssh.exec_command(cmd2, timeout=30)
print("\n=== 特色图片 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 清理缓存
cmd3 = 'rm -rf /www/wwwroot/resource_site/wp-content/cache/* 2>/dev/null; echo "缓存已清理"'
stdin, stdout, stderr = ssh.exec_command(cmd3, timeout=30)
print("\n=== 缓存清理 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# 测试访问
cmd4 = "curl -sIL 'https://www.skillxm.cn/?p=779' | head -15"
stdin, stdout, stderr = ssh.exec_command(cmd4, timeout=30)
print("\n=== 测试访问 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
print("\n完成！")
