import paramiko

server = '240b:4001:278:8402:0:bd18:bd09:af0d'
port = 22
user = 'root'
password = 'Langlang0.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print('Connecting to %s ...' % server)
client.connect(server, port=port, username=user, password=password,
               timeout=20, allow_agent=False, look_for_keys=False,
               banner_timeout=20, auth_timeout=20)
print('[OK] Connected!')

def cmd(c):
    stdin, stdout, stderr = client.exec_command(c, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

print('\n=== System Info ===')
print(cmd('uname -a && uptime && free -h'))

print('\n=== Network Interfaces ===')
print(cmd('ip addr show'))

print('\n=== TCP Params ===')
print(cmd('sysctl -a 2>/dev/null | grep -E "^(net.ipv4.tcp|net.core|net.ipv4.ip_local_port_range)" | sort -u'))

print('\n=== DNS ===')
print(cmd('cat /etc/resolv.conf'))

print('\n=== Latency Test ===')
print(cmd('curl -s -w "Google: dns=%{time_namelookup}s conn=%{time_connect}s ttfb=%{time_starttransfer}s total=%{time_total}s\n" -o /dev/null https://www.google.com --max-time 15'))
print(cmd('curl -s -w "Baidu: dns=%{time_namelookup}s conn=%{time_connect}s ttfb=%{time_starttransfer}s total=%{time_total}s\n" -o /dev/null https://www.baidu.com --max-time 10'))
print(cmd('curl -s -w "Github: dns=%{time_namelookup}s conn=%{time_connect}s ttfb=%{time_starttransfer}s total=%{time_total}s\n" -o /dev/null https://github.com --max-time 15'))

print('\n=== Core Network Limits ===')
print('somaxconn:', cmd('cat /proc/sys/net/core/somaxconn').strip())
print('tcp_max_syn_backlog:', cmd('cat /proc/sys/net/ipv4/tcp_max_syn_backlog').strip())
print('ip_local_port_range:', cmd('cat /proc/sys/net/ipv4/ip_local_port_range').strip())
print('netdev_max_backlog:', cmd('cat /proc/sys/net/core/netdev_max_backlog').strip())
print('rmem_max:', cmd('cat /proc/sys/net/core/rmem_max').strip())
print('wmem_max:', cmd('cat /proc/sys/net/core/wmem_max').strip())

print('\n=== Web Server ===')
print(cmd('which nginx caddy apache2 httpd 2>/dev/null'))
print(cmd('nginx -v 2>&1; caddy version 2>&1; httpd -v 2>&1'))
print(cmd('systemctl status nginx 2>/dev/null | head -5; systemctl status caddy 2>/dev/null | head -5'))

print('\n=== BBR ===')
print(cmd('sysctl net.ipv4.tcp_congestion_control 2>/dev/null'))
print(cmd('ls /lib/modules/$(uname -r)/kernel/net/ipv4/tcp_bbr* 2>/dev/null && echo "BBR module found" || echo "BBR module not found"'))

print('\n=== OS Version ===')
print(cmd('cat /etc/os-release'))

print('\n=== IPv6 ===')
print(cmd('cat /proc/sys/net/ipv6/conf/all/disable_ipv6'))
print(cmd('ip -6 route show | head -5'))

client.close()
print('\n[Done]')
