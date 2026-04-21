import paramiko, sys, json, os, time
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 获取去重后的文章列表（每篇只取一次）
cmd = """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "
SELECT DISTINCT p.ID, p.post_title,
    COALESCE((SELECT t.name FROM wp_terms t
        JOIN wp_term_taxonomy tt ON t.term_id = tt.term_id
        JOIN wp_term_relationships tr ON tr.term_taxonomy_id = tt.term_taxonomy_id
        WHERE tt.taxonomy='category' AND tr.object_id = p.ID
        ORDER BY tt.count DESC LIMIT 1), '未分类') as cat
FROM wp_posts p
WHERE p.post_type='post' AND p.post_status='publish'
    AND p.post_title != 'Hello world!'
ORDER BY p.ID ASC;
" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
raw = stdout.read().decode('utf-8', errors='ignore')

articles = []
seen = set()
for line in raw.strip().split('\n'):
    parts = line.split('\t')
    if len(parts) >= 3:
        pid = int(parts[0])
        if pid not in seen:
            seen.add(pid)
            articles.append({
                'id': pid,
                'title': parts[1].strip(),
                'category': parts[2].strip()
            })

print("去重后: %d 篇文章（已排除Hello world）" % len(articles))

# 保存
out_path = os.path.join(os.path.dirname(__file__), 'articles_clean.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

# 显示前10个标题作为样本
print("\n前10篇:")
for a in articles[:10]:
    print("  [%d] [%s] %s" % (a['id'], a['category'], a['title'][:50]))

# 分类统计
cats = {}
for a in articles:
    cats[a['category']] = cats.get(a['category'], 0) + 1
print("\n分类统计:")
for c, n in sorted(cats.items(), key=lambda x: -x[1]):
    print("  %s: %d" % (c, n))

print("\n保存到: %s" % out_path)
ssh.close()
