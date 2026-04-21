import paramiko
import time

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect('43.103.5.46', username='root', password='l95UE5ysF)7.gR', allow_agent=False, look_for_keys=False)

# Create website directory
print("=== 创建网站目录 ===")
stdin, out, err = c.exec_command('mkdir -p /www/wwwroot/skillxm.cn/public')
print(out.read().decode())

# Create test index.html
print("=== 创建测试页面 ===")
test_html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>极创网 - 资源站</title>
</head>
<body>
    <h1>🎉 网站测试成功！</h1>
    <p>服务器: skillxm.cn</p>
    <p>状态: 运行中</p>
</body>
</html>'''
stdin, out, err = c.exec_command('cat > /www/wwwroot/skillxm.cn/public/index.html << \'EOF\'\n' + test_html + '\nEOF')
print(out.read().decode())

# Create Nginx config
print("=== 创建Nginx配置 ===")
nginx_conf = '''server {
    listen 80;
    server_name skillxm.cn www.skillxm.cn 43.103.5.46;
    
    root /www/wwwroot/skillxm.cn/public;
    index index.html index.htm index.php;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    access_log /www/wwwlogs/skillxm.cn.log;
    error_log /www/wwwlogs/skillxm.cn.error.log;
}'''

stdin, out, err = c.exec_command('cat > /etc/nginx/sites-available/skillxm.cn.conf << \'EOF\'\n' + nginx_conf + '\nEOF')
print(out.read().decode())

# Enable site
print("=== 启用站点 ===")
stdin, out, err = c.exec_command('ln -sf /etc/nginx/sites-available/skillxm.cn.conf /etc/nginx/sites-enabled/ && nginx -t')
print(out.read().decode())

# Reload Nginx
print("=== 重载Nginx ===")
stdin, out, err = c.exec_command('systemctl reload nginx')
print(out.read().decode())

# Check status
print("=== 检查网站 ===")
stdin, out, err = c.exec_command('curl -s -o /dev/null -w "%{http_code}" http://localhost/')
print('HTTP Status:', out.read().decode().strip())

c.close()

print("\n✅ 网站创建完成！")
print("访问: http://43.103.5.46/ 或 http://skillxm.cn/")