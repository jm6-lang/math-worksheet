import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Backup
stdin, stdout, stderr = ssh.exec_command(
    "cp /www/wwwroot/resource_site/wp-content/themes/yymarket/sidebar.php /www/wwwroot/resource_site/wp-content/themes/yymarket/sidebar.php.bak",
    timeout=10
)
print("Backup created")

# Read full file
stdin, stdout, stderr = ssh.exec_command(
    "cat /www/wwwroot/resource_site/wp-content/themes/yymarket/sidebar.php",
    timeout=10
)
content = stdout.read().decode('utf-8', errors='replace')

# Remove the tag cloud widget section (lines 24-36)
# Find and remove the widget_tag_cloud block
import re

# Pattern to match the entire tag cloud widget block
pattern = r'''\t\t\t<li class="widget widget_tag_cloud" ><h3>.*?</h3>\n\t\t\t\t<div class="tagcloud">\n\t\t\t\t.*?\n\t\t\t\t</div>\n\t\t\t</li>\n'''

# Use simpler approach - find the exact block and remove
lines = content.split('\n')
new_lines = []
skip = False
skip_count = 0

for i, line in enumerate(lines):
    if 'widget_tag_cloud' in line and '<li' in line:
        skip = True
        skip_count = 0
        continue
    if skip:
        if '</li>' in line and 'widget_tag_cloud' not in line:
            skip = False
            continue
        skip_count += 1
        if skip_count > 20:  # Safety break
            skip = False
        continue
    new_lines.append(line)

new_content = '\n'.join(new_lines)

# Write back
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/wp-content/themes/yymarket/sidebar.php', 'w') as f:
    f.write(new_content)
sftp.close()

print("Tag cloud removed")

# Verify
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'tag_cloud\|Tag Cloud' /www/wwwroot/resource_site/wp-content/themes/yymarket/sidebar.php",
    timeout=10
)
result = stdout.read().decode().strip()
print("Tag cloud references after removal:", result if result else "None (removed successfully)")

ssh.close()
print("Done!")