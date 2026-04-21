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
print('[OK] Connected!')

def cmd(c):
    stdin, stdout, stderr = client.exec_command(c, timeout=30)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

# 1. 开启 BBR
print('\n[1] 开启 BBR...')
r = cmd('echo "net.core.default_qdisc=fq_codel\nnet.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf && sysctl -p')
print(r)

# 2. 调大 buffer 和端口范围
print('\n[2] 调大网络参数...')
sysctl_cmds = [
    'sysctl -w net.core.rmem_max=134217728',
    'sysctl -w net.core.wmem_max=134217728',
    'sysctl -w net.ipv4.tcp_rmem="4096 87380 134217728"',
    'sysctl -w net.ipv4.tcp_wmem="4096 16384 134217728"',
    'sysctl -w net.ipv4.tcp_max_syn_backlog=4096',
    'sysctl -w net.core.somaxconn=4096',
    'sysctl -w net.core.netdev_max_backlog=5000',
    'sysctl -w net.ipv4.ip_local_port_range="10240 65535"',
    'sysctl -w net.ipv4.tcp_fastopen=3',
    'sysctl -w net.ipv4.tcp_fin_timeout=15',
    'sysctl -w net.ipv4.tcp_keepalive_time=600',
    'sysctl -w net.ipv4.tcp_keepalive_intvl=30',
    'sysctl -w net.ipv4.tcp_keepalive_probes=3',
    'sysctl -w net.ipv4.tcp_slow_start_after_idle=0',
    'sysctl -w net.core.optmem_max=65536',
]
for c in sysctl_cmds:
    r = cmd(c)
    if 'error' in r.lower() or 'permission' in r.lower():
        print('FAIL: ' + c + ' -> ' + r.strip())
    else:
        print('OK: ' + c)

# 3. 优化 DNS（改成 Cloudflare DNS）
print('\n[3] 优化 DNS...')
r = cmd('mkdir -p /etc/systemd/resolved.conf.d/ && echo -e "[Resolve]\nDNS=1.1.1.1 8.8.8.8\nDNSOverTLS=opportunistic" > /etc/systemd/resolved.conf.d/dns.conf && systemctl restart systemd-resolved')
print(r)
print(cmd('cat /etc/resolv.conf'))

# 4. 验证 BBR 开启
print('\n[4] 验证 BBR...')
print(cmd('sysctl net.ipv4.tcp_congestion_control'))
print(cmd('lsmod | grep bbr'))

# 5. 验证参数
print('\n[5] 验证参数...')
for f in ['net.core.rmem_max', 'net.core.wmem_max', 'net.ipv4.tcp_max_syn_backlog',
          'net.core.somaxconn', 'net.core.netdev_max_backlog', 'net.ipv4.ip_local_port_range',
          'net.ipv4.tcp_congestion_control', 'net.ipv4.tcp_fastopen']:
    print(f + ' = ' + cmd('sysctl -n ' + f).strip())

# 6. 延迟测试（对比优化前后）
print('\n[6] 优化后延迟测试...')
print(cmd('curl -s -w "Google: dns=%{time_namelookup}s conn=%{time_connect}s ttfb=%{time_starttransfer}s total=%{time_total}s\n" -o /dev/null https://www.google.com --max-time 15'))
print(cmd('curl -s -w "Baidu: dns=%{time_namelookup}s conn=%{time_connect}s ttfb=%{time_starttransfer}s total=%{time_total}s\n" -o /dev/null https://www.baidu.com --max-time 10'))
print(cmd('curl -s -w "Github: dns=%{time_namelookup}s conn=%{time_connect}s ttfb=%{time_starttransfer}s total=%{time_total}s\n" -o /dev/null https://github.com --max-time 15'))

client.close()
print('\n[完成]')
