# SSH 连接脚本
$server = "240b:4001:278:8402:0:bd18:bd09:af0d"
$port = 22
$user = "root"
$pass = "Langlanbg0.0"

# 创建 PSCredential
$secPass = ConvertTo-SecureString $pass -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential($user, $secPass)

# 读取服务器信息
$cmd = @"
uname -a
echo '=== CPU/内存 ==='
free -h
echo '=== 负载/进程数 ==='
uptime
echo '=== 网络接口 ==='
ip addr show
echo '=== 网络统计 ==='
ss -s
echo '=== 当前TCP参数 ==='
sysctl -a 2>/dev/null | grep -E '^(net\.ipv4\.tcp|net\.core|net\.ipv4\.conf\.all\.rp_filter)' | sort -u
echo '=== DNS ==='
cat /etc/resolv.conf
echo '=== 当前DNS ==='
nslookup google.com 2>/dev/null || echo 'nslookup not available'
echo '=== 延迟测试 ==='
curl -s -w 'dns: %{time_namelookup}s connect: %{time_connect}s total: %{time_total}s\n' -o /dev/null https://www.google.com --max-time 10
curl -s -w 'dns: %{time_namelookup}s connect: %{time_connect}s total: %{time_total}s\n' -o /dev/null https://www.baidu.com --max-time 10
"@

# 建立 SSH 会话
try {
    $session = New-SSHSession -ComputerName $server -Port $port -Credential $cred -ConnectionTimeout 30 -AcceptKey
    if ($session.Connected) {
        Write-Host '[OK] SSH连接成功'
        $result = Invoke-SSHCommand -SessionId $session.SessionId -Command $cmd -Timeout 60
        $result.Output
        Remove-SSHSession -SessionId $session.SessionId | Out-Null
    }
} catch {
    Write-Host "[错误] $_"
    # 备用方案：使用 ssh.exe 直接命令
    Write-Host '尝试使用 ssh.exe 直接连接...'
    echo $pass | ssh -o StrictHostKeyChecking=no -o PasswordAuthentication=yes -o ConnectTimeout=20 $user@$server $cmd
}
