import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

print("=== 优化 Puock 主题配置 ===\n")

# 1. 获取当前配置
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp option get puock_options --format=json --allow-root 2>&1')
config_json = out.read().decode()
print(f"当前配置长度: {len(config_json)}")

# 2. 更新关键配置项
updates = [
    ('puock_index_mode', 'cms'),
    ('puock_post_style', 'card'),
    ('puock_cms_card_columns', '2'),
    ('puock_index_carousel', '1'),
    ('puock_carousel_mode', 'swiper'),
    ('puock_nav_blur', '1'),
    ('puock_show_search_btn', '1'),
    ('puock_show_login_btn', '1'),
    ('puock_enable_seo_meta', '1'),
]

for key, value in updates:
    stdin, out, err = c.exec_command(f'cd /www/wwwroot/skillxm.cn/public && wp option update {key} "{value}" --allow-root 2>&1')
    result = out.read().decode()
    if 'Success' in result:
        print(f"[OK] {key} = {value}")

# 3. 设置轮播图
print("\n=== 配置轮播图 ===")
# 检查是否有轮播图设置
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp option get puock_carousel --allow-root 2>&1')
carousel = out.read().decode()
print(f"轮播配置: {carousel[:100] if carousel else '未设置'}")

# 4. 清除所有缓存
print("\n=== 清除缓存 ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp cache flush --allow-root 2>&1')
print(out.read().decode())

# 5. 检查主题版本
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp theme list --allow-root 2>&1')
print(f"\n主题状态:\n{out.read().decode()}")

c.close()
print("\n配置优化完成！")