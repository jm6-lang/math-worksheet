import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'

steps = [
    # 1. Rename 赚钱教程 -> 网赚项目
    f"wp term update category 53 --name='网赚项目' --slug='wangzhuan' --allow-root --path={wp}",
    # 2. Rename 渠道资源共享 -> 渠道资源
    f"wp term update category 93 --name='渠道资源' --slug='qudao' --allow-root --path={wp}",
    # 3. Get post counts for categories to be merged
    f"wp db query \"SELECT t.term_id, t.name, COUNT(p.ID) as post_count FROM wp_terms t JOIN wp_term_taxonomy tt ON t.term_id = tt.term_id LEFT JOIN wp_term_relationships tr ON tt.term_taxonomy_id = tr.term_taxonomy_id LEFT JOIN wp_posts p ON tr.object_id = p.ID AND p.post_type='post' AND p.post_status='publish' WHERE tt.taxonomy='category' AND t.term_id IN (81,90,87,89,92,83,82) GROUP BY t.term_id\" --allow-root --path={wp}",
]

for c in steps:
    stdin, stdout, stderr = ssh.exec_command(c, timeout=20)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    err = stderr.read().decode('utf-8', errors='replace').strip()
    print(f">>> {c[:70]}")
    print(out if out else (err if err else 'OK'))
    print()

ssh.close()
