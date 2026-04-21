import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'
dbuser = 'wp_user'
dbpass = 'gMshA29CshK5'
dbname = 'wp_skillxm'

# Step A: Merge 书籍资料(81), 传统文化(90), 健康养生(87) into 教育资源(84)
# For each source category, update term_taxonomy_id in wp_term_relationships

sql_merge_edu = f"""-- Get term_taxonomy_ids
SET @src_books = (SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id=81 AND taxonomy='category');
SET @src_culture = (SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id=90 AND taxonomy='category');
SET @src_health = (SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id=87 AND taxonomy='category');
SET @dst_edu = (SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id=84 AND taxonomy='category');

-- Update 书籍资料 -> 教育资源
UPDATE wp_term_relationships SET term_taxonomy_id = @dst_edu WHERE term_taxonomy_id = @src_books;

-- Update 传统文化 -> 教育资源
UPDATE wp_term_relationships SET term_taxonomy_id = @dst_edu WHERE term_taxonomy_id = @src_culture;

-- Update 健康养生 -> 教育资源
UPDATE wp_term_relationships SET term_taxonomy_id = @dst_edu WHERE term_taxonomy_id = @src_health;
"""

# Step B: Merge 跨境电商(82), 自媒体运营(83) into 网赚项目(53)
sql_merge_wangzhuan = f"""SET @src_cross = (SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id=82 AND taxonomy='category');
SET @src_media = (SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id=83 AND taxonomy='category');
SET @dst_wz = (SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id=53 AND taxonomy='category');

UPDATE wp_term_relationships SET term_taxonomy_id = @dst_wz WHERE term_taxonomy_id = @src_cross;
UPDATE wp_term_relationships SET term_taxonomy_id = @dst_wz WHERE term_taxonomy_id = @src_media;
"""

# Step C: Delete old categories (after merging)
sql_cleanup = f"""DELETE FROM wp_term_taxonomy WHERE term_id IN (81, 82, 83, 87, 89, 90, 92);
DELETE FROM wp_terms WHERE term_id IN (81, 82, 83, 87, 89, 90, 92);
"""

for label, sql in [("合并到教育资源", sql_merge_edu), ("合并到网赚项目", sql_merge_wangzhuan), ("删除旧分类", sql_cleanup)]:
    cmd = f"mysql -u {dbuser} -p'{dbpass}' {dbname} -e \"{sql}\""
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    print(f">>> {label}")
    print(err if 'Warning' in err else (out or err or 'OK'))
    print()

ssh.close()
print("Done")
