$ErrorActionPreference = "Stop"
$LocalFile = "C:\Users\Administrator\Desktop\新建文件夹\9951d3ac2a60b345235b026e181af1c.jpg"
$DestPath = "docs/public/data-card-qr.png"
$Repo = "jm6-lang/resource-portal"

# Get SHA
$proc = Start-Process -FilePath "gh" -ArgumentList "api","repos/$Repo/contents/$DestPath","--jq",".sha" -NoNewWindow -Wait -PassThru -RedirectStandardOutput "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_sha.txt"
$sha = (Get-Content "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_sha.txt" -Raw).Trim()
Write-Host "SHA: $sha"

# Read image bytes
$bytes = [System.IO.File]::ReadAllBytes($LocalFile)
$b64 = [Convert]::ToBase64String($bytes)
Write-Host "Image bytes: $($bytes.Length), base64: $($b64.Length)"

# Build input file: key=value on each line (NOT JSON)
$inputFile = [System.IO.Path]::GetTempPath() + "qr_input.txt"
$lines = @(
    "message=chore: 替换大流量卡二维码图片",
    "sha=$sha",
    "content=$b64"
)
[System.IO.File]::WriteAllLines($inputFile, $lines, [System.Text.Encoding]::UTF8)
Write-Host "Input file: $inputFile ($(Get-Item $inputFile).Length bytes)"

# Upload via gh api --input
$proc2 = Start-Process -FilePath "gh" -ArgumentList "api","repos/$Repo/contents/$DestPath","--method","PUT","--input",$inputFile -NoNewWindow -Wait -PassThru `
    -RedirectStandardOutput "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_out.txt" `
    -RedirectStandardError "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_err.txt"

$stdout = (Get-Content "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_out.txt" -Raw).Trim()
$stderr = (Get-Content "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_err.txt" -Raw).Trim()

Write-Host "Exit: $($proc2.ExitCode)"
if ($stdout) { Write-Host "OUT: $stdout" }
if ($stderr) { Write-Host "ERR: $stderr" }

Remove-Item $inputFile -Force -EA SilentlyContinue
