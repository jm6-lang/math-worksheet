import paramiko
import urllib.request
import re

# 连接服务器
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

print("=== 第一步：配置 Puock 主题设置 ===")

# 获取当前主题设置
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp option get puock_options --format=json --allow-root 2>&1')
result = out.read().decode()
print(f"当前设置长度: {len(result)}")

# 更新主题设置 - 配置为与目标站类似的布局
# 目标站特征：
# 1. 紫色渐变主色调
# 2. Banner轮播
# 3. 分类图标导航
# 4. 卡片式文章列表
# 5. VIP会员按钮

# 创建配置数组
config = '''
array (
  'index_mode' => 'cms',
  'post_style' => 'card',
  'style_color_primary' => '#6366f1',
  'cms_card_columns' => 2,
  'cms_show_pagination' => true,
  'cms_show_load_more' => false,
  'cms_show_new' => true,
  'cms_show_new_num' => 12,
  'hide_global_sidebar' => false,
  'nav_blur' => true,
  'index_carousel' => true,
  'carousel_mode' => 'swiper',
  'show_site_description' => true,
  'header_style' => 'center',
  'logo_text' => '技能项目网',
  'site_keywords' => '副业项目,创业项目,网赚项目,搞钱项目,赚钱项目',
  'site_description' => '副业项目、创业项目、网创资源一站式平台',
)
'''

print("\n主题配置准备完成")

# 2. 清理重复菜单和英文内容
print("\n=== 第二步：清理菜单 ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp menu item list 2 --fields=db_id,title --allow-root 2>&1')
menu_items = out.read().decode()
print(f"当前菜单项:\n{menu_items}")

# 删除所有菜单项重新创建
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp menu item delete $(wp menu item list 2 --format=ids --allow-root) --allow-root 2>&1')
result = out.read().decode()
print(f"删除旧菜单: {result[:50] if result else 'OK'}")

# 3. 清理重复分类
print("\n=== 第三步：清理重复分类 ===")
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp term list category --fields=term_id,name,slug --allow-root 2>&1')
cats = out.read().decode()
print(f"当前分类:\n{cats}")

# 删除英文slug的分类（保留中文的）
for cat_id in ['10', '11', '12', '13', '14', '15', '16', '17', '18']:
    stdin, out, err = c.exec_command(f'cd /www/wwwroot/skillxm.cn/public && wp term delete category {cat_id} --allow-root 2>&1')
    result = out.read().decode()
    if 'Deleted' in result or 'Success' in result:
        print(f"删除分类 {cat_id}")

c.close()
print("\n=== 配置准备完成 ===")
print("接下来需要：")
print("1. 更新主题配色为紫色渐变")
print("2. 添加Banner轮播图片")
print("3. 创建正确的中文菜单")
print("4. 优化文章卡片样式")