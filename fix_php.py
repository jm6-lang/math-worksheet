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

# 查看第130行附近
print('[1] 查看问题行附近...')
content = cmd('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php')
lines = content.split('\n')
for i, line in enumerate(lines[125:140], start=126):
    print(f'{i:3}: {line}')

# 找到并删除未闭合的 <?php /*
print('\n[2] 修复未闭合的注释...')
# 查找所有 <?php /* 和 */ ?>
open_comment = content.count('<?php /*')
close_comment = content.count('*/ ?>')
print(f'  <?php /* 数量: {open_comment}')
print(f'  */ ?> 数量: {close_comment}')

# 如果有不匹配，直接从原始备份恢复，然后重新删除打赏板块
print('\n[3] 从最早备份恢复，重新处理...')

# 检查是否有原始备份
backup_check = cmd('ls -la /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/*.bak* 2>/dev/null')
print(backup_check)

# 看看 sites-available 里是否有原始版本
original = cmd('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php 2>/dev/null | head -5')
print('\n当前文件开头:')
print(original)

# 直接用 sed 删除问题行
print('\n[4] 删除第131行的问题注释...')
cmd("sed -i '131d' /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php")

# 验证
print('\n[5] 验证 PHP 语法...')
print(cmd('php -l /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php'))

# 测试访问
print('\n[6] 测试访问...')
print(cmd('curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1/'))

client.close()
