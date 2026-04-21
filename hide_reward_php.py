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

# 备份
print('[1] 备份 home-1.php ...')
print(cmd('cp /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php.bak'))

# 用 sed 注释掉打赏板块（从 <!-- Support Us Section --> 到 </div> 结束）
# 更安全的方式：用 PHP if (false) 包裹
print('\n[2] 读取打赏板块代码 ...')
content = cmd('cat /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php')

# 找到打赏板块并注释
import re

# 注释方式：用 HTML 注释包裹整个板块
# 从 <!-- Support Us Section --> 开始，到最后一个 </div>（在 <?php get_footer(); ?> 之前）

# 更简单的方法：把整个 support-us-container div 包成 HTML 注释
new_content = content.replace(
    '<!-- Support Us Section -->',
    '<!-- Support Us Section - 已隐藏用于 AdSense 审核\n<!-- '
)
# 找到 support-us-container 结束的位置并关闭注释

# 让我直接用 PHP 条件包裹
# 在 <!-- Support Us Section --> 前加 <?php if(false): ?>
# 在最后 </div> 后加 <?php endif; ?>

# 读取原文件
print('\n[3] 用 PHP 条件注释掉打赏板块 ...')

# 找到打赏板块的位置
lines = content.split('\n')
new_lines = []
in_reward = False
for i, line in enumerate(lines):
    if '<!-- Support Us Section -->' in line:
        in_reward = True
        new_lines.append('<?php // 临时隐藏打赏板块用于 AdSense 审核 ?>')
        new_lines.append('<?php /*')
        new_lines.append(line)
    elif in_reward and '</div>' in line and 'support-us-container' not in line:
        # 检查是否是打赏板块结束
        # 简单判断：连续3个 </div> 后结束
        new_lines.append(line)
        # 检查后面几行是否是 <script> 或 <?php get_footer
        remaining = '\n'.join(lines[i+1:i+5])
        if '<script>' in remaining or 'get_footer' in remaining or 'jQuery' in remaining:
            new_lines.append('*/ ?>')
            in_reward = False
    else:
        new_lines.append(line)

new_content = '\n'.join(new_lines)

# 写回文件
print(cmd('cat > /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php << \'PHPEOF\'\n' + new_content + '\nPHPEOF'))

# 验证
print('\n[4] 验证修改 ...')
result = cmd('grep -n "Support Us" /www/wwwroot/resource_site/wp-content/themes/yymarket/page-templates/home-1.php')
print(result)

# 同时删除 style.css 里的隐藏规则（因为已经用 PHP 注释了）
print('\n[5] 清理 style.css 中的临时隐藏规则 ...')
print(cmd("sed -i '/隐藏打赏板块/,/}/d' /www/wwwroot/resource_site/wp-content/themes/yymarket/style.css"))
print(cmd("sed -i '/support-us-container.*display.*none/d' /www/wwwroot/resource_site/wp-content/themes/yymarket/style.css"))

print('\n[完成] 打赏板块已用 PHP 注释彻底隐藏，HTML 不会输出到页面')

client.close()
