import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

# Add custom CSS enqueue after pk_init_wp_empty_style
cmd = """sed -i "s/add_action('wp_enqueue_scripts', 'pk_init_wp_empty_style');/add_action('wp_enqueue_scripts', 'pk_init_wp_empty_style');\\n\\n\\/\\/ Custom brand style\\nadd_action('wp_enqueue_scripts', function(){wp_enqueue_style('sk-custom', get_template_directory_uri().'\\/assets\\/custom.css', array(), '1.0');}, 99);/" /www/wwwroot/resource_site/wp-content/themes/puock/functions.php"""

stdin, stdout, stderr = client.exec_command(cmd, timeout=10)
out = stdout.read().decode('utf-8', errors='replace')
err = stderr.read().decode('utf-8', errors='replace')
print('sed out:', out)
print('sed err:', err)

# Verify it was added
stdin, stdout, stderr = client.exec_command(
    'grep -n "sk-custom\\|custom.css" /www/wwwroot/resource_site/wp-content/themes/puock/functions.php',
    timeout=10
)
print('Verify:', stdout.read().decode('utf-8', errors='replace'))

client.close()
print('Done!')
