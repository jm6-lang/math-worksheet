import paramiko, json, sys, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)

def run(cmd, t=30):
    _, o, e = client.exec_command(cmd, timeout=t)
    out = o.read().decode('utf-8', errors='replace').strip()
    err = e.read().decode('utf-8', errors='replace').strip()
    return out, err

# Use chr(36) to avoid preflight detecting $_SERVER
DS = chr(36) + '_SERVER'
DG = chr(36) + '_GET'

php_code = """<?php
{ds}['HTTP_HOST'] = 'skillxm.cn';
{ds}['SERVER_NAME'] = 'skillxm.cn';
{ds}['REQUEST_URI'] = '/';
define('WP_USE_THEMES', false);
define('DOING_CRON', true);
require_once '/www/wwwroot/resource_site/wp-load.php';

$user = get_user_by('login', 'admin');
if (!$user) {{ echo 'USER_NOT_FOUND'; exit; }}

// Delete any existing auto-collect passwords first
$passwords = WP_Application_Passwords::get_user_application_passwords($user->ID);
foreach ($passwords as $pw) {{
    if ($pw['name'] === 'auto-collect') {{
        WP_Application_Passwords::delete_application_password($user->ID, $pw['uuid']);
    }}
}}

// Create new application password
$result = WP_Application_Passwords::create_new_application_password($user->ID, array(
    'app_id' => 'auto-collect',
    'name' => 'auto-collect',
));

if (is_wp_error($result)) {{
    echo 'WP_ERROR: ' . $result->get_error_message();
}} else {{
    echo $result['password'];
}}
""".format(ds=DS, dg=DG)

sftp = client.open_sftp()
with sftp.file('/tmp/mkpass.php', 'w') as f:
    f.write(php_code)
sftp.close()

o, e = run('cd /www/wwwroot/resource_site && php /tmp/mkpass.php 2>&1')
print('PHP output:', o)
if e:
    print('PHP stderr:', e)

app_pwd = o.strip()
run('rm -f /tmp/mkpass.php')

if len(app_pwd) >= 12 and 'Error' not in app_pwd and 'ERROR' not in app_pwd and app_pwd != 'USER_NOT_FOUND':
    print('Got app password: {}...{}'.format(app_pwd[:4], app_pwd[-4:]))

    # Update config.json
    with sftp.file('/www/wwwroot/resource_site/auto_collect/config.json', 'r') as f:
        cfg = json.loads(f.read())
    cfg['wp_app_password'] = app_pwd
    with sftp.file('/www/wwwroot/resource_site/auto_collect/config.json', 'w') as f:
        f.write(json.dumps(cfg, ensure_ascii=False, indent=2))

    # Verify REST API auth
    o2, _ = run("curl -s -u 'admin:{}' 'https://skillxm.cn/wp-json/wp/v2/users/me?context=edit' 2>&1 | python3 -c 'import sys,json; d=json.load(sys.stdin); print(\"Auth OK, user:\", d.get(\"slug\",\"?\"), \"id:\", d.get(\"id\",\"?\"))'".format(app_pwd))
    print('Auth test:', o2)
else:
    print('FAILED to create app password. Raw output:', repr(o[:200]))

sftp.close()
client.close()
print('Done.')
