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
    s = client.exec_command(c, timeout=30)
    return s[0].read().decode('utf-8', errors='replace') + s[2].read().decode('utf-8', errors='replace')

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
print(cmd('cat /proc/sys/net/core/somaxconn'))
print(cmd('cat /proc/sys/net/ipv4/tcp_max_syn_backlog'))
print(cmd('cat /proc/sys/net/ipv4/ip_local_port_range'))
print(cmd('cat /proc/sys/net/core/netdev_max_backlog'))
print(cmd('cat /proc/sys/net/core/rmem_max'))
print(cmd('cat /proc/sys/net/core/wmem_max'))

print('\n=== Installed Software ===')
print(cmd('which nginx caddy haproxy apache2 2>/dev/null'))
print(cmd('nginx -v 2>&1; caddy version 2>&1; httpd -v 2>&1'))

print('\n=== Kernel BBR ===')
print(cmd('sysctl net.ipv4.tcp_congestion_control 2>/dev/null'))
print(cmd('ls /lib/modules/$(uname -r)/kernel/net/ipv4/tcp_bbr.ko 2>/dev/null && echo "BBR module exists"'))

print('\n=== OS Version ===')
print(cmd('cat /etc/os-release'))

client.close()
print('\n[Done]')
