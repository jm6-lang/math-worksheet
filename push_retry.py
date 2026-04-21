import subprocess, time

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal'

# Get the commit to push
r = subprocess.run(['git', 'log', '-1', '--format=%H'], cwd=repo, capture_output=True, text=True, encoding='utf-8', errors='replace')
sha = r.stdout.strip()
print('Commit SHA:', sha)

# Push via git with more retries
for attempt in range(8):
    print(f'Push attempt {attempt+1}...')
    r2 = subprocess.run(
        ['git', 'push', 'origin', 'main'],
        cwd=repo, capture_output=True, text=True, encoding='utf-8', errors='replace',
        timeout=30
    )
    if r2.returncode == 0:
        print('SUCCESS!')
        print(r2.stdout[:300])
        break
    print(f'  Failed: {r2.stderr[:80]}')
    time.sleep(8)
else:
    print('All attempts failed')
