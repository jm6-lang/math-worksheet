$ErrorActionPreference = "Stop"
$REPO = "jm6-lang/resource-portal"
$SHA = "613754cf"
$LocalFile = "C:\Users\Administrator\Desktop\新建文件夹\9951d3ac2a60b345235b026e181af1c.jpg"
$API_PATH = "repos/$REPO/contents/docs/public/data-card-qr.png"

# Read image as base64
$bytes = [System.IO.File]::ReadAllBytes($LocalFile)
$b64 = [Convert]::ToBase64String($bytes)
Write-Host "Image size: $($bytes.Length) bytes, base64 length: $($b64.Length)"

# Build JSON body
$body = @{
    message = "chore: 替换大流量卡二维码图片"
    content = $b64
    sha     = $SHA
} | ConvertTo-Json -Compress

# Write body to temp file
$tmp = [System.IO.Path]::GetTempFileName() + ".json"
[System.IO.File]::WriteAllText($tmp, $body, [System.Text.UTF8Encoding]::new($true))
Write-Host "Body written to: $tmp"

# Call GitHub API via curl
$headers = @{
    Accept        = "application/vnd.github+json"
    Authorization = "Bearer $env:GH_TOKEN"
    "X-GitHub-Api-Version" = "2022-11-28"
}

try {
    $resp = Invoke-RestMethod -Uri "https://api.github.com/$API_PATH" `
        -Method PUT `
        -Headers $headers `
        -ContentType "application/json" `
        -InFile $tmp `
        -TimeoutSec 30
    Write-Host "OK - content_url: $($resp.content.html_url)"
} catch {
    Write-Host "FAIL: $($_.Exception.Message)"
    Write-Host "Response: $($_.Exception.Response)"
} finally {
    Remove-Item $tmp -Force -EA SilentlyContinue
}
