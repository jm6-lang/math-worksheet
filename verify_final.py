import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'

# Get real slugs
stdin, stdout, stderr = ssh.exec_command(
    f"mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT term_id, name, slug FROM wp_terms WHERE term_id IN (80,84,85,86,53,93)\"",
    timeout=10
)
out = stdout.read().decode('utf-8', errors='replace').strip()
print("分类详情:")
print(out)
print()

# Verify menu items
stdin, stdout, stderr = ssh.exec_command(
    f"wp menu item list 2 --allow-root --path={wp} --fields=db_id,title,url --format=table",
    timeout=10
)
out = stdout.read().decode('utf-8', errors='replace').strip()
print("菜单项:")
print(out)
print()

# Flush cache
stdin, stdout, stderr = ssh.exec_command(
    f"wp cache flush --allow-root --path={wp}",
    timeout=10
)
print("缓存:", stdout.read().decode().strip())

ssh.close()
