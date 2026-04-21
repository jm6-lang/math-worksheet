$ErrorActionPreference = 'SilentlyContinue'
try {
    $r = Invoke-WebRequest -Uri 'https://github.com' -TimeoutSec 8 -UseBasicParsing
    Write-Host "GitHub.com: $($r.StatusCode)"
} catch {
    Write-Host "GitHub.com: FAIL - $($_.Exception.Message.Substring(0, [Math]::Min(100, $_.Exception.Message.Length)))"
}
