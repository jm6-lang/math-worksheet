import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 部署天空采集器 (SkyCAiji) ===\n")

# 1. 创建安装目录
print("1. 创建安装目录...")
ssh.exec_command("mkdir -p /www/wwwroot/skycaiji", timeout=10)
print("   目录已创建: /www/wwwroot/skycaiji")

# 2. 下载最新版本
print("\n2. 下载天空采集器源码...")
cmd = "cd /www/wwwroot/skycaiji && curl -sL 'https://github.com/zorlan/skycaiji/archive/refs/heads/main.zip' -o skycaiji.zip 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=60)
result = stdout.read().decode().strip()
print(f"   下载完成")

# 检查文件
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/skycaiji/", timeout=10)
print("\n3. 文件列表:")
print(stdout.read().decode().strip())

# 如果下载的是main分支的zip，需要解压
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/skycaiji && unzip -o skycaiji.zip 2>&1 | tail -20", timeout=30)
print("\n4. 解压结果:")
print(stdout.read().decode().strip())

# 检查解压后的内容
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/skycaiji/", timeout=10)
print("\n5. 解压后文件列表:")
print(stdout.read().decode().strip())

# 移动文件到正确位置
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/skycaiji && if [ -d 'skycaiji-main' ]; then mv skycaiji-main/* . && mv skycaiji-main/.[!.]* . 2>/dev/null; rmdir skycaiji-main; fi", timeout=10)
stdin, stdout, stderr = ssh.exec_command("ls -la /www/wwwroot/skycaiji/", timeout=10)
print("\n6. 整理后文件列表:")
print(stdout.read().decode().strip())

# 设置权限
stdin, stdout, stderr = ssh.exec_command("chmod -R 755 /www/wwwroot/skycaiji && chmod -R 777 /www/wwwroot/skycaiji/runtime /www/wwwroot/skycaiji/public/uploads 2>/dev/null", timeout=10)
print("\n7. 权限设置完成")

# 检查PHP版本
stdin, stdout, stderr = ssh.exec_command("php -v | head -1", timeout=10)
print("\n8. PHP版本:", stdout.read().decode().strip())

# 复制到网站目录并配置Nginx
print("\n9. 配置Nginx...")
nginx_config = """server {
    listen 80;
    server_name skycaiji.skillxm.cn;
    root /www/wwwroot/skycaiji;
    index index.php index.html;
    
    client_max_body_size 100M;
    
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    
    location ~ \\.php$ {
        fastcgi_pass unix:/run/php/php8.1-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
    
    location ~ /\\.ht {
        deny all;
    }
}
"""

sftp = ssh.open_sftp()
with sftp.open('/etc/nginx/sites-available/skycaiji.conf', 'w') as f:
    f.write(nginx_config)
sftp.close()

# 启用站点
stdin, stdout, stderr = ssh.exec_command("ln -sf /etc/nginx/sites-available/skycaiji.conf /etc/nginx/sites-enabled/skycaiji.conf && nginx -t 2>&1", timeout=10)
print("   Nginx配置测试:", stdout.read().decode().strip())

# 重载Nginx
stdin, stdout, stderr = ssh.exec_command("nginx -s reload 2>&1", timeout=10)
print("   Nginx重载:", stdout.read().decode().strip() or "成功")

print("\n=== 天空采集器安装完成 ===")
print("\n访问地址: http://skycaiji.skillxm.cn")
print("如需独立域名，请配置DNS解析")

ssh.close()
