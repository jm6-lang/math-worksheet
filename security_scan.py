import paramiko

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD)

print('[SECURITY SCAN] Scanning zibll theme...')

# 1. Check for eval() calls
stdin, stdout, stderr = client.exec_command('grep -r "eval(" /www/wwwroot/resource_site/wp-content/themes/zibll/ 2>/dev/null | wc -l')
print('[1] eval() calls:', stdout.read().decode('utf-8', errors='ignore').strip())

# 2. Check for base64_decode
stdin, stdout, stderr = client.exec_command('grep -r "base64_decode" /www/wwwroot/resource_site/wp-content/themes/zibll/ 2>/dev/null | wc -l')
print('[2] base64_decode calls:', stdout.read().decode('utf-8', errors='ignore').strip())

# 3. Check for shell_exec
stdin, stdout, stderr = client.exec_command('grep -rE "shell_exec|exec\\(|system\\(|passthru" /www/wwwroot/resource_site/wp-content/themes/zibll/ 2>/dev/null | wc -l')
print('[3] Shell execution calls:', stdout.read().decode('utf-8', errors='ignore').strip())

# 4. Check for suspicious input usage
stdin, stdout, stderr = client.exec_command('grep -rE "\\\\$_GET|\\\\$_POST|\\\\$_REQUEST" /www/wwwroot/resource_site/wp-content/themes/zibll/ 2>/dev/null | wc -l')
print('[4] $_GET/$_POST usage:', stdout.read().decode('utf-8', errors='ignore').strip())

# 5. Check for gzinflate
stdin, stdout, stderr = client.exec_command('grep -r "gzinflate" /www/wwwroot/resource_site/wp-content/themes/zibll/ 2>/dev/null | wc -l')
print('[5] gzinflate calls:', stdout.read().decode('utf-8', errors='ignore').strip())

# 6. File count and size
stdin, stdout, stderr = client.exec_command('find /www/wwwroot/resource_site/wp-content/themes/zibll/ -name "*.php" | wc -l')
print('[6] PHP files:', stdout.read().decode('utf-8', errors='ignore').strip())

stdin, stdout, stderr = client.exec_command('du -sh /www/wwwroot/resource_site/wp-content/themes/zibll/')
print('[7] Theme size:', stdout.read().decode('utf-8', errors='ignore').strip())

# 7. Recently modified files
stdin, stdout, stderr = client.exec_command('find /www/wwwroot/resource_site/wp-content/themes/zibll/ -name "*.php" -mmin -60 -type f 2>/dev/null')
print('[8] Recently modified PHP files:')
print(stdout.read().decode('utf-8', errors='ignore')[:500] or 'None')

# 8. Check for long encoded strings
stdin, stdout, stderr = client.exec_command('grep -rEl "[A-Za-z0-9+/=]{100,}" /www/wwwroot/resource_site/wp-content/themes/zibll/ 2>/dev/null | head -10')
print('[9] Files with long encoded strings:')
print(stdout.read().decode('utf-8', errors='ignore')[:300] or 'None')

client.close()
print('\n[DONE] Security scan complete')