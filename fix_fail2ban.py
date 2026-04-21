import paramiko, time

server = '240b:4001:278:8402:0:bd18:bd09:af0d'
port = 22222  # 新端口！
user = 'root'
password = 'Langlang0.'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server, port=port, username=user, password=password,
               timeout=20, allow_agent=False, look_for_keys=False,
               banner_timeout=20, auth_timeout=20)

def cmd(c, timeout=60):
    stdin, stdout, stderr = client.exec_command(c, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

print('[1] 检查 fail2ban 运行状态...')
print(cmd('systemctl status fail2ban 2>&1 | head -20'))
print()
print('[2] 尝试手动启动...')
print(cmd('systemctl restart fail2ban 2>&1'))
time.sleep(3)
print(cmd('systemctl status fail2ban 2>&1 | head -10'))

print('\n[3] socket 检查...')
print(cmd('ls -la /var/run/fail2ban/ 2>/dev/null || echo "目录不存在"'))
print(cmd('cat /var/log/fail2ban/fail2ban.log 2>/dev/null | tail -20 || echo "无日志"'))

print('\n[4] 手动启动 fail2ban 进程...')
print(cmd('fail2ban-server -b -s /var/run/fail2ban/fail2ban.sock 2>&1 &'))
time.sleep(3)
r = cmd('fail2ban-client status sshd 2>&1')
print('SSH jail:', r.strip()[:300] if r.strip() else '仍失败')

print('\n[5] 如果 fail2ban 仍失败，用 iptables 手动加规则...')
print('  (检查当前被封 IP)...')
print(cmd('iptables -L INPUT -n --line-numbers 2>/dev/null | grep -i fail2ban | head -10'))

print('\n[6] 测试 fail2ban 状态...')
r = cmd('fail2ban-client ping 2>&1')
print('  ping:', r.strip())

client.close()
