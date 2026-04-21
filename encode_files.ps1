$ErrorActionPreference = 'Stop'

# Step 1: base64 encode
$wfContent = [Convert]::ToBase64String([IO.File]::ReadAllBytes("C:\resource-nav\.github\workflows\deploy.yml"))
$recContent = [Convert]::ToBase64String([IO.File]::ReadAllBytes("C:\resource-nav\docs\recommend.md"))

# Write to temp files
$wfContent | Out-File "C:\Temp\wf_b64.txt" -Encoding ASCII -NoNewline
$recContent | Out-File "C:\Temp\rec_b64.txt" -Encoding ASCII -NoNewline

Write-Host "Base64 encoded, lengths: wf=$($wfContent.Length) rec=$($recContent.Length)"
