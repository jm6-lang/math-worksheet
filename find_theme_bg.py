import paramiko

server = '240b:4001:278:8402:0:bd18:bd09:af0d'
port = 22
user = 'root'
password = 'Langlang0.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server, port=port, username=user, password=password,
               timeout=20, allow_agent=False, look_for_keys=False,
               banner_timeout=20, auth_timeout=20)

def cmd(c):
    stdin, stdout, stderr = client.exec_command(c, timeout=30)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# 搜索所有 PHP 文件中的 background 设置
print('[1] 搜索 PHP 中的 background 设置...')
result = cmd('grep -rn "background" /www/wwwroot/resource_site/wp-content/themes/yymarket/*.php 2>/dev/null | grep -v "//" | grep -v "background:#fff\|background:#000\|background:#f\|background: #fff\|background: #000\|background: white\|background: #333\|background:#eee\|background:rgba\|background:rgb\|background: -webkit\|background: -moz\|background: -o\|background: -ms" | head -30')
print(result if result.strip() else '  无匹配')

# 搜索 background-image
print('\n[2] 搜索 background-image...')
result = cmd('grep -rn "background-image" /www/wwwroot/resource_site/wp-content/themes/yymarket/*.php 2>/dev/null')
print(result if result.strip() else '  无')

# 搜索 Autoptimize 缓存 CSS
print('\n[3] Autoptimize 缓存 CSS...')
result = cmd('find /www/wwwroot/resource_site/wp-content/cache -name "*.css" 2>/dev/null | head -5')
print(result)

# 搜索插件 CSS
print('\n[4] 插件目录...')
result = cmd('find /www/wwwroot/resource_site/wp-content/plugins -name "*.css" 2>/dev/null | xargs grep -l "background" 2>/dev/null | head -5')
print(result if result.strip() else '  无')

# 搜索 yythemes 或主题选项中的背景
print('\n[5] 主题 functions.php 中的背景...')
result = cmd('grep -n "background\|bg_color\|bg_image\|footer_bg" /www/wwwroot/resource_site/wp-content/themes/yymarket/functions.php 2>/dev/null | head -20')
print(result if result.strip() else '  无')

# 搜索所有 CSS 文件中的背景
print('\n[6] 所有主题 CSS 文件...')
result = cmd('find /www/wwwroot/resource_site/wp-content/themes/yymarket -name "*.css" -exec grep -l "background-image" {} \; 2>/dev/null')
print(result if result.strip() else '  无')

# 检查 footer.php 的 yy-footer 样式
print('\n[7] footer.php 中的样式...')
result = cmd('grep -n "background\|class.*yy-footer\|style.*footer" /www/wwwroot/resource_site/wp-content/themes/yymarket/footer.php 2>/dev/null | head -10')
print(result)

client.close()
