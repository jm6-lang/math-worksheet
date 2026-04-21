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

# 写入 Nginx 速度优化配置
nginx_speed_conf = """# Nginx 速度优化配置
# 写入 /etc/nginx/conf.d/speed.conf

gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_proxied any;
gzip_comp_level 5;
gzip_types text/plain text/css text/xml application/json application/javascript application/rss+xml application/atom+xml image/svg+xml;

keepalive_timeout 65;
keepalive_requests 1000;

tcp_nopush on;
tcp_nodelay on;

client_body_buffer_size 16k;
client_header_buffer_size 1k;
large_client_header_buffers 4 8k;
client_max_body_size 20m;

client_body_timeout 12;
client_header_timeout 12;
send_timeout 10;

# 静态资源 30 天缓存
location ~* \\.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot|webp)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
"""

# 写入文件
print('[1] 写入 Nginx 配置到 /etc/nginx/conf.d/speed.conf ...')
cmd("cat > /etc/nginx/conf.d/speed.conf << 'EOF'\n" + nginx_speed_conf + "EOF")
print(cmd('cat /etc/nginx/conf.d/speed.conf'))

# 测试语法
print('\n[2] 测试 Nginx 配置语法...')
print(cmd('nginx -t 2>&1'))

# 重载 Nginx
print('\n[3] 重载 Nginx ...')
print(cmd('nginx -s reload 2>&1'))
print(cmd('systemctl reload nginx 2>&1'))
print(cmd('systemctl status nginx | head -5'))

# 验证 gzip 开启
print('\n[4] 验证 gzip 是否生效...')
print(cmd('curl -s -I -H "Accept-Encoding: gzip" https://www.google.com 2>/dev/null | head -5 || echo "外部网络测试"'))

# 最终多轮延迟测试
print('\n[5] 最终延迟测试（3轮取最优）...')
for i in range(3):
    g = cmd('curl -s -w "Google: %{time_namelookup}s | %{time_connect}s | %{time_starttransfer}s | %{time_total}s\n" -o /dev/null https://www.google.com --max-time 15')
    b = cmd('curl -s -w "Baidu:  %{time_namelookup}s | %{time_connect}s | %{time_starttransfer}s | %{time_total}s\n" -o /dev/null https://www.baidu.com --max-time 15')
    print('轮次' + str(i+1) + ': ' + g.strip() + '  ' + b.strip())

client.close()
print('\n[全部完成]')
