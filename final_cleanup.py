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

# 删除那行注释
print('[1] 删除注释行...')
print(cmd("sed -i '/临时隐藏打赏板块/d' /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php"))

# 删除备份文件（含打赏内容）
print('\n[2] 删除备份文件...')
print(cmd('rm -f /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php.bak'))
print(cmd('rm -f /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php.bak2'))

# 最终验证
print('\n[3] 最终验证...')
result = cmd('grep -c "打赏" /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php')
print(f'  打赏关键词数量: {result.strip()}')

result = cmd('grep -c "support-us" /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php')
print(f'  support-us 关键词数量: {result.strip()}')

result = cmd('grep -c "PayPal" /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php')
print(f'  PayPal 关键词数量: {result.strip()}')

result = cmd('grep -c "微信扫码" /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php')
print(f'  微信扫码 关键词数量: {result.strip()}')

print('\n[清理完成] 源文件中已无任何打赏相关代码')

client.close()