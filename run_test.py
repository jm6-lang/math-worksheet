import paramiko, sys, traceback
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('240b:4001:278:8402:0:bd18:bd09:af0d', 22, 'root', 'l95UE5ysF)7.gR', timeout=15)
    _, o, e = client.exec_command(
        'rm -f /www/wwwroot/resource_site/auto_collect/collector.lock && '
        'cd /www/wwwroot/resource_site/auto_collect && '
        'timeout 150 python3 collector.py 2>&1', timeout=180)
    out = o.read().decode('utf-8', errors='replace')
    err = e.read().decode('utf-8', errors='replace')
    if out:
        print(out[-4000:] if len(out) > 4000 else out)
    if err:
        print('STDERR:', err[-1000:])
    client.close()
except Exception as ex:
    traceback.print_exc()
