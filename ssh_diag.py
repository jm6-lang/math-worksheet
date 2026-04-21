import paramiko
import time

server = "240b:4001:278:8402:0:bd18:bd09:af0d"
port = 22
user = "root"
password = "Langlanbg0.0"

def ssh_cmd(cmd):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=30)
    out = stdout.read().decode('utf-8', errors='replace')
    err = stderr.read().decode('utf-8', errors='replace')
    return out + err

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"正在连接 {server} ...")
    client.connect(server, port=port, username=user, password=password, 
                   timeout=20, allow_agent=False, look_for_keys=False,
                   banner_timeout=20, auth_timeout=20)
    print("[OK] 连接成功！")

    print("\n=== 1. 系统信息 ===")
    print(ssh_cmd("uname -a && uptime && free -h && df -h /"))

    print("\n=== 2. 网络接口状态 ===")
    print(ssh_cmd("ip addr show | grep -E 'inet|state|mtu'"))

    print("\n=== 3. 网络统计 ===")
    print(ssh_cmd("ss -tuln | head -20 && echo '---' && ip -s link show | grep -E 'RX|TX|errors|collisions'"))

    print("\n=== 4. 当前 TCP 参数 ===")
    print(ssh_cmd("sysctl -a 2>/dev/null | grep -E '^(net\.ipv4\.tcp|net\.core|net\.ipv4\.conf\.all\.rp_filter|net\.ipv4\.ip_local_port_range)' | sort -u"))

    print("\n=== 5. DNS 配置 ===")
    print(ssh_cmd("cat /etc/resolv.conf"))

    print("\n=== 6. 延迟测试 ===")
    print(ssh_cmd("curl -s -w 'Google => dns:%{time_namelookup}s connect:%{time_connect}s ttfb:%{time_starttransfer}s total:%{time_total}s\\n' -o /dev/null https://www.google.com --max-time 15 || echo 'google超时'"))
    print(ssh_cmd("curl -s -w 'Baidu  => dns:%{time_namelookup}s connect:%{time_connect}s ttfb:%{time_starttransfer}s total:%{time_total}s\\n' -o /dev/null https://www.baidu.com --max-time 10 || echo 'baidu超时'"))
    print(ssh_cmd("curl -s -w 'Github => dns:%{time_namelookup}s connect:%{time_connect}s ttfb:%{time_starttransfer}s total:%{time_total}s\\n' -o /dev/null https://github.com --max-time 15 || echo 'github超时'"))

    print("\n=== 7. 系统限制 ===")
    print(ssh_cmd("ulimit -a 2>/dev/null && cat /proc/sys/fs/file-nr"))
    print(ssh_cmd("cat /proc/sys/net/core/somaxconn && cat /proc/sys/net/ipv4/tcp_max_syn_backlog"))

    print("\n=== 8. 已安装的网络工具 ===")
    print(ssh_cmd("which speedtest-cli netcat nc iperf3 tcptrace 2>/dev/null; systemctl status nginx 2>/dev/null | head -5 || echo 'nginx未运行/未安装'"))
    print(ssh_cmd("systemctl status docker 2>/dev/null | head -5 || echo 'docker未运行/未安装'"))

    client.close()

except Exception as e:
    print(f"[错误] {e}")
