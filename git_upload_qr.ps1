$ErrorActionPreference = "Stop"
$LocalFile = "C:\Users\Administrator\Desktop\新建文件夹\9951d3ac2a60b345235b026e181af1c.jpg"
$DestFile = "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs\public\data-card-qr.png"
$RepoDir = "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal"

# Check file exists
if (-not (Test-Path $LocalFile)) {
    Write-Host "FAIL: Source file not found: $LocalFile"
    exit 1
}

# Copy to destination
Copy-Item $LocalFile -Destination $DestFile -Force
$size = (Get-Item $DestFile).Length
Write-Host "Copied: $size bytes to $DestFile"

# Git add + commit + push
Set-Location $RepoDir
git add "docs/public/data-card-qr.png"
git status --short "docs/public/data-card-qr.png"

$proc = Start-Process -FilePath "git" -ArgumentList "commit","-m","chore: 替换大流量卡二维码图片" -NoNewWindow -Wait -PassThru
Write-Host "commit exit: $($proc.ExitCode)"

if ($proc.ExitCode -ne 0) {
    $err = git commit -m "chore: 替换大流量卡二维码图片" 2>&1
    Write-Host "commit err: $err"
}

$proc2 = Start-Process -FilePath "git" -ArgumentList "push" -NoNewWindow -Wait -PassThru
Write-Host "push exit: $($proc2.ExitCode)"
