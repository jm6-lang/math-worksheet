import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Set fcode_template to template_1')

php_script = """<?php
define('WP_USE_THEMES', false);
require_once('/www/wwwroot/resource_site/wp-load.php');

$opts = get_option('zibll_options', array());

// CRITICAL: Enable footer template
$opts['fcode_template'] = 'template_1';

// Also set the general footer text (for single page footer)
$opts['footer'] = 'Copyright &copy; 2026 &middot; <a href="https://beian.miit.gov.cn/" target="_blank" rel="nofollow noopener">鲁ICP备2025156080号-1</a> &middot; 由<a href="https://www.jichuanglm.cn/" target="_blank">极创联盟</a>强力驱动';

// Footer section 1 - title text
$opts['footer_t1_t'] = '极创项目网';

// Footer section 1 - more content
$opts['fcode_t1_code'] = '专注分享网创项目、副业项目、创业项目、搞钱项目等优质资源';

// Footer section 2 - links
$opts['fcode_t2_code_1'] = '<a href="/">首页</a> <a href="/category/default/">项目列表</a> <a href="/user/">会员中心</a>';

// Footer section 2 - copyright + ICP
$opts['fcode_t2_code_2'] = 'Copyright &copy; 2026 &middot; <a href="https://beian.miit.gov.cn/" target="_blank" rel="nofollow noopener">鲁ICP备2025156080号-1</a> &middot; 由<a href="https://www.jichuanglm.cn/" target="_blank">极创联盟</a>强力驱动';

// Enable mobile footer
$opts['footer_t1_m_s'] = true;
$opts['footer_contact_m_s'] = true;

update_option('zibll_options', $opts);

// Clear cache
global $wpdb;
$wpdb->query("DELETE FROM $wpdb->options WHERE option_name LIKE '%transient%'");
wp_cache_flush();

echo "fcode_template: " . $opts['fcode_template'] . "\\n";
echo "DONE\\n";
"""

sftp = client.open_sftp()
f = sftp.file('/tmp/fix_footer.php', 'w')
f.write(php_script)
f.close()

stdin, stdout, stderr = client.exec_command('cd /www/wwwroot/resource_site && php /tmp/fix_footer.php 2>&1')
print('Result:', stdout.read().decode('utf-8', errors='ignore').strip())

# Verify
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ | grep -i "copyright\\|ICP\\|极创联盟\\|jichuanglm\\|fcode"')
copyright = stdout.read().decode('utf-8', errors='ignore').strip()
print('Footer content:', copyright[:500] if copyright else 'Still empty')

# Check footer HTML now
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ | grep -A 20 "container-footer"')
footer_html = stdout.read().decode('utf-8', errors='ignore').strip()
print('Footer HTML:', footer_html[:500])

client.close()