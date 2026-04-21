import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

print("=== 安装会员系统插件 ===\n")

# 1. 检查已安装的会员相关插件
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp plugin list --allow-root 2>&1')
print("已安装插件:")
print(out.read().decode())

# 2. 安装 WooCommerce（会员+支付系统）
print("\n=== 安装 WooCommerce ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp plugin install woocommerce --activate --allow-root 2>&1')
result = out.read().decode()
print(f"WooCommerce: {result[:200]}")

# 3. 安装 Paid Member Subscriptions（会员订阅）
print("\n=== 安装会员订阅插件 ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp plugin install paid-member-subscriptions --activate --allow-root 2>&1')
result = out.read().decode()
print(f"会员订阅: {result[:200]}")

# 4. 清除缓存
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp cache flush --allow-root 2>&1')
print(f"\n清除缓存: {out.read().decode()[:50]}")

# 5. 列出最终插件
print("\n=== 最终插件列表 ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp plugin list --allow-root 2>&1')
print(out.read().decode())

c.close()
print("\n完成！")