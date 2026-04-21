import subprocess, json, sys

sys.stdout.reconfigure(encoding='utf-8')

result = subprocess.run(
    ['node', 'E:/Qclaw/resources/openclaw/config/skills/online-search/scripts/prosearch.cjs',
     json.dumps({'keyword': 'site:skillxm.cn'})],
    capture_output=True, timeout=15
)
stdout = result.stdout.decode('utf-8', errors='ignore')
stderr = result.stderr.decode('utf-8', errors='ignore')

try:
    data = json.loads(stdout)
    print(json.dumps(data, ensure_ascii=False, indent=2))
except:
    print("Raw output:", stdout[:500])
    if stderr:
        print("Stderr:", stderr[:200])
