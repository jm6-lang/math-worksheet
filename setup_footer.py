import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[BEAUTIFY] Set Zibll theme options with correct keys')

php_script = """<?php
define('WP_USE_THEMES', false);
require_once('/www/wwwroot/resource_site/wp-load.php');

// Get current options
$opts = get_option('zibll_options', array());

// Footer copyright (key: 'footer')
$opts['footer'] = 'Copyright &copy; 2026 &middot; <a href="https://beian.miit.gov.cn/" target="_blank" rel="nofollow noopener">鲁ICP备2025156080号-1</a> &middot; 由<a href="https://www.jichuanglm.cn/" target="_blank">极创联盟</a>强力驱动';

// Footer section 1 - title text
$opts['footer_t1_t'] = '极创项目网 - 网创项目资源站';

// Footer section 1 - more content
$opts['fcode_t1_code'] = '专注分享网创项目、副业项目、创业项目、搞钱项目等优质资源，助您实现财富自由';

// Footer section 2 - first line (links)
$opts['fcode_t2_code_1'] = '<a href="/">首页</a>
<a href="/category/default/">项目列表</a>
<a href="/user/">会员中心</a>';

// Footer section 2 - second line (copyright + ICP)
$opts['fcode_t2_code_2'] = 'Copyright &copy; 2026 &middot; <a href="https://beian.miit.gov.cn/" target="_blank" rel="nofollow noopener">鲁ICP备2025156080号-1</a> &middot; 由<a href="https://www.jichuanglm.cn/" target="_blank">极创联盟</a>强力驱动';

// Enable footer tabbar (mobile bottom nav)
$opts['footer_tabbar_s'] = true;

// Navbar style
$opts['navbar_s'] = 1;

// Enable mobile footer display
$opts['footer_t1_m_s'] = true;

update_option('zibll_options', $opts);
echo "Theme options updated\\n";

// Verify
$check = get_option('zibll_options');
echo "footer set: " . (isset($check['footer']) ? 'YES' : 'NO') . "\\n";
echo "fcode_t2_code_2 set: " . (isset($check['fcode_t2_code_2']) ? 'YES' : 'NO') . "\\n";

echo "DONE\\n";
"""

sftp = client.open_sftp()
f = sftp.file('/tmp/setup_footer.php', 'w')
f.write(php_script)
f.close()

# Execute
stdin, stdout, stderr = client.exec_command('cd /www/wwwroot/resource_site && php /tmp/setup_footer.php 2>&1')
result = stdout.read().decode('utf-8', errors='ignore').strip()
print('Result:', result)

errors = stderr.read().decode('utf-8', errors='ignore').strip()
if errors:
    print('Errors:', errors[:500])

# Test homepage
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ | grep -i "copyright\\|ICP\\|极创联盟\\|jichuanglm"')
copyright = stdout.read().decode('utf-8', errors='ignore').strip()
print('Copyright in homepage:', copyright[:300] if copyright else 'Not found')

client.close()