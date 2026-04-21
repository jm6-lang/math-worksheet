import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 更新Nginx配置添加采集器 ===\n")

# 1. 读取完整配置
print("1. 读取配置...")
cmd = """cat /etc/nginx/sites-available/resource_site.conf"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
config = stdout.read().decode().strip()

# 2. 在第一个server块（HTTP重定向）后面插入采集器配置
caiji_config = '''
    # 天空采集器子目录
    location ^~ /caiji/ {
        alias /www/wwwroot/skycaiji/public/;
        index index.php index.html;
        
        location ~ \\.php$ {
            fastcgi_pass unix:/run/php/php8.1-fpm.sock;
            fastcgi_index index.php;
            fastcgi_param SCRIPT_FILENAME $request_filename;
            include fastcgi_params;
        }
        
        location ~* \\.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf)$ {
            expires 7d;
            add_header Cache-Control "public";
        }
    }
    
    # 采集器API接口
    location ^~ /caijiapi/ {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
'''

# 在第一个server块结束前插入
if "location ^~ /caiji/" not in config:
    # 找到第一个server块的结束位置
    lines = config.split('\n')
    new_lines = []
    brace_count = 0
    inserted = False
    
    for line in lines:
        new_lines.append(line)
        brace_count += line.count('{') - line.count('}')
        
        # 在第一个server块的第一个location之后插入
        if not inserted and brace_count == 1 and line.strip().startswith('location'):
            new_lines.append(caiji_config)
            inserted = True
    
    config = '\n'.join(new_lines)

# 3. 写回配置
sftp = ssh.open_sftp()
with sftp.open('/etc/nginx/sites-available/resource_site.conf', 'w') as f:
    f.write(config)
sftp.close()
print("   配置已更新")

# 4. 测试Nginx
print("\n2. 测试Nginx配置...")
stdin, stdout, stderr = ssh.exec_command("nginx -t 2>&1", timeout=10)
result = stdout.read().decode().strip()
print("   ", result)

# 5. 重载Nginx
print("\n3. 重载Nginx...")
stdin, stdout, stderr = ssh.exec_command("nginx -s reload 2>&1", timeout=10)
print("   ", stdout.read().decode().strip() or "成功")

# 6. 测试访问采集器
print("\n4. 测试访问...")
cmd = """curl -sL --max-time 10 'https://www.skillxm.cn/caiji/' -k 2>/dev/null | head -50"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore').strip()
print(content[:500])

ssh.close()
