$ErrorActionPreference = "Stop"
$LocalFile = "C:\Users\Administrator\Desktop\新建文件夹\9951d3ac2a60b345235b026e181af1c.jpg"
$DestPath = "docs/public/data-card-qr.png"
$Repo = "jm6-lang/resource-portal"

# Get SHA
$sha = (gh api "repos/$Repo/contents/$DestPath" --jq ".sha").Trim()
Write-Host "SHA: $sha"

# Write base64 to temp file
$b64File = [System.IO.Path]::GetTempPath() + "qr_b64.txt"
$b64 = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($LocalFile))
[System.IO.File]::WriteAllText($b64File, $b64, [System.Text.Encoding]::UTF8)
Write-Host "Base64 file: $b64File ($((Get-Item $b64File).Length) bytes)"

# gh api -F content=@file reads content from file
$result = gh api "repos/$Repo/contents/$DestPath" `
    --method PUT `
    -f message="chore: 替换大流量卡二维码图片" `
    -f sha="$sha" `
    -f content="@$b64File" `
    --jq ".content.html_url" 2>&1

Write-Host "Exit: $LASTEXITCODE"
Write-Host "Result: $result"

if ($LASTEXITCODE -eq 0) { Write-Host "SUCCESS!" }

Remove-Item $b64File -Force -EA SilentlyContinue
