import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Create SQL to bulk update thumbnails by category
sql = """
-- 网赚项目 (cat 53) -> money image (1087)
UPDATE wp_postmeta 
SET meta_value = '1087' 
WHERE meta_key = '_thumbnail_id' 
AND post_id IN (
    SELECT object_id FROM wp_term_relationships 
    WHERE term_taxonomy_id IN (SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id = 53)
);

-- 小说资源 (cat 84) -> novel image (1085)
UPDATE wp_postmeta 
SET meta_value = '1085' 
WHERE meta_key = '_thumbnail_id' 
AND post_id IN (
    SELECT object_id FROM wp_term_relationships 
    WHERE term_taxonomy_id IN (SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id = 84)
);

-- 教程合集 (cat 85) -> course image (1088)
UPDATE wp_postmeta 
SET meta_value = '1088' 
WHERE meta_key = '_thumbnail_id' 
AND post_id IN (
    SELECT object_id FROM wp_term_relationships 
    WHERE term_taxonomy_id IN (SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id = 85)
);

-- 影视资源 (cat 86) -> movie image (1086)
UPDATE wp_postmeta 
SET meta_value = '1086' 
WHERE meta_key = '_thumbnail_id' 
AND post_id IN (
    SELECT object_id FROM wp_term_relationships 
    WHERE term_taxonomy_id IN (SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id = 86)
);

-- 资源合集 (cat 91) -> default image (1091)
UPDATE wp_postmeta 
SET meta_value = '1091' 
WHERE meta_key = '_thumbnail_id' 
AND post_id IN (
    SELECT object_id FROM wp_term_relationships 
    WHERE term_taxonomy_id IN (SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id = 91)
);

-- 网创资源 (cat 93) -> money image (1087)
UPDATE wp_postmeta 
SET meta_value = '1087' 
WHERE meta_key = '_thumbnail_id' 
AND post_id IN (
    SELECT object_id FROM wp_term_relationships 
    WHERE term_taxonomy_id IN (SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id = 93)
);
"""

# Save SQL
sftp = ssh.open_sftp()
with sftp.open('/tmp/update_thumbs.sql', 'w') as f:
    f.write(sql)
sftp.close()

# Execute
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query < /tmp/update_thumbs.sql --allow-root 2>&1",
    timeout=30
)
result = stdout.read().decode()
print("SQL Result:", result[:500])

# Check a sample
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && wp db query \"SELECT p.ID, p.post_title, pm.meta_value as thumb_id FROM wp_posts p JOIN wp_postmeta pm ON p.ID = pm.post_id WHERE pm.meta_key='_thumbnail_id' AND p.post_type='post' LIMIT 10\" --allow-root",
    timeout=15
)
print("\nSample posts with thumbnails:")
print(stdout.read().decode())

ssh.close()
print("\nDone! Category-specific images assigned.")