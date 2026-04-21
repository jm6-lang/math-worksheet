import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check for existing image collection scripts
stdin, stdout, stderr = ssh.exec_command(
    "find /www/wwwroot -name '*.py' -o -name '*.sh' | xargs grep -l 'image\|图片\|采集\|crawl' 2>/dev/null | head -20",
    timeout=15
)
scripts = stdout.read().decode().strip()
print("Found scripts:")
print(scripts if scripts else "None found")

# Check for any cron jobs related to images
stdin, stdout, stderr = ssh.exec_command(
    "crontab -l 2>/dev/null | grep -i image || echo 'No image cron jobs'",
    timeout=10
)
print("\nCron jobs:")
print(stdout.read().decode().strip())

# Check wp-content for any collection scripts
stdin, stdout, stderr = ssh.exec_command(
    "ls -la /www/wwwroot/resource_site/ | grep -i script\|tool\|collect",
    timeout=10
)
print("\nScripts in site root:")
print(stdout.read().decode().strip())

ssh.close()