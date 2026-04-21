import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

wp = '/www/wwwroot/resource_site'

# Move posts from source categories to target categories
# First get all post IDs in each source category, then reassign

steps = [
    # Get post IDs in 书籍资料(81)
    f"wp db query \"SELECT p.ID FROM wp_posts p JOIN wp_term_relationships tr ON p.ID = tr.object_id JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id WHERE tt.term_id = 81 AND p.post_type='post' AND p.post_status='publish'\" --allow-root --path={wp} | tail -n +2",
    # Get post IDs in 传统文化(90)
    f"wp db query \"SELECT p.ID FROM wp_posts p JOIN wp_term_relationships tr ON p.ID = tr.object_id JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id WHERE tt.term_id = 90 AND p.post_type='post' AND p.post_status='publish'\" --allow-root --path={wp} | tail -n +2",
    # Get post IDs in 健康养生(87)
    f"wp db query \"SELECT p.ID FROM wp_posts p JOIN wp_term_relationships tr ON p.ID = tr.object_id JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id WHERE tt.term_id = 87 AND p.post_type='post' AND p.post_status='publish'\" --allow-root --path={wp} | tail -n +2",
    # Get post IDs in 跨境电商(82)
    f"wp db query \"SELECT p.ID FROM wp_posts p JOIN wp_term_relationships tr ON p.ID = tr.object_id JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id WHERE tt.term_id = 82 AND p.post_type='post' AND p.post_status='publish'\" --allow-root --path={wp} | tail -n +2",
    # Get post IDs in 自媒体运营(83)
    f"wp db query \"SELECT p.ID FROM wp_posts p JOIN wp_term_relationships tr ON p.ID = tr.object_id JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id WHERE tt.term_id = 83 AND p.post_type='post' AND p.post_status='publish'\" --allow-root --path={wp} | tail -n +2",
]

results = {}
for i, c in enumerate(steps):
    stdin, stdout, stderr = ssh.exec_command(c, timeout=20)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    cats = ['books(81)', 'culture(90)', 'health(87)', 'crossborder(82)', 'selfmedia(83)']
    results[cats[i]] = [x.strip() for x in out.split('\n') if x.strip() and x.strip().isdigit()]
    print(f"{cats[i]}: {len(results[cats[i]])} posts")

ssh.close()
print("\nPost IDs collected")
