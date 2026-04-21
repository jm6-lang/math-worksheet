$ErrorActionPreference = 'SilentlyContinue'
$token = gh auth token
$headers = @{
    "Authorization" = "Bearer $token"
    "Accept" = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
    "Content-Type" = "application/json"
}

$repo = "jm6-lang/resource-nav"
$files = @(
    ".github/workflows/deploy.yml",
    "docs/recommend.md"
)

foreach ($file in $files) {
    $localPath = "C:\resource-nav\$file"
    if (!(Test-Path $localPath)) {
        Write-Host "SKIP: $file not found"
        continue
    }
    
    $content = [Convert]::ToBase64String([IO.File]::ReadAllBytes($localPath))
    
    # Get current SHA
    $getUrl = "https://api.github.com/repos/$repo/contents/$file`?ref=main"
    $sha = $null
    try {
        $existing = Invoke-RestMethod -Uri $getUrl -Headers $headers -Method GET
        $sha = $existing.sha
    } catch {}
    
    $body = @{
        message = "Add $file"
        content = $content
        branch = "main"
    }
    if ($sha) { $body.sha = $sha }
    
    $bodyJson = $body | ConvertTo-Json -Compress
    $bodyBytes = [System.Text.Encoding]::UTF8.GetBytes($bodyJson)
    
    $req = [System.Net.WebRequest]::Create("https://api.github.com/repos/$repo/contents/$file")
    $req.Method = "PUT"
    $req.Headers["Authorization"] = "Bearer $token"
    $req.Headers["Accept"] = "application/vnd.github+json"
    $req.Headers["X-GitHub-Api-Version"] = "2022-11-28"
    $req.ContentType = "application/json; charset=utf-8"
    $req.ContentLength = $bodyBytes.Length
    $req.Timeout = 15000
    
    $reqStream = $req.GetRequestStream()
    $reqStream.Write($bodyBytes, 0, $bodyBytes.Length)
    $reqStream.Close()
    
    try {
        $resp = $req.GetResponse()
        $status = [int]$resp.StatusCode
        Write-Host "OK $status : $file"
        $resp.Close()
    } catch {
        $ex = $_.Exception.Response
        if ($ex) {
            $status = [int]$ex.StatusCode
            Write-Host "FAIL $status : $file"
        } else {
            Write-Host "FAIL timeout : $file"
        }
    }
}

Write-Host ""
Write-Host "Done! Check https://github.com/jm6-lang/resource-nav/actions"
