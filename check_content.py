import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check some post titles to understand the content
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp post list --post_type=post --posts_per_page=20 --fields=ID,post_title --format=csv --allow-root",
    timeout=15
)
print("Sample posts:")
print(stdout.read().decode('utf-8', errors='replace')[:1000])

# Check categories
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp term list category --fields=name,count --format=csv --allow-root",
    timeout=15
)
print("\nCategories:")
print(stdout.read().decode('utf-8', errors='replace'))

ssh.close()