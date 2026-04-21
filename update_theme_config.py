import paramiko
import json

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

print("=== 更新 Puock 主题配置 ===")

# 更新主题选项 - 使用紫色渐变配色
update_cmd = '''
cd /www/wwwroot/skillxm.cn/public && wp option update puock_options 'a:50:{
s:10:"index_mode";s:3:"cms";
s:10:"post_style";s:4:"card";
s:19:"style_color_primary";s:7:"#6366f1";
s:20:"style_color_gradient";s:7:"#8b5cf6";
s:17:"cms_card_columns";i:2;
s:20:"cms_show_pagination";b:1;
s:19:"cms_show_load_more";b:0;
s:12:"cms_show_new";b:1;
s:16:"cms_show_new_num";i:12;
s:20:"hide_global_sidebar";b:0;
s:9:"nav_blur";b:1;
s:14:"index_carousel";b:1;
s:13:"carousel_mode";s:6:"swiper";
s:21:"show_site_description";b:1;
s:12:"header_style";s:6:"center";
s:12:"navbar_style";s:7:"primary";
s:18:"navbar_sticky_top";b:1;
s:15:"show_search_btn";b:1;
s:15:"show_login_btn";b:1;
s:13:"show_user_btn";b:1;
s:15:"show_dark_mode";b:1;
s:14:"show_read_mode";b:1;
s:20:"enable_post_toc_auto";b:1;
s:16:"enable_post_like";b:1;
s:18:"enable_post_reward";b:0;
s:21:"enable_post_copyright";b:1;
s:19:"enable_post_share";b:1;
s:16:"enable_qrcode";b:0;
s:14:"enable_reward";b:0;
s:11:"footer_info";s:100:"Copyright © 2026 · 技能项目网 · 副业项目、创业项目一站式平台";
s:14:"footer_icp_num";s:20:"";
s:16:"footer_police_num";s:0:"";
s:15:"footer_safe_date";s:10:"2026-04-05";
s:16:"enable_seo_meta";b:1;
s:15:"enable_seo_baidu";b:0;
s:14:"enable_seo_google";b:0;
s:15:"enable_seo_bing";b:0;
s:17:"enable_seo_sitemap";b:1;
s:14:"enable_seo_robots";b:1;
s:15:"seo_keywords_list";s:50:"副业项目,创业项目,网赚项目,搞钱项目";
s:18:"seo_description_val";s:80:"副业项目、创业项目、网创资源一站式平台，每日更新优质项目";
}' --allow-root 2>&1
'''

stdin, out, err = c.exec_command(update_cmd)
result = out.read().decode()
print(f"更新主题配置: {result[:100] if result else 'OK'}")

# 更新站点标题和描述
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp option update blogname "技能项目网" --allow-root 2>&1')
print(f"更新站点名称: {out.read().decode()[:50]}")

stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp option update blogdescription "副业项目、创业项目、网创资源一站式平台" --allow-root 2>&1')
print(f"更新站点描述: {out.read().decode()[:50]}")

# 清除缓存
stdin, out, err = c.exec_command('cd /www/wwwroot/skillxm.cn/public && wp cache flush --allow-root 2>&1')
print(f"清除缓存: {out.read().decode()[:50]}")

c.close()
print("\n主题配置更新完成！")