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

# 方法1：用 CSS 隐藏（推荐，不改源码）
# 在主题的 Additional CSS 或 style.css 中添加
print('[1] 备份 style.css ...')
print(cmd('cp /www/wwwroot/resource_site/wp-content/themes/yymarket/style.css /www/wwwroot/resource_site/wp-content/themes/yymarket/style.css.bak'))

# 检查 style.css 末尾
print('\n[2] 当前 style.css 末尾 ...')
print(cmd('tail -10 /www/wwwroot/resource_site/wp-content/themes/yymarket/style.css'))

# 追加隐藏规则
print('\n[3] 添加隐藏打赏板块的 CSS ...')
hide_css = '''
/* 隐藏打赏板块 - 临时隐藏用于 AdSense 审核 */
.support-us-container {
    display: none !important;
}
'''
cmd('echo "' + hide_css.replace('\n', '\\n') + '" >> /www/wwwroot/resource_site/wp-content/themes/yymarket/style.css')

# 验证
print('\n[4] 验证 CSS 已添加 ...')
print(cmd('tail -10 /www/wwwroot/resource_site/wp-content/themes/yymarket/style.css'))

# 清理缓存（如果有缓存插件）
print('\n[5] 清理可能的缓存 ...')
print(cmd('rm -rf /www/wwwroot/resource_site/wp-content/cache/* 2>/dev/null || echo "无缓存目录"'))

print('\n[完成] 打赏板块已通过 CSS 隐藏')
print('效果：访问网站时看不到打赏板块')
print('恢复：删除 style.css 末尾的 .support-us-container { display: none !important; } 即可')

client.close()
