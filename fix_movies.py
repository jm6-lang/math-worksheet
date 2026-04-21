import subprocess, base64

# Check music directory contents
result = subprocess.run(['gh', 'api', 'repos/jm6-lang/resource-portal/contents/docs/music', '--jq', '.[] | .name'], capture_output=True, text=True, encoding='utf-8', errors='replace')
names = result.stdout.strip().split('\n')
print(f'Music has {len(names)} items')
music_posts = [n for n in names if n.startswith('post_')]
print(f'Post files: {len(music_posts)}')

# For each garbled movie post (129-144), find corresponding music post
# The commit was "音乐资源迁移到影视聚集区"
# Let's check the commit that created the garbled files
sha = 'e15e743e6f1b355fdb2f807749ed12d3c5ba5ce5'
result2 = subprocess.run(['gh', 'api', f'repos/jm6-lang/resource-portal/commits?path=docs/movies/post_129.md&per_page=5', '--jq', '.[].sha'], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('Commits for post_129:', result2.stdout.strip())

# Let's also check the music files in the same commit to get original titles
# The music/ directory might have been processed in a different commit
# Let's try to get the original content from the parent commit of e15e743
result3 = subprocess.run(['gh', 'api', f'repos/jm6-lang/resource-portal/git/commits/e15e743e6f1b355fdb2f807749ed12d3c5ba5ce5', '--jq', '.parents[0].sha'], capture_output=True, text=True, encoding='utf-8', errors='replace')
parent_sha = result3.stdout.strip()
print(f'Parent commit: {parent_sha}')
