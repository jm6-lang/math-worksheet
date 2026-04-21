$ErrorActionPreference = 'SilentlyContinue'
try {
    $r = Invoke-WebRequest -Uri 'https://jm6-lang.github.io/resource-nav/' -TimeoutSec 15 -UseBasicParsing
    Write-Host "Status: $($r.StatusCode)"
    Write-Host "Length: $($r.Content.Length)"
} catch {
    Write-Host "Error: $($_.Exception.Message.Substring(0, [Math]::Min(200, $_.Exception.Message.Length)))"
}
