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

print('[1] 读取当前 home-1.php ...')
content = cmd('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-templates/home-1.php 2>/dev/null || cat /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php')

# 找到打赏板块并删除
print('\n[2] 定位打赏板块...')
lines = content.split('\n')

# 找到打赏板块的起止行
start_idx = None
end_idx = None
brace_count = 0

for i, line in enumerate(lines):
    if '<!-- Support Us Section -->' in line or 'support-us-container' in line:
        if start_idx is None:
            start_idx = i
            print(f'  起始行: {i+1}')
    
    if start_idx is not None:
        # 找到结束：在 get_footer 之前的 </div> 后，或者到 <script> 开始
        if '<?php get_footer()' in line or '<script>' in line:
            end_idx = i
            print(f'  结束行: {i+1}')
            break

if start_idx is None:
    print('  [错误] 未找到打赏板块起始位置')
elif end_idx is None:
    print('  [错误] 未找到打赏板块结束位置')
else:
    # 删除打赏板块
    print(f'\n[3] 删除第 {start_idx+1} 到 {end_idx} 行...')
    
    # 保留 get_footer 和 script
    new_lines = lines[:start_idx]
    
    # 检查 end_idx 那行是什么
    end_line = lines[end_idx] if end_idx < len(lines) else ''
    if '<?php get_footer()' in end_line or '<script>' in end_line:
        # 保留这行
        new_lines.extend(lines[end_idx:])
    
    new_content = '\n'.join(new_lines)
    
    # 备份原文件
    print('\n[4] 备份原文件...')
    print(cmd('cp /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php.bak2'))
    
    # 写入新文件
    print('\n[5] 写入清理后的文件...')
    cmd('cat > /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php << \'ENDOFFILE\'\n' + new_content + '\nENDOFFILE')
    
    # 验证
    print('\n[6] 验证删除结果...')
    result = cmd('grep -c "support-us" /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php')
    if result.strip() == '0':
        print('  [OK] support-us 已完全删除')
    else:
        print(f'  [警告] 仍有 {result.strip()} 处 support-us')
    
    result = cmd('grep -c "打赏" /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php')
    if result.strip() == '0':
        print('  [OK] 打赏关键词已完全删除')
    else:
        print(f'  [警告] 仍有 {result.strip()} 处打赏')

print('\n[完成]')
client.close()
