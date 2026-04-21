import paramiko, time

HOST = '240b:4001:278:8402:0:bd18:bd09:af0d'
USERNAME = 'root'
PASSWORD = 'l95UE5ysF)7.gR'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, 22, USERNAME, PASSWORD, timeout=15)

print('=== Strategy: Find what blocks ===')
print('Instead of fixing obfuscated code, we will:')
print('1. Switch to Zibll theme')
print('2. Use strace to find the blocking call')
print()

# Step 1: Switch back to Zibll
stdin, stdout, stderr = client.exec_command("mysql -u root -e \"UPDATE wp_skillxm.wp_options SET option_value = 'zibll' WHERE option_name IN ('template', 'stylesheet');\"")
time.sleep(1)

# Step 2: Find the PHP-FPM master PID
stdin, stdout, stderr = client.exec_command('pgrep -f "php-fpm: pool" | head -5')
pids = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'PHP-FPM workers: {pids}')

# Step 3: Use strace on PHP to find blocking network call
# First, make a request in background, then strace a worker
stdin, stdout, stderr = client.exec_command('curl -s -k --max-time 3 https://127.0.0.1/ > /dev/null 2>&1 & sleep 0.5 && strace -f -e trace=network,read,write -p $(pgrep -f "php-fpm: pool" | head -1) -o /tmp/strace_out.txt & sleep 3 && kill %1 %2 2>/dev/null; cat /tmp/strace_out.txt 2>&1 | grep -i "connect\|poll\|recvfrom\|sendto" | tail -30', timeout=15)
strace_out = stdout.read().decode('utf-8', errors='ignore').strip()
print(f'\n=== Strace network calls ===\n{strace_out[:3000]}')

# Step 4: Alternative - use timeout on PHP CLI to see where it hangs
print('\n=== PHP CLI timeout test ===')
# Run WordPress via PHP CLI with a timeout
stdin, stdout, stderr = client.exec_command('cd /www/wwwroot/resource_site && timeout 8 php -d display_errors=1 -r "define(\'WP_USE_THEMES\', true); define(\'ABSPATH\', \'/www/wwwroot/resource_site/\'); require_once ABSPATH . \'wp-load.php\'; echo \'OK\';" 2>&1 | tail -30', timeout=15)
cli_out = stdout.read().decode('utf-8', errors='ignore').strip()
print(cli_out[:2000])

# Step 5: Switch back to safe theme
stdin, stdout, stderr = client.exec_command("mysql -u root -e \"UPDATE wp_skillxm.wp_options SET option_value = 'twentytwentyfour' WHERE option_name IN ('template', 'stylesheet');\"")
print('\nSwitched back to twentytwentyfour for safety')

client.close()