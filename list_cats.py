import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'

# Get all categories
stdin, stdout, stderr = ssh.exec_command(
    f"wp term list category --allow-root --path={wp} --fields=term_id,name,slug --format=csv",
    timeout=15
)
out = stdout.read().decode('utf-8', errors='replace').strip()
print(out)

ssh.close()
