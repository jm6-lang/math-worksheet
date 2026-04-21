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

print('[1] 检查 home-1.php 中打赏板块是否被正确注释...')
print(cmd('grep -n "Support Us" /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php'))

print('\n[2] 检查是否有 PHP 注释标记...')
content = cmd('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php')

# 检查 support-us-container 前后是否有 PHP 注释
if '<?php /*' in content or '*/ ?>' in content:
    print('[OK] 发现 PHP 注释标记，打赏代码被注释')
else:
    print('[警告] 未发现 PHP 注释标记')

# 显示打赏板块附近的代码（第130-160行）
print('\n[3] 打赏板块附近代码（第128-145行）:')
lines = content.split('\n')
for i, line in enumerate(lines[127:145], start=128):
    print(f'{i:3}: {line}')

# 检查是否有任何"打赏"相关代码未被注释
print('\n[4] 检查未被注释的打赏相关代码...')
# 查找不在注释中的打赏关键词
import re
# 简单检查：如果 support-us-container 在 <?php /* 之后，*/ ?> 之前，就是被注释的
support_idx = content.find('support-us-container')
if support_idx > 0:
    before = content[:support_idx]
    after = content[support_idx:]
    php_comment_start = before.rfind('<?php /*')
    php_comment_end_before = before.rfind('*/ ?>')
    
    if php_comment_start > php_comment_end_before:
        print('[OK] support-us-container 在 PHP 注释块内')
    else:
        print('[警告] support-us-container 可能未被正确注释')

print('\n[5] 最终确认 - 搜索所有打赏关键词在源文件中的位置...')
for kw in ['打赏', 'donate', 'support-us', '微信扫码', '支付宝扫码', 'PayPal']:
    result = cmd(f"grep -n '{kw}' /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php 2>/dev/null | head -3")
    if result.strip():
        print(f'  [{kw}]:')
        print('    ' + result.strip().replace('\n', '\n    '))
    else:
        print(f'  [{kw}]: 未找到')

client.close()
print('\n[检查完成]')
