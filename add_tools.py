import subprocess

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal'

r = subprocess.run(['git', 'add', 'docs/tools/post_225.md'], cwd=repo)
r2 = subprocess.run(['git', 'commit', '-m', 'feat(tools): 添加易店助手（闲鱼自动发货）'], cwd=repo, capture_output=True, text=True, encoding='utf-8', errors='replace')
print('Commit:', r2.returncode, r2.stdout[:100])

for attempt in range(5):
    r3 = subprocess.run(['git', 'push'], cwd=repo, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
    if r3.returncode == 0:
        print('Push OK!')
        break
    print(f'Push failed: {r3.stderr[:60]}')
    import time; time.sleep(5)
else:
    print('All push attempts failed')
