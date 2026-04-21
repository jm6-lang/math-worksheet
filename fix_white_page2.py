import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[FIX] Thorough fix for white page')

# Open SFTP once
sftp = client.open_sftp()

# Step 1: Check if the is_update call still exists in both files
for filepath in [
    '/www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/admin-options.php',
    '/www/wwwroot/resource_site/wp-content/themes/zibll/inc/options/options-module.php',
]:
    f = sftp.file(filepath, 'r')
    content = f.read().decode('utf-8', errors='replace')
    f.close()
    
    count = content.count('ZibAut::is_update()')
    print(f'{filepath.split("/")[-1]}: {count} occurrences of ZibAut::is_update()')
    
    if count > 0:
        content = content.replace('ZibAut::is_update()', 'null /* bypassed */')
        f = sftp.file(filepath, 'w')
        f.write(content)
        f.close()
        print(f'  -> Replaced all {count} occurrences')

# Step 2: Check code.php line 381 - it's calling curl_update via eval()
# The eval code at line 373 and 381 calls curl_update() which causes the TypeError
# We need to make curl_update() return null without executing its eval code

f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php', 'r')
code_content = f.read().decode('utf-8', errors='replace')
f.close()

# Check if curl_update still contains eval
if 'function curl_update()' in code_content:
    print('curl_update() still has original code')
    # Find the function definition
    pos = code_content.find('function curl_update()')
    # Find where this function ends (next 'function ' in the class)
    next_func = code_content.find('\n    function ', pos + 1)
    if next_func < 0:
        next_func = code_content.find('\nfunction ', pos + 1)
    
    if next_func > 0:
        # Replace the entire function body
        before = code_content[:pos]
        after = code_content[next_func:]
        new_func = 'function curl_update(){return null;}'
        code_content = before + new_func + after
        
        f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php', 'w')
        f.write(code_content)
        f.close()
        print('Replaced curl_update() with return null')

# Step 3: Also make is_update() safe
f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php', 'r')
code_content = f.read().decode('utf-8', errors='replace')
f.close()

if 'function is_update(' in code_content:
    pos = code_content.find('function is_update(')
    next_func = code_content.find('\n    function ', pos + 1)
    if next_func < 0:
        next_func = code_content.find('\nfunction ', pos + 1)
    
    if next_func > 0:
        before = code_content[:pos]
        after = code_content[next_func:]
        new_func = 'function is_update($r=null){return null;}'
        code_content = before + new_func + after
        
        f = sftp.file('/www/wwwroot/resource_site/wp-content/themes/zibll/inc/code/code.php', 'w')
        f.write(code_content)
        f.close()
        print('Replaced is_update() with return null')

# Step 4: Fix permissions
stdin, stdout, stderr = client.exec_command('chown -R www-data:www-data /www/wwwroot/resource_site/wp-content/themes/zibll/')

# Step 5: Restart
stdin, stdout, stderr = client.exec_command('systemctl restart php8.1-fpm nginx')

import time
time.sleep(2)

# Step 6: Test
stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ 2>&1 | head -3')
print('Homepage:', stdout.read().decode('utf-8', errors='ignore').strip()[:300])

stdin, stdout, stderr = client.exec_command('curl -s -k -o /dev/null -w "%{http_code}" https://127.0.0.1/ 2>&1')
print(f'Homepage HTTP: {stdout.read().decode("utf-8", errors="ignore").strip()}')

stdin, stdout, stderr = client.exec_command('curl -s -k -o /dev/null -w "%{http_code}" https://127.0.0.1/wp-admin/ 2>&1')
print(f'Admin HTTP: {stdout.read().decode("utf-8", errors="ignore").strip()}')

stdin, stdout, stderr = client.exec_command('curl -s -k https://127.0.0.1/ 2>&1 | grep -c "Fatal\\|Parse error\\|Warning"')
print(f'Page errors: {stdout.read().decode("utf-8", errors="ignore").strip()}')

client.close()