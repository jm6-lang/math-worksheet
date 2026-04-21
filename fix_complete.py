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

# 读取完整内容
print('[1] 读取完整 home-1.php ...')
content = cmd('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php')
lines = content.split('\n')
print(f'总行数: {len(lines)}')

# 找到 ticker script 开始和结束位置
print('\n[2] 定位 ticker script ...')
ticker_start = None
ticker_end = None
for i, line in enumerate(lines):
    if '<script>' in line and '<?php' not in line:
        # 检查是否是 ticker script
        context = '\n'.join(lines[max(0,i-2):i+3])
        if 'ticker' in context.lower() or 'ticker-list' in context:
            ticker_start = i
            print(f'  ticker script 开始行: {i+1}')
    if ticker_start is not None and '</script>' in line:
        ticker_end = i
        print(f'  ticker script 结束行: {i+1}')
        break

# 找到 get_footer 位置
get_footer_line = None
for i, line in enumerate(lines):
    if '<?php get_footer()' in line:
        get_footer_line = i
        print(f'  get_footer 行: {i+1}')
        break

if ticker_start and ticker_end and get_footer_line:
    print(f'\n[3] 保留第 1-{ticker_start} 行 + 第 {get_footer_line+1} 行之后')
    
    # 保留：开头到 ticker script 开始之前 + get_footer 那一行
    new_lines = lines[:ticker_start]
    new_lines.append(lines[get_footer_line])  # 保留 get_footer
    
    new_content = '\n'.join(new_lines)
    
    # 写入
    print('\n[4] 写入修复后的文件...')
    cmd('cat > /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php << \'EOFEND\n' + new_content + '\nEOFEND')
    
    # 验证 PHP 语法
    print('\n[5] PHP 语法检查...')
    print(cmd('php -l /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php'))
    
    # 测试网站
    print('\n[6] 测试网站访问...')
    print(cmd('curl -s -o /dev/null -w "HTTP状态码: %{http_code}\\n" http://127.0.0.1/'))
    
    # 确认无打赏关键词
    print('\n[7] 最终检查打赏关键词...')
    for kw in ['打赏', 'support-us', 'PayPal', '微信']:
        r = cmd(f"grep -c '{kw}' /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php")
        print(f'  {kw}: {r.strip()}')
    
    # 查看文件末尾
    print('\n[8] 文件末尾...')
    print(cmd('tail -10 /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php'))

client.close()
print('\n[完成]')
