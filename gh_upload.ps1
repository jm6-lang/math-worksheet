$ErrorActionPreference = "Stop"
$LocalFile = "C:\Users\Administrator\Desktop\新建文件夹\9951d3ac2a60b345235b026e181af1c.jpg"
$DestPath = "docs/public/data-card-qr.png"
$Repo = "jm6-lang/resource-portal"

# Get SHA
$proc = Start-Process -FilePath "gh" -ArgumentList "api","repos/$Repo/contents/$DestPath","--jq",".sha" -NoNewWindow -Wait -PassThru -RedirectStandardOutput "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_sha.txt" -RedirectStandardError "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_sha_err.txt"
$sha = (Get-Content "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_sha.txt" -Raw).Trim()
Write-Host "SHA: $sha"

# Build input JSON: message + sha + content (base64 on one line)
$body = @{
    message = "chore: 替换大流量卡二维码图片"
    sha     = $sha
} | ConvertTo-Json -Compress
$b64 = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($LocalFile))
$inputContent = "$body`n$b64"
$inputFile = [System.IO.Path]::GetTempPath() + "qr_input.txt"
[System.IO.File]::WriteAllText($inputFile, $inputContent, [System.Text.Encoding]::UTF8)
Write-Host "Input file: $inputFile ($((Get-Item $inputFile).Length) bytes)"

# Read README to understand input format
# gh api --input format: key=value on each line, content is base64
$proc2 = Start-Process -FilePath "gh" -ArgumentList "api","repos/$Repo/contents/$DestPath","--method","PUT","--input",$inputFile -NoNewWindow -Wait -PassThru -RedirectStandardOutput "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_out.txt" -RedirectStandardError "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_err.txt"
Write-Host "Exit: $($proc2.ExitCode)"
if ((Test-Path "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_out.txt") -and ((Get-Item "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_out.txt").Length -gt 0) -and ((Get-Content "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_out.txt" -Raw).Trim())) {
    Write-Host "OUT: $(Get-Content 'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_out.txt' -Raw)"
}
if (Test-Path "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_err.txt") {
    Write-Host "ERR: $(Get-Content 'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\qr_err.txt' -Raw)"
}

Remove-Item $inputFile -Force -EA SilentlyContinue
