import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Fix the functions.php - remove the broken code and add proper code
stdin, out, err = c.exec_command('head -n -13 /www/wwwroot/skillxm.cn/public/wp-content/themes/generatepress/functions.php > /tmp/functions_fixed.php && mv /tmp/functions_fixed.php /www/wwwroot/skillxm.cn/public/wp-content/themes/generatepress/functions.php')
print('Fix functions.php:', err.read().decode() if err.read() else 'OK')

# Add proper custom code
php_code = '''
// Custom CSS enqueue
function skillxm_custom_css() {
    wp_enqueue_style("skillxm-custom", get_template_directory_uri() . "/custom.css", array(), "1.0");
}
add_action("wp_enqueue_scripts", "skillxm_custom_css");
'''

stdin, out, err = c.exec_command(f'echo \'{php_code}\' >> /www/wwwroot/skillxm.cn/public/wp-content/themes/generatepress/functions.php')
print('Add custom code:', err.read().decode() if err.read() else 'OK')

# Verify
stdin, out, err = c.exec_command('tail -10 /www/wwwroot/skillxm.cn/public/wp-content/themes/generatepress/functions.php')
print(out.read().decode())

c.close()
print("Done")