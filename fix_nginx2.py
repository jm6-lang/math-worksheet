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

# 删除有问题的 speed.conf（只含 location，非法）
print('[1] 删除无效的 speed.conf ...')
print(cmd('rm -f /etc/nginx/conf.d/speed.conf'))

# 把静态缓存和超时优化直接注入到 resource_site.conf 两个 server 块里
print('\n[2] 备份原配置 ...')
print(cmd('cp /etc/nginx/sites-enabled/resource_site.conf /etc/nginx/sites-enabled/resource_site.conf.bak'))

# 追加到 resource_site.conf（在最后一个 } 之前插入）
inject = '''
    # ===== 速度优化 =====
    # 静态资源 30 天缓存
    location ~* \\.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot|webp|mp4|webm)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # HTML 缓存 1 天
    location ~* \\.html?$ {
        expires 1d;
        add_header Cache-Control "no-cache, must-revalidate";
    }

    # 代理超时优化
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
'''

# 用 sed 在最后一个 } 前插入（适用于单个 server 块追加）
# 先看看当前文件末尾
print('\n[3] 当前配置末尾 ...')
print(cmd('tail -10 /etc/nginx/sites-enabled/resource_site.conf'))

# 在文件末尾的 } 前插入（简单方式，直接追加到 } 之前）
print('\n[4] 追加优化配置到 80 端口 server 块 ...')
# 读取原文件，去掉末尾的 }，追加inject，再加 }
content = cmd('cat /etc/nginx/sites-enabled/resource_site.conf')
# 移除末尾的 } （可能有多个，移除最后一个）
lines = content.rstrip().split('\n')
# 找到最后一个 } 的位置
last_brace_idx = len(lines) - 1
while last_brace_idx >= 0 and lines[last_brace_idx].strip() != '}':
    last_brace_idx -= 1
if last_brace_idx >= 0:
    # 在最后一个 } 之前插入（只插入一次）
    # 这里比较复杂，用更简单的方法：直接替换整个文件
    pass

# 更简单的方式：直接用 python 构造完整的新文件
# 两个 server 块，需要在各自的末尾 } 前注入
# 由于两个 server 块结构类似，我们分别处理

new_content_80 = """server {
    listen 80;
    server_name skillxm.cn www.skillxm.cn;
    root /www/wwwroot/resource_site;
    index index.php index.html index.htm;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \\.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    # ===== 速度优化 =====
    location ~* \\.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot|webp|mp4|webm)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    location ~* \\.html?$ {
        expires 1d;
        add_header Cache-Control "no-cache, must-revalidate";
    }

    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}
"""

new_content_443 = """server {
    listen 443 ssl http2;
    server_name skillxm.cn www.skillxm.cn;
    
    ssl_certificate /etc/letsencrypt/live/skillxm.cn/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/skillxm.cn/privkey.pem;
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options nosniff;
    fastcgi_read_timeout 300;
    fastcgi_send_timeout 300;
    
    root /www/wwwroot/resource_site;
    index index.php index.html index.htm;

    client_max_body_size 50M;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~ \\.php$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    # ===== 速度优化 =====
    location ~* \\.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot|webp|mp4|webm)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    location ~* \\.html?$ {
        expires 1d;
        add_header Cache-Control "no-cache, must-revalidate";
    }

    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}
"""

new_conf = new_content_80 + '\n' + new_content_443

print('\n[5] 写入新配置 ...')
cmd('cat > /etc/nginx/sites-enabled/resource_site.conf << \'NGINXEOF\'\n' + new_conf + 'NGINXEOF')

print('\n[6] 测试 Nginx 配置语法 ...')
print(cmd('nginx -t 2>&1'))

print('\n[7] 重载 Nginx ...')
print(cmd('nginx -s reload 2>&1'))
print(cmd('systemctl status nginx | head -5'))

# 验证缓存头
print('\n[8] 验证缓存头生效 ...')
print(cmd('curl -sI https://skillxm.cn/ --max-time 10 | grep -E "Cache-Control|X-Cache|Content-Type|X-Server"'))

# 最终延迟测试
print('\n[9] 最终延迟测试（skillxm.cn 实际域名）...')
for i in range(3):
    s = cmd('curl -s -w "SkillX#{i}: dns=%{time_namelookup}s conn=%{time_connect}s ttfb=%{time_starttransfer}s total=%{time_total}s\\n" -o /dev/null https://skillxm.cn/ --max-time 15 -L')
    print(s.strip())

print('\n[完成]')
client.close()
