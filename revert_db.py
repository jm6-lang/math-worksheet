import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'
db = 'wp_skillxm'
dbuser = 'wp_user'
dbpass = 'gMshA29CshK5'

steps = [
    # 1. Restore original site description
    f"wp option update blogdescription 'AI教程、学习资源、影视资源分享平台' --allow-root --path={wp}",

    # 2. Delete all Yoast postmeta
    f"mysql -u {dbuser} -p'{dbpass}' {db} -N -e \"DELETE FROM wp_postmeta WHERE meta_key LIKE '_yoast_wpseo%'\"",

    # 3. Verify
    f"mysql -u {dbuser} -p'{dbpass}' {db} -N -e \"SELECT COUNT(*) FROM wp_postmeta WHERE meta_key LIKE '_yoast_wpseo%'\"",
    f"wp option get blogdescription --allow-root --path={wp}",
]

for c in steps:
    stdin, stdout, stderr = ssh.exec_command(c, timeout=20)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    label = c.split('--path')[0].strip()[-70:] if '--path' in c else c[:70]
    print(f">>> {label}")
    print(out or err)
    print()

ssh.close()
print("All cleaned")
