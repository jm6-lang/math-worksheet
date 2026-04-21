import paramiko, sys, json, os
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# 导出所有文章 ID, 标题, 分类, 当前内容长度
cmd = """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "
SELECT p.ID, p.post_title, COALESCE(t.name,'未分类'), LENGTH(p.post_content)
FROM wp_posts p
LEFT JOIN wp_term_relationships tr ON p.ID = tr.object_id
LEFT JOIN wp_term_taxonomy tt ON tr.term_taxonomy_id = tt.term_taxonomy_id AND tt.taxonomy='category'
LEFT JOIN wp_terms t ON tt.term_id = t.term_id
WHERE p.post_type='post' AND p.post_status='publish'
ORDER BY p.ID ASC;
" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
raw = stdout.read().decode('utf-8', errors='ignore')

articles = []
for line in raw.strip().split('\n'):
    parts = line.split('\t')
    if len(parts) >= 4:
        articles.append({
            'id': int(parts[0]),
            'title': parts[1].strip(),
            'category': parts[2].strip() if parts[2].strip() else '未分类',
            'content_len': int(parts[3])
        })

print("导出完成: %d 篇文章" % len(articles))

# 保存到本地
out_path = os.path.join(os.path.dirname(__file__), 'articles_data.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

# 统计
cats = {}
for a in articles:
    c = a['category']
    cats[c] = cats.get(c, 0) + 1

print("\n按分类统计:")
for c, n in sorted(cats.items(), key=lambda x: -x[1]):
    print("  %s: %d篇" % (c, n))

# 内容长度统计
lengths = [a['content_len'] for a in articles]
print("\n当前内容长度: 最短%d字, 最长%d字, 平均%d字" % (
    min(lengths), max(lengths), sum(lengths)//len(lengths)
))

print("\n数据已保存: %s" % out_path)

ssh.close()
