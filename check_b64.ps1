# Check what the b64 files look like
$wfPath = "C:\Temp\wf_b64.txt"
$content = Get-Content $wfPath -Raw
Write-Host "Length: $($content.Length)"
Write-Host "First 50 chars:"
Write-Host $content.Substring(0, [Math]::Min(50, $content.Length))
Write-Host "---"
Write-Host "Last 50 chars:"
Write-Host $content.Substring([Math]::Max(0, $content.Length - 50))
