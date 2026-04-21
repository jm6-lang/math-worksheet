import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'

# Check custom CSS
cmds = [
    f"wp option get site_custom_css --allow-root --path={wp}",
    f"wp option get custom_css --allow-root --path={wp}",
    # Check theme options for any CSS
    f"mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT option_name, LEFT(option_value,200) FROM wp_options WHERE option_name LIKE '%css%' OR option_name LIKE '%style%' LIMIT 10\"",
    # Check for any injected CSS in theme
    f"ls -la /www/wwwroot/resource_site/wp-content/themes/yymarket/assets/css/",
    f"head -50 /www/wwwroot/resource_site/wp-content/themes/yymarket/style.css",
]

for c in cmds:
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    label = c.split()[0][:60]
    print(f">>> {c[:80]}")
    print(out[:600] if out else (err[:200] if err else '(empty)'))
    print()

ssh.close()
