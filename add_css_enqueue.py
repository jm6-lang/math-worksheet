import paramiko

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Create a custom functions.php snippet to enqueue the CSS
php_code = '''<?php
// Enqueue custom CSS
function custom_enqueue_styles() {
    wp_enqueue_style('custom-style', get_template_directory_uri() . '/custom.css', array(), '1.0.0');
}
add_action('wp_enqueue_scripts', 'custom_enqueue_styles');

// Add theme support
add_theme_support('post-thumbnails');
add_theme_support('title-tag');
?>'''

# Append to functions.php
stdin, out, err = c.exec_command(f'echo \'{php_code}\' >> /www/wwwroot/skillxm.cn/public/wp-content/themes/generatepress/functions.php')
print('Add to functions.php:', err.read().decode() if err.read() else 'OK')

# Check file
stdin, out, err = c.exec_command('tail -20 /www/wwwroot/skillxm.cn/public/wp-content/themes/generatepress/functions.php')
print(out.read().decode())

c.close()
print("Done")