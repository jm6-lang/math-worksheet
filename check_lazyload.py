import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check if lazyload JS is loaded
stdin, stdout, stderr = ssh.exec_command(
    "grep -r 'lazyload' /www/wwwroot/resource_site/wp-content/themes/yymarket/*.php | head -5",
    timeout=10
)
print("Lazyload references:")
print(stdout.read().decode().strip())

# Check site URL setting
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp option get siteurl --allow-root",
    timeout=10
)
print("\nSite URL:", stdout.read().decode().strip())

# Check home URL
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp option get home --allow-root",
    timeout=10
)
print("Home URL:", stdout.read().decode().strip())

# Check if lazyload script is enqueued
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'lazyload\|lazy' /www/wwwroot/resource_site/wp-content/themes/yymarket/functions.php | head -10",
    timeout=10
)
print("\nLazyload in functions:")
print(stdout.read().decode().strip())

ssh.close()