$ErrorActionPreference = "Stop"
$LocalFile = "C:\Users\Administrator\Desktop\新建文件夹\9951d3ac2a60b345235b026e181af1c.jpg"
$DestPath = "docs/public/data-card-qr.png"
$Repo = "jm6-lang/resource-portal"

# Get SHA
$sha = (gh api "repos/$Repo/contents/$DestPath" --jq ".sha" 2>$null).Trim()
Write-Host "SHA: $sha"

# Build JSON file
$bytes = [System.IO.File]::ReadAllBytes($LocalFile)
$b64 = [Convert]::ToBase64String($bytes)

$json = @{
    message = "chore: 替换大流量卡二维码图片"
    sha     = $sha
    content = $b64
} | ConvertTo-Json

$jsonFile = [System.IO.Path]::GetTempPath() + "qr_body.json"
# Write without BOM
$utf8 = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllText($jsonFile, $json, $utf8)
Write-Host "JSON file: $(Get-Item $jsonFile).Length bytes"

# Try gh api --input
$result = gh api "repos/$Repo/contents/$DestPath" --method PUT --input $jsonFile 2>&1
Write-Host "Result exit: $LASTEXITCODE"
Write-Host $result

Remove-Item $jsonFile -Force -EA SilentlyContinue
