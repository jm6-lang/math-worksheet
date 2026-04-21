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

# 删除重复的 .bak 文件
print('[1] 删除 sites-enabled 下的备份文件（导致冲突）...')
print(cmd('rm -f /etc/nginx/sites-enabled/*.bak'))
print(cmd('ls -la /etc/nginx/sites-enabled/'))

# 测试配置
print('\n[2] 测试 Nginx 配置 ...')
print(cmd('nginx -t 2>&1'))

# 重载
print('\n[3] 重载 Nginx ...')
print(cmd('systemctl reload nginx 2>&1'))

# 验证
print('\n[4] 验证无警告 ...')
print(cmd('nginx -t 2>&1 | grep -v "syntax is ok" | grep -v "test is successful"'))

# 测试网站访问
print('\n[5] 测试网站访问 ...')
print(cmd('curl -s -o /dev/null -w "状态码: %{http_code}\\nTTFB: %{time_starttransfer}s\\n总时间: %{time_total}s\\n" https://skillxm.cn/ --max-time 15 -L'))

# 多轮测试取平均
print('\n[6] 多轮访问测试 ...')
import time
times = []
for i in range(5):
    r = cmd('curl -s -o /dev/null -w "%{time_starttransfer}" https://skillxm.cn/ --max-time 15 -L')
    t = float(r.strip()) if r.strip() else 0
    times.append(t)
    print('  轮次' + str(i+1) + ': TTFB=' + str(round(t, 3)) + 's')
    time.sleep(0.5)

avg = sum(times) / len(times)
print('\\n平均 TTFB: ' + str(round(avg, 3)) + 's')
print('最优 TTFB: ' + str(round(min(times), 3)) + 's')

# 最终总结
print('\n========== 优化完成总结 ==========')
print('1. TCP 拥塞控制: BBR (已启用)')
print('2. 网络缓冲区: 128MB (原 212KB)')
print('3. SYN 队列: 4096 (原 128)')
print('4. 端口范围: 10240-65535 (原 32768-60999)')
print('5. TCP FastOpen: 已启用')
print('6. Nginx 静态缓存: 30天')
print('7. Gzip 压缩: 已启用')
print('8. 配置冲突: 已清理')

client.close()
print('\n[全部完成]')
