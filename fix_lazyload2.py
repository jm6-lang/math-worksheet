import paramiko
import re

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sftp = ssh.open_sftp()

# Fix index.php
with sftp.open('/www/wwwroot/resource_site/wp-content/themes/yymarket/index.php', 'r') as f:
    content = f.read().decode('utf-8')

# Replace lazyload img with normal img
old_pattern = '<img class="lazyload" src="<?php echo yy_get(\'site_loading_image\')?>" data-src="<?php echo get_the_post_thumbnail_url()?:yy_get(\'site_thumbnail\')?>" alt="<?php the_title() ?>"'
new_pattern = '<img src="<?php echo get_the_post_thumbnail_url()?:yy_get(\'site_thumbnail\')?>" alt="<?php the_title() ?>"'

content = content.replace(old_pattern, new_pattern)

with sftp.open('/www/wwwroot/resource_site/wp-content/themes/yymarket/index.php', 'w') as f:
    f.write(content)

print("index.php fixed")

# Fix search.php
with sftp.open('/www/wwwroot/resource_site/wp-content/themes/yymarket/search.php', 'r') as f:
    content = f.read().decode('utf-8')

content = content.replace(old_pattern, new_pattern)

with sftp.open('/www/wwwroot/resource_site/wp-content/themes/yymarket/search.php', 'w') as f:
    f.write(content)

print("search.php fixed")

# Also check archive.php
with sftp.open('/www/wwwroot/resource_site/wp-content/themes/yymarket/archive.php', 'r') as f:
    content = f.read().decode('utf-8')

if 'lazyload' in content:
    content = content.replace(old_pattern, new_pattern)
    with sftp.open('/www/wwwroot/resource_site/wp-content/themes/yymarket/archive.php', 'w') as f:
        f.write(content)
    print("archive.php fixed")

sftp.close()
ssh.close()
print("\nAll done! Refresh the page to see images.")