import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 更新文章ID 737的内容
cmd = '''cat > /tmp/update_737.sql << 'SQLEND'
UPDATE wp_posts SET post_content = '<!-- 电话号码标记清除 -->
<h2>📱 号码标记免费查询</h2>
<p>防止号码被恶意标记，导致被系统拦截，电话打不进，影响办事效率。</p>

<p style="color: #e74c3c; font-weight: bold; font-size: 18px;">⚠️ 标记越多拦截率越高 ⚠️</p>

<div style="text-align: center; margin: 20px 0;">
    👇👇👇👇👇
</div>

<h3>⭐️ 使用必读 ⭐️</h3>
<p>工具为官方网页版，商品拍下后系统会自动发送查询链接，免费查询，如果被标记了，会有详细介绍，并有标记去除功能（非人工手动操作，无需验证码，无需静默），消除是按次收费的，系统会根据号码标记情况自动生成订单，消除订单价格在5-28之间，提交订单后在1-3天内完全清除，清除失败的话系统会自动退款（原路退回）。</p>

<p style="background: #f0f9ff; padding: 15px; border-radius: 8px; border-left: 4px solid #1890ff; margin: 20px 0;">
<strong>网站链接：</strong><br>
<a href="http://xbh5.open10086.com/?authorization=f91029a83a8758aa" target="_blank" style="color: #1890ff; word-break: break-all;">http://xbh5.open10086.com/?authorization=f91029a83a8758aa</a>
</p>

<h3>✅ 功能特点</h3>
<ul>
<li>免费查询号码是否被恶意标注</li>
<li>快速消除标记</li>
<li>无需静默、无需验证码</li>
<li>清除失败自动退款</li>
</ul>

<div style="text-align: center; margin: 30px 0;">
    <img src="https://skillxm.cn/wp-content/uploads/2026/04/wechat_qr_reg_card-1.jpg" alt="添加微信二维码" style="max-width: 250px; width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px;">
    <p style="color: #666; font-size: 14px; margin-top: 10px;">扫码添加微信 · 咨询更多问题</p>
    <p style="color: #e74c3c; font-size: 12px;">添加微信时记得标注"在小二郎资源网获取"</p>
</div>' 
WHERE ID = 737;
SQLEND
mysql -u wp_user -pgMshA29CshK5 wp_skillxm < /tmp/update_737.sql && echo "更新成功"
'''

stdin, stdout, stderr = ssh.exec_command(cmd, timeout=60)
print("=== 更新结果 ===")
print(stdout.read().decode())
err = stderr.read().decode()
if err and 'Using a password' not in err:
    print("错误:", err)

# 清理缓存
cmd2 = 'rm -rf /www/wwwroot/resource_site/wp-content/cache/* 2>/dev/null; echo "缓存已清理"'
stdin, stdout, stderr = ssh.exec_command(cmd2, timeout=30)
print("\n=== 缓存 ===")
print(stdout.read().decode())

# 验证
cmd3 = '''mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "SELECT ID, post_title, LEFT(post_content, 80) FROM wp_posts WHERE ID = 737"'''
stdin, stdout, stderr = ssh.exec_command(cmd3, timeout=30)
print("\n=== 验证 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
print("\n完成")
