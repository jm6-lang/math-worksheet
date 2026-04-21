import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.')

print("=" * 50, flush=True)
print("SEO OPTIMIZATION - FINAL VERIFICATION", flush=True)
print("=" * 50, flush=True)

checks = [
    ("1. Sitemap Index (HTTP 200)", "curl -s https://skillxm.cn/sitemap_index.xml -o /dev/null -w 'HTTP %{http_code}, Size: %{size_download} bytes'"),
    ("2. Post Sitemap (HTTP 200)", "curl -s https://skillxm.cn/post-sitemap.xml -o /dev/null -w 'HTTP %{http_code}, Size: %{size_download} bytes'"),
    ("3. Category Sitemap (HTTP 200)", "curl -s https://skillxm.cn/category-sitemap.xml -o /dev/null -w 'HTTP %{http_code}, Size: %{size_download} bytes'"),
    ("4. Robots.txt", "curl -s https://skillxm.cn/robots.txt 2>/dev/null | grep -c 'Sitemap'"),
    ("5. Homepage Title", "curl -s https://skillxm.cn/ 2>/dev/null | grep -oP '(?<=<title>).*?(?=</title>)' | head -1"),
    ("6. JSON-LD on homepage", "curl -s https://skillxm.cn/ 2>/dev/null | grep -c 'application/ld+json'"),
    ("7. JSON-LD on article", "curl -s https://skillxm.cn/?p=800 2>/dev/null | grep -c 'application/ld+json'"),
    ("8. Meta description count", "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT COUNT(*) FROM wp_postmeta WHERE meta_key='_yoast_wpseo_metadesc'\""),
    ("9. Focus keyword count", "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT COUNT(*) FROM wp_postmeta WHERE meta_key='_yoast_wpseo_focuskw'\""),
    ("10. Total tags", "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT COUNT(DISTINCT t.term_id) FROM wp_terms t JOIN wp_term_taxonomy tt ON t.term_id=tt.term_id WHERE tt.taxonomy='post_tag'\""),
    ("11. Tag-post relationships", "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT COUNT(*) FROM wp_term_relationships tr JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id=tt.term_taxonomy_id WHERE tt.taxonomy='post_tag'\""),
    ("12. Yoast SEO active", "wp plugin is-active wordpress-seo --allow-root --path=/www/wwwroot/skillxm.cn/public/ 2>/dev/null"),
    ("13. Total published posts", "mysql -uwpuser -p'WpPass2024!' wp_skillxm -N -e \"SELECT COUNT(*) FROM wp_posts WHERE post_type='post' AND post_status='publish'\""),
]

for label, cmd in checks:
    print(flush=True)
    print("--- {} ---".format(label), flush=True)
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    print(out if out else "OK", flush=True)

ssh.close()
print("\n" + "=" * 50, flush=True)
print("VERIFICATION COMPLETE", flush=True)
print("=" * 50, flush=True)
