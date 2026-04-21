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
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

# ============ 1. 防火墙状态 ============
print('=' * 60)
print('[1] 防火墙状态')
print('=' * 60)
r = cmd('ufw status verbose 2>/dev/null')
print('ufw:', r.strip() if r.strip() else '未安装/未运行')
r = cmd('systemctl is-active firewalld 2>/dev/null')
print('firewalld:', r.strip() if r.strip() else '未运行')
r = cmd('iptables -L -n 2>/dev/null | grep -c "^Chain"')
print('iptables 链数:', r.strip())
r = cmd('nft list ruleset 2>/dev/null | head -5')
print('nftables:', r.strip()[:200] if r.strip() else '未安装')

# ============ 2. 开放端口 ============
print('\n' + '=' * 60)
print('[2] 监听端口（对外暴露）')
print('=' * 60)
print(cmd('ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null'))

# ============ 3. 入侵检测工具 ============
print('\n' + '=' * 60)
print('[3] 安全工具安装情况')
print('=' * 60)
tools = ['fail2ban', 'ossec', 'tripwire', 'aide', 'lynis', 'rkhunter', 'chkrootkit', 'samhain', 'auditd']
for tool in tools:
    r = cmd('which ' + tool + ' 2>/dev/null')
    status = '已安装' if r.strip() else '未安装'
    print('  ' + tool + ': ' + status)

# fail2ban 详细
r = cmd('which fail2ban 2>/dev/null')
if r.strip():
    print('\n  --- fail2ban 状态 ---')
    print(cmd('fail2ban-client status 2>/dev/null'))
    print(cmd('ls /etc/fail2ban/jail.d/ 2>/dev/null'))

# ============ 4. SSH 安全 ============
print('\n' + '=' * 60)
print('[4] SSH 安全配置')
print('=' * 60)
print('端口:', cmd("grep '^Port' /etc/ssh/sshd_config").strip())
print('Root登录:', cmd("grep 'PermitRootLogin' /etc/ssh/sshd_config").strip())
print('密码登录:', cmd("grep 'PasswordAuthentication' /etc/ssh/sshd_config").strip())
print('\n最近登录记录:')
print(cmd('last -15 2>/dev/null'))
print('\n失败登录尝试:')
r = cmd("journalctl -u ssh --since '1 day ago' 2>/dev/null | grep -i 'failed' | tail -10")
print(r.strip() if r.strip() else '无记录（可能无日志）')

# ============ 5. Cloudflare 代理 ============
print('\n' + '=' * 60)
print('[5] Cloudflare CDN 代理状态')
print('=' * 60)
r = cmd('curl -s https://www.skillxm.cn/ -I 2>/dev/null | grep -i "cf-ray\|server:"')
print('CF-Ray header:', '有（已代理）' if 'cf-ray' in r.lower() else '无（未开启代理 / DNS Only）')
print(r[:300])

# ============ 6. 系统状态 ============
print('\n' + '=' * 60)
print('[6] 系统资源 & 异常')
print('=' * 60)
print('负载:', cmd('uptime').strip())
print(cmd('free -h'))
print('\n活跃连接数:', cmd('ss -tnp 2>/dev/null | grep ESTAB | wc -l').strip())
print('连接来源TOP10:')
print(cmd("ss -tnp 2>/dev/null | grep ESTAB | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | head -10"))

# ============ 7. 总结 ============
print('\n' + '=' * 60)
print('[7] 安全评估总结')
print('=' * 60)
fw = cmd('ufw status verbose 2>/dev/null | grep "^Status"')
has_fw = 'active' in fw.lower()
ssh_port = cmd("grep '^Port' /etc/ssh/sshd_config").strip()
has_f2b = cmd('which fail2ban 2>/dev/null').strip()
cf = cmd('curl -s https://www.skillxm.cn/ -I 2>/dev/null | grep -qi cf-ray')
root_login = cmd("grep 'PermitRootLogin' /etc/ssh/sshd_config").strip()
pw_auth = cmd("grep 'PasswordAuthentication' /etc/ssh/sshd_config").strip()

print('  防火墙 ufw:', '已启用' if has_fw else '未启用 (!!危险!!)')
print('  fail2ban:', '已安装' if has_f2b else '未安装')
print('  SSH端口:', ssh_port if ssh_port else '默认22')
print('  Root登录:', root_login if root_login else '未限制')
print('  密码登录:', pw_auth if pw_auth else '未配置')
print('  Cloudflare:', '已代理(橙色云)' if cf else 'DNS Only(灰色云)(!!建议开启!!)')

client.close()
