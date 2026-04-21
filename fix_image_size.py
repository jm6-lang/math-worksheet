import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 更新文章内容，图片宽度改为300px
cmd = '''cat > /tmp/update_779.sql << 'SQLEOF'
UPDATE wp_posts SET post_content = '<!-- 渠道资源介绍 -->
<div style="text-align: center; margin: 20px 0;">
    <img src="https://skillxm.cn/wp-content/uploads/2026/04/wechat_qr_reg_card-1.jpg" alt="注册卡采购渠道二维码" style="max-width: 300px; width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
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
    <img src="https://skillxm.cn/wp-content/uploads/2026/04/wechat_qr_reg_card-1.jpg" alt="添加微信二维码" style="max-width: 250px; width: 100%; height: auto; border: 1px solid #ddd; border-radius: 8px;">
    <p style="color: #666; font-size: 14px; margin-top: 10px;">扫码添加微信 · 获取更多优惠</p>
</div>' 
WHERE ID = 779;
SQLEOF
mysql -u wp_user -pgMshA29CshK5 wp_skillxm < /tmp/update_779.sql && echo "更新成功"
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

ssh.close()
print("\n完成 - 图片已改为300px宽")
