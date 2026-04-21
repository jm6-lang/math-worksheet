import paramiko, time

server = '240b:4001:278:8402:0:bd18:bd09:af0d'
port = 22
user = 'root'
password = 'Langlang0.'
NEW_SSH_PORT = '22222'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(server, port=port, username=user, password=password,
               timeout=20, allow_agent=False, look_for_keys=False,
               banner_timeout=20, auth_timeout=20)

def cmd(c, timeout=60):
    stdin, stdout, stderr = client.exec_command(c, timeout=timeout)
    return stdout.read().decode('utf-8', errors='replace') + stderr.read().decode('utf-8', errors='replace')

print('=' * 55)
print('安全加固脚本开始')
print('=' * 55)

# ============ Step 1: 安装 fail2ban ============
print('\n[1/6] 安装 fail2ban...')
out = cmd('apt-get install -y fail2ban 2>&1', timeout=180)
if 'Unable to locate' in out or 'E: ' in out:
    print('  apt 失败，尝试 pip3...')
    out = cmd('pip3 install fail2ban 2>&1', timeout=120)
print('  结果:', out.strip()[-200:] if out.strip() else 'OK')

r = cmd('which fail2ban')
if r.strip():
    print('  fail2ban 已就绪，写入 jail 配置...')
    jail_conf = f'''[sshd]
enabled = true
port = {NEW_SSH_PORT}
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
'''
    cmd('mkdir -p /etc/fail2ban/jail.d')
    cmd('cat > /etc/fail2ban/jail.d/sshd.local << \'JAILEOF\'\n' + jail_conf + 'JAILEOF')
    cmd('systemctl enable fail2ban 2>/dev/null')
    cmd('systemctl restart fail2ban 2>&1')
    time.sleep(3)
    r = cmd('fail2ban-client status sshd 2>&1')
    print('  SSH jail 状态:', r.strip()[:250] if r.strip() else '(查询失败)')
else:
    print('  fail2ban 未安装成功，跳过')

# ============ Step 2: ufw 开放新端口 ============
print('\n[2/6] ufw 放行新端口 22222...')
print(' ', cmd('ufw allow ' + NEW_SSH_PORT + '/tcp comment SSH-New 2>&1').strip())

# ============ Step 3: 修改 SSH 端口 ============
print('\n[3/6] 修改 SSH 端口 22 -> ' + NEW_SSH_PORT + '...')

# 把 #Port 22 改成 Port 22222
r = cmd("sed -n 's/^#Port 22/Port " + NEW_SSH_PORT + "/p' /etc/ssh/sshd_config")
if r.strip():
    print('  找到注释的 Port 22，执行替换...')
    cmd("sed -i 's/^#Port 22/Port " + NEW_SSH_PORT + "/' /etc/ssh/sshd_config")
else:
    print('  未找到 #Port 22，直接追加 Port 行...')
    cmd("echo 'Port " + NEW_SSH_PORT + "' >> /etc/ssh/sshd_config")

# 验证
r = cmd("grep 'Port " + NEW_SSH_PORT + "' /etc/ssh/sshd_config").strip()
print('  Port ' + NEW_SSH_PORT + ' 配置:', r)

# 语法检查
r = cmd('sshd -t 2>&1')
if r.strip():
    print('  语法错误! 恢复备份...')
    cmd('cp /etc/ssh/sshd_config.bak /etc/ssh/sshd_config 2>/dev/null || echo "无备份需手动处理"')
else:
    print('  语法检查: OK')

# ============ Step 4: reload SSH（不断当前会话）===========
print('\n[4/6] reload SSH（不断开当前连接）...')
r = cmd('systemctl reload ssh 2>&1 || systemctl reload sshd 2>&1')
print('  结果:', r.strip() or '成功')

# 验证新端口已监听
time.sleep(2)
r = cmd('ss -tlnp | grep ' + NEW_SSH_PORT).strip()
print('  新端口 ' + NEW_SSH_PORT + ' 监听:', r or '等待中...')

# ============ Step 5: ufw 关闭 22 端口 ============
print('\n[5/6] ufw 关闭 22 端口...')
r = cmd('ufw delete allow 22/tcp 2>&1').strip()
print('  删除 22/tcp:', r[:100] if r else '成功')

# ============ Step 6: 验证最终状态 ============
print('\n[6/6] 最终验证...')
print()
print('--- ufw 规则 ---')
print(cmd('ufw status verbose | head -25'))
print()
print('--- SSH 端口 ---')
print(cmd("grep -E '^Port|^#Port' /etc/ssh/sshd_config").strip())
print()
print('--- fail2ban ---')
print(cmd('fail2ban-client status 2>&1 | head -20'))

client.close()
print()
print('=' * 55)
print('加固完成！')
print('下次连接命令:')
print('  ssh root@240b:4001:278:8402:0:bd18:bd09:af0d -p 22222')
print('=' * 55)
