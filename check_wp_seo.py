import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Check current SEO plugin settings
cmd = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT option_name, option_value FROM wp_options 
WHERE option_name LIKE '%blogname%' OR option_name LIKE '%blogdescription%' 
OR option_name LIKE '%siteurl%' OR option_name LIKE '%home%'
LIMIT 10;
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print("=== WordPress 基本设置 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# Check SEO plugin settings (Rank Math or Yoast)
cmd2 = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT option_name FROM wp_options 
WHERE option_name LIKE '%rank_math%' OR option_name LIKE '%wpseo%'
LIMIT 20;
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd2, timeout=30)
print("\n=== SEO插件设置 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# Check homepage meta description
cmd3 = '''
mysql -u wp_user -pgMshA29CshK5 wp_skillxm -e "
SELECT p.ID, p.post_title, pm.meta_key, pm.meta_value 
FROM wp_posts p 
LEFT JOIN wp_postmeta pm ON p.ID = pm.post_id 
WHERE p.post_type = 'page' AND p.post_status = 'publish' 
AND (pm.meta_key = 'rank_math_description' OR pm.meta_key = '_yoast_wpseo_metadesc')
LIMIT 5;
"
'''
stdin, stdout, stderr = ssh.exec_command(cmd3, timeout=30)
print("\n=== 页面SEO设置 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()