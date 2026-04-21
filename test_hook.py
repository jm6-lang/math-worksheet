import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Test if the function exists and runs
cmd = """cd /www/wwwroot/resource_site && wp eval "
if (function_exists('geo_ai_optimization')) {
    echo 'FUNCTION EXISTS';
} else {
    echo 'FUNCTION NOT FOUND';
}
$hooks = $GLOBALS['wp_filter']['wp_head'];
if (isset($hooks[99])) {
    echo 'PRIORITY 99 HOOKS: ' . count($hooks[99]) . '\\n';
    foreach ($hooks[99] as $key => $val) {
        echo '  - ' . print_r($key, true);
    }
} else {
    echo 'NO PRIORITY 99 HOOKS';
}
" --allow-root 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("WP eval:")
print(stdout.read().decode('utf-8', errors='ignore'))
err = stderr.read().decode('utf-8', errors='ignore')
if err:
    print("Errors: %s" % err[:300])

ssh.close()
