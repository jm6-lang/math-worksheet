$ErrorActionPreference = "Stop"
$REPO = "jm6-lang/resource-portal"
$LocalFile = "C:\Users\Administrator\Desktop\新建文件夹\9951d3ac2a60b345235b026e181af1c.jpg"
$DestPath = "docs/public/data-card-qr.png"
$SHA = "613754cf"

# Get base64 of image
$bytes = [System.IO.File]::ReadAllBytes($LocalFile)
$b64 = [Convert]::ToBase64String($bytes)
Write-Host "Image: $($bytes.Length) bytes, base64: $($b64.Length) chars"

# Write base64 to temp file (content=@file.txt syntax)
$b64file = [System.IO.Path]::GetTempPath() + "qr_b64.txt"
[System.IO.File]::WriteAllText($b64file, $b64, [System.Text.Encoding]::UTF8)

# Write JSON body to temp file
$body = @{
    message = "chore: 替换大流量卡二维码图片"
    sha     = $SHA
} | ConvertTo-Json

$jsonFile = [System.IO.Path]::GetTempPath() + "qr_body.json"
[System.IO.File]::WriteAllText($jsonFile, $body, [System.Text.Encoding]::UTF8)

# Use gh api with --field content=@file
$proc = Start-Process -FilePath "gh" -ArgumentList "api","repos/$REPO/contents/$DestPath","--method","PUT","--field","message=chore: 替换大流量卡二维码图片","--field","content=@$b64file","--field","sha=$SHA" -NoNewWindow -Wait -PassThru
Write-Host "Exit code: $($proc.ExitCode)"

# Cleanup
Remove-Item $b64file -Force -EA SilentlyContinue
Remove-Item $jsonFile -Force -EA SilentlyContinue
