import paramiko

server = '240b:4001:278:8402:0:bd18:bd09:af0d'
port = 22
user = 'root'
password = 'Langlang0.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server, port=port, username=user, password=password,
               timeout=20, allow_agent=False, look_for_keys=False,
               banner_timeout=20, auth_timeout=20)

def cmd(c):
    stdin, stdout, stderr = client.exec_command(c, timeout=30)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# 检查所有 nginx 配置文件
print('[1] 查找所有包含 skillxm.cn 的配置 ...')
print(cmd('grep -r "skillxm.cn" /etc/nginx/ 2>/dev/null'))

# 检查 default site
print('\n[2] 检查 default site ...')
print(cmd('cat /etc/nginx/sites-enabled/default 2>/dev/null || echo "无 default site"'))

# 检查是否有 default.conf
print('\n[3] conf.d 下所有文件 ...')
print(cmd('ls -la /etc/nginx/conf.d/'))

# 移除无用的 default site（如果有）
print('\n[4] 清理冲突 ...')
# 如果 sites-enabled 里有 default 且没有 skillxm.cn，禁用它
r = cmd('ls /etc/nginx/sites-enabled/')
print(r)

# 最终验证
print('\n[5] 验证配置是否正确 ...')
print(cmd('nginx -t 2>&1'))
print(cmd('systemctl reload nginx 2>&1'))
print(cmd('systemctl status nginx | head -4'))

# 测试静态资源缓存头
print('\n[6] 测试静态资源响应头（检查缓存是否生效）...')
# 找一个实际存在的静态资源
print(cmd('curl -sI https://skillxm.cn/ --max-time 10 | grep -E "Cache-Control|Content-Type|X-Frame|X-XSS|X-Content"'))
print(cmd('curl -sI "https://skillxm.cn/favicon.ico" --max-time 10 2>/dev/null | head -8 || echo "favicon.ico 不存在"'))

# 最终网络状态确认
print('\n[7] 当前网络参数最终状态 ...')
for p in ['net.ipv4.tcp_congestion_control', 'net.core.default_qdisc', 'net.core.rmem_max',
          'net.core.wmem_max', 'net.ipv4.tcp_max_syn_backlog', 'net.core.somaxconn',
          'net.ipv4.ip_local_port_range', 'net.ipv4.tcp_fastopen']:
    print('  ' + p + ' = ' + cmd('sysctl -n ' + p).strip())

client.close()
print('\n[完成]')
