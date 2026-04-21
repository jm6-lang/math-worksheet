import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'

# Restore original site name
stdin, stdout, stderr = ssh.exec_command(
    f"wp option update blogname '小二郎资源网' --allow-root --path={wp}",
    timeout=15
)
print("blogname:", stdout.read().decode('utf-8', errors='replace').strip())

# Verify
stdin, stdout, stderr = ssh.exec_command(
    f"wp option get blogname --allow-root --path={wp}",
    timeout=10
)
print("verify:", stdout.read().decode('utf-8', errors='replace').strip())

# Also flush cache
stdin, stdout, stderr = ssh.exec_command(
    f"wp cache flush --allow-root --path={wp}",
    timeout=10
)
print("cache:", stdout.read().decode('utf-8', errors='replace').strip())

ssh.close()
print("Done")
