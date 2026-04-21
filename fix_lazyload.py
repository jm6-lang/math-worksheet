import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Fix index.php - remove lazyload, use src directly
stdin, stdout, stderr = ssh.exec_command(
    """sed -i 's/<img class="lazyload" src="<?php echo yy_get('\''site_loading_image'\''\?)>" data-src="<?php echo get_the_post_thumbnail_url()\?:yy_get('\''site_thumbnail'\''\?)>"/<img src="<?php echo get_the_post_thumbnail_url()\?:yy_get('\''site_thumbnail'\''\?)>"/g' /www/wwwroot/resource_site/wp-content/themes/yymarket/index.php""",
    timeout=10
)

# Fix search.php same way  
stdin, stdout, stderr = ssh.exec_command(
    """sed -i 's/<img class="lazyload" src="<?php echo yy_get('\''site_loading_image'\''\?)>" data-src="<?php echo get_the_post_thumbnail_url()\?:yy_get('\''site_thumbnail'\''\?)>"/<img src="<?php echo get_the_post_thumbnail_url()\?:yy_get('\''site_thumbnail'\''\?)>"/g' /www/wwwroot/resource_site/wp-content/themes/yymarket/search.php""",
    timeout=10
)

# Verify the changes
stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'get_the_post_thumbnail_url' /www/wwwroot/resource_site/wp-content/themes/yymarket/index.php",
    timeout=10
)
print("Fixed index.php:")
print(stdout.read().decode().strip())

stdin, stdout, stderr = ssh.exec_command(
    "grep -n 'get_the_post_thumbnail_url' /www/wwwroot/resource_site/wp-content/themes/yymarket/search.php",
    timeout=10
)
print("\nFixed search.php:")
print(stdout.read().decode().strip())

ssh.close()
print("\nDone! Images should display now.")