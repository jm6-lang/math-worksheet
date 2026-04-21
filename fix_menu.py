import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'

# Assign menu ID 2 (主菜单) to main-menu location
stdin, stdout, stderr = ssh.exec_command(
    f"wp menu location assign 2 main-menu --allow-root --path={wp}",
    timeout=15
)
print("assign:", stdout.read().decode('utf-8', errors='replace').strip())
err = stderr.read().decode('utf-8', errors='replace').strip()
if err: print("err:", err)

# Verify
stdin, stdout, stderr = ssh.exec_command(
    f"mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT option_value FROM wp_options WHERE option_name='theme_mods_yymarket'\"",
    timeout=10
)
print("theme_mods:", stdout.read().decode('utf-8', errors='replace').strip())

# Flush cache
stdin, stdout, stderr = ssh.exec_command(
    f"wp cache flush --allow-root --path={wp}",
    timeout=10
)
print("cache:", stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()
print("Done")
