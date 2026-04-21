import subprocess, time

repo = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal'

for attempt in range(5):
    time.sleep(5)
    print('Attempt', attempt + 1, '...')
    r = subprocess.run(['git', 'push'], cwd=repo, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.returncode == 0:
        print('Push OK!')
        print(r.stdout[:200])
        break
    else:
        print('Failed:', r.stderr[:100])
        time.sleep(5)
