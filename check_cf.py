import paramiko
import subprocess

server = '240b:4001:278:8402:0:bd18:bd09:af0d'
port = 22
user = 'root'
password = 'Langlang0.'

# 从本地 Windows 测试访问
print('[本地测试] 检查 Cloudflare 是否生效 ...')

# 用 curl 测试响应头（从 Windows 本地）
result = subprocess.run(
    ['curl', '-sI', 'https://skillxm.cn/', '--max-time', '15'],
    capture_output=True, text=True, timeout=20
)
print(result.stdout)
print(result.stderr)

# 检查是否有 CF-Ray header（Cloudflare 特征）
if 'cf-ray' in result.stdout.lower():
    print('\n✅ Cloudflare 已生效！看到 CF-Ray 响应头')
else:
    print('\n⚠️ 未检测到 CF-Ray，可能 Cloudflare 代理未完全生效')

# SSH 到服务器检查源站是否正常
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server, port=port, username=user, password=password,
               timeout=20, allow_agent=False, look_for_keys=False)

def cmd(c):
    stdin, stdout, stderr = client.exec_command(c, timeout=30)
    return stdout.read().decode('utf-8', errors='replace')

print('\n[服务器端] 检查源站访问 ...')
print(cmd('curl -sI http://127.0.0.1/ | head -5'))
print(cmd('curl -sI https://127.0.0.1/ -k | head -5'))

# 检查 Nginx 是否看到真实 IP
print('\n[Nginx 日志] 最近访问 ...')
print(cmd('tail -3 /var/log/nginx/access.log 2>/dev/null || echo "日志路径可能不同"'))

client.close()
