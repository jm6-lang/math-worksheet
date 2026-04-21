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

# 7. Nginx 优化
print('[7] Nginx 配置优化...')
nginx_conf = '''# Nginx 网络优化配置片段
# 在 server{} 块中或 /etc/nginx/conf.d/ 目录下添加

# 开启 gzip（减少传输体积）
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_proxied any;
gzip_types text/plain text/css text/xml application/json application/javascript application/rss+xml application/atom+xml image/svg+xml;
gzip_disable "MSIE [1-6]\\.";

# 连接复用（HTTP/1.1 KeepAlive）
keepalive_timeout 65;
keepalive_requests 1000;

# 缓冲区优化
client_body_buffer_size 16k;
client_header_buffer_size 1k;
large_client_header_buffers 4 8k;
client_max_body_size 20m;

# 超时优化
client_body_timeout 12;
client_header_timeout 12;
send_timeout 10;

# TCP 优化
tcp_nopush on;
tcp_nodelay on;

# 静态资源缓存
location ~* \\.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}

# 禁用日志（可选，减少 IO）
access_log off;
'''
print(cmd('cat > /tmp/nginx_network.conf << \'NGINXEOF\'\n' + nginx_conf + 'NGINXEOF'))
print(cmd('cat /tmp/nginx_network.conf'))

# 检查现有 nginx.conf
print('\n当前 nginx.conf 关键部分：')
print(cmd('grep -E "^(worker_connections|worker_rlimit|gzip|keepalive)" /etc/nginx/nginx.conf /etc/nginx/conf.d/*.conf 2>/dev/null'))

# 测试 nginx 语法
print('\n测试 nginx 配置语法...')
print(cmd('nginx -t 2>&1'))

# 如果用户想要，可以给出完整建议
print('\n建议添加到 /etc/nginx/conf.d/speed.conf：')
print(nginx_conf)

# 8. Nginx 重新加载
print('\n[8] 重载 Nginx 配置...')
print(cmd('nginx -s reload 2>&1'))

# 9. 最终全面延迟测试（多测几次）
print('\n[9] 多轮延迟测试（取最优值）...')
for i in range(3):
    g = cmd('curl -s -w "Google: %{time_namelookup}s | %{time_connect}s | %{time_starttransfer}s | %{time_total}s\n" -o /dev/null https://www.google.com --max-time 15')
    b = cmd('curl -s -w "Baidu:  %{time_namelookup}s | %{time_connect}s | %{time_starttransfer}s | %{time_total}s\n" -o /dev/null https://www.baidu.com --max-time 15')
    print(f'轮次{i+1}: ' + g.strip() + '  ' + b.strip())

# 10. 综合报告
print('\n========== 优化总结 ==========')
print('BBR 拥塞控制: ' + cmd('sysctl -n net.ipv4.tcp_congestion_control').strip())
print('默认队列算法: ' + cmd('sysctl -n net.core.default_qdisc').strip())
print('rmem_max:     ' + cmd('sysctl -n net.core.rmem_max').strip())
print('wmem_max:     ' + cmd('sysctl -n net.core.wmem_max').strip())
print('tcp_max_syn_backlog: ' + cmd('sysctl -n net.ipv4.tcp_max_syn_backlog').strip())
print('somaxconn:    ' + cmd('sysctl -n net.core.somaxconn').strip())
print('端口范围:     ' + cmd('sysctl -n net.ipv4.ip_local_port_range').strip())
print('netdev_max_backlog:   ' + cmd('sysctl -n net.core.netdev_max_backlog').strip())
print('tcp_fastopen: ' + cmd('sysctl -n net.ipv4.tcp_fastopen').strip())
print('nginx 版本:   ' + cmd('nginx -v 2>&1').strip())
print('nginx 状态:   ' + cmd('systemctl is-active nginx').strip())

client.close()
print('\n[全部完成]')
