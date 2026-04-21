import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

def run_cmd(cmd, timeout=10):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    try:
        out = stdout.read().decode('utf-8', errors='ignore').strip()
        return out
    except:
        return '[TIMEOUT]'

# First switch to Zibll theme
run_cmd("mysql -u root -e \"UPDATE wp_skillxm.wp_options SET option_value = 'zibll' WHERE option_name IN ('template', 'stylesheet');\"")

print('=== Binary search: which file causes the hang ===')

# Test: load inc.php without code.php
# inc.php loads multiple files via zib_require. Let's see what files it loads.
print('\n--- inc.php content (find zib_require calls) ---')
out = run_cmd("grep -n 'zib_require\\|require' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php 2>&1")
print(out[:2000])

# Let's check what files zib_require loads by looking at the array
print('\n--- Find the file list array in inc.php ---')
out = run_cmd("grep -n 'array\\|\\$d\\|\\$data' /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php 2>&1 | head -40")
print(out[:2000])

# Show full inc.php
print('\n--- inc.php full content ---')
out = run_cmd("wc -l /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php 2>&1")
print(f'Lines: {out}')

out = run_cmd("cat /www/wwwroot/resource_site/wp-content/themes/zibll/inc/inc.php 2>&1")
print(out[:3000])

client.close()