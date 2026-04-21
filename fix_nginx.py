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

print('[1] 删除旧 speed.conf，重新写入（去掉与 nginx.conf 重复的指令）...')

# 写入新的 speed.conf（只保留 server 块内有效的指令，不重复 gzip）
new_conf = """# Nginx 速度优化 - 补充配置
# 仅包含 server 块内有效的指令

# 静态资源长期缓存
location ~* \\.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot|webp|mp4|webm)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
    access_log off;
}

# 针对 HTML 的缓存（1天）
location ~* \\.html?$ {
    expires 1d;
    add_header Cache-Control "no-cache, must-revalidate";
}

# 开启 FastCGI 缓存（减少 PHP 重复解析）
# 如果用的是 WordPress/Typecho，可以开启这个
# 注意：需要先在 nginx.conf http 块定义 fastcgi_cache_path
# 此处暂时不开启，避免对动态站造成问题
"""

cmd('cat > /etc/nginx/conf.d/speed.conf << \'EOF\'\n' + new_conf + 'EOF')

print('[2] 补充 nginx.conf 中缺失的 gzip_types（image/svg+xml 等）...')
# 在 gzip_types 那行追加缺少的类型
r = cmd("sed -i 's/gzip_types text\\/plain text\\/css application\\/json application\\/javascript text\\/xml application\\/xml application\\/xml\\+rss text\\/javascript;/gzip_types text\\/plain text\\/css application\\/json application\\/javascript text\\/xml application\\/xml application\\/xml\\+rss text\\/javascript application\\/rss\\+xml application\\/atom\\+xml image\\/svg\\+xml;/' /etc/nginx/nginx.conf")
print(r)

# 添加 gzip_min_length（如果没有的话）
r = cmd("grep -q 'gzip_min_length' /etc/nginx/nginx.conf && echo 'gzip_min_length 已存在' || sed -i '/gzip_types/i\\    gzip_min_length 1024;' /etc/nginx/nginx.conf")
print(r)

# 验证修改
print('\n[3] 验证 gzip 配置...')
print(cmd("grep -A5 'Gzip Settings' /etc/nginx/nginx.conf"))

print('\n[4] 测试 Nginx 配置语法...')
print(cmd('nginx -t 2>&1'))

print('\n[5] 重载 Nginx...')
print(cmd('nginx -s reload 2>&1'))

print('\n[6] 查看最终状态...')
print(cmd('systemctl status nginx | head -5'))
print(cmd('curl -sI -H "Accept-Encoding: gzip" https://skillxm.cn/ --max-time 10 | grep -E "Content-Encoding|Content-Type|Cache-Control|X-Cache"'))

# 延迟测试
print('\n[7] 最终延迟测试...')
for i in range(3):
    g = cmd('curl -s -w "Google: %{time_namelookup}s | %{time_connect}s | %{time_starttransfer}s | %{time_total}s\n" -o /dev/null https://www.google.com --max-time 15')
    b = cmd('curl -s -w "Baidu:  %{time_namelookup}s | %{time_connect}s | %{time_starttransfer}s | %{time_total}s\n" -o /dev/null https://www.baidu.com --max-time 15')
    s = cmd('curl -s -w "SkillX: %{time_namelookup}s | %{time_connect}s | %{time_starttransfer}s | %{time_total}s\n" -o /dev/null https://skillxm.cn/ --max-time 15 -L')
    print('轮次' + str(i+1) + ':')
    print('  ' + g.strip())
    print('  ' + b.strip())
    print('  ' + s.strip())

print('\n[完成]')
client.close()
