import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'

cmds = [
    # Current theme
    f"wp option get template --allow-root --path={wp}",
    f"wp option get stylesheet --allow-root --path={wp}",
    # Current site name
    f"wp option get blogname --allow-root --path={wp}",
    f"wp option get blogdescription --allow-root --path={wp}",
    # All installed themes
    f"wp theme list --allow-root --path={wp} --format=csv",
    # Check option revisions/backups
    f"mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT option_name, option_value FROM wp_options WHERE option_name IN ('blogname','blogdescription','template','stylesheet','siteurl','home')\"",
]

for c in cmds:
    stdin, stdout, stderr = ssh.exec_command(c, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    label = c.split('--path')[0].strip()[-70:] if '--path' in c else c[:70]
    print(f">>> {label}")
    print(out[:500] if out else err)
    print()

ssh.close()
