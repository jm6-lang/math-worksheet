"""
文章重写协调器 - 读取文章列表，启动subagent批量生成原创内容
每个subagent处理一批文章，生成后通过SSH直接更新到数据库
"""
import json, os, sys, subprocess

sys.stdout.reconfigure(encoding='utf-8')

# 读取文章列表
base = os.path.dirname(__file__)
with open(os.path.join(base, 'articles_clean.json'), 'r', encoding='utf-8') as f:
    all_articles = json.load(f)

print("总文章数: %d" % len(all_articles))

# 按分类分组
categories = {}
for a in all_articles:
    cat = a['category'] if a['category'] not in ['Uncategorized', '未分类'] else '网赚项目'
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(a)

print("\n分类分布:")
for cat, articles in sorted(categories.items(), key=lambda x: -len(x[1])):
    print("  %s: %d篇" % (cat, len(articles)))

# 保存分组后的文件
for cat, articles in categories.items():
    safe_name = cat.replace('/', '_')
    out_file = os.path.join(base, 'batch_%s.json' % safe_name)
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print("  Saved: %s (%d篇)" % (out_file, len(articles)))

print("\n准备启动subagent，每个处理一个分类的文章...")
print("按分类启动subagent:")
for cat in sorted(categories.keys()):
    print("  - %s: %d篇" % (cat, len(categories[cat])))
