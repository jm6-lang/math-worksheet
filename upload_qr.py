import subprocess, base64

REPO = 'jm6-lang/resource-portal'
src = r'C:\Users\Administrator\Desktop\新建文件夹\9951d3ac2a60b345235b026e181af1c.jpg'
dst = 'docs/public/data-card-qr.png'

r = subprocess.run(['gh', 'api', f'repos/{REPO}/contents/{dst}?ref=main', '--jq', '.sha'],
                   capture_output=True, text=True, timeout=10)
sha = r.stdout.strip() if r.returncode == 0 else ''
print('sha:', sha[:8] if sha else 'none')

b64 = base64.b64encode(open(src, 'rb').read()).decode()
msg = 'chore: 替换大流量卡二维码图片'
cmd = ['gh', 'api', f'repos/{REPO}/contents/{dst}',
       '--method', 'PUT',
       '--field', f'message={msg}',
       '--field', f'content={b64}']
if sha:
    cmd += ['--field', f'sha={sha}']

r2 = subprocess.run(cmd, capture_output=True, text=True, timeout=30, encoding='utf-8')
if r2.returncode == 0:
    print('OK - pushed successfully')
else:
    print('FAIL:', r2.stderr[:200])
