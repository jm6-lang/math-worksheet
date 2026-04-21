$ErrorActionPreference = "Stop"
$REPO = "jm6-lang/resource-portal"
$LocalFile = "C:\Users\Administrator\Desktop\新建文件夹\9951d3ac2a60b345235b026e181af1c.jpg"
$DestPath = "docs/public/data-card-qr.png"
$SHA = "613754cf"

# Get base64
$bytes = [System.IO.File]::ReadAllBytes($LocalFile)
$b64 = [Convert]::ToBase64String($bytes)
Write-Host "Image: $($bytes.Length) bytes"

# Write input JSON
$inputFile = [System.IO.Path]::GetTempPath() + "qr_input.json"
$b64 | Out-File -FilePath $inputFile -Encoding UTF8 -NoNewline
$size = (Get-Item $inputFile).Length
Write-Host "Base64 file: $size bytes"

# Try gh api --input
$proc = Start-Process -FilePath "gh" -ArgumentList "api","repos/$REPO/contents/$DestPath","--method","PUT","--input",$inputFile,"--jq",".content.html_url" -NoNewWindow -Wait -PassThru -RedirectStandardOutput "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\upload_out.txt" -RedirectStandardError "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\upload_err.txt"
Write-Host "Exit code: $($proc.ExitCode)"
if (Test-Path "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\upload_out.txt") {
    $out = Get-Content "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\upload_out.txt" -Raw
    Write-Host "STDOUT: $out"
}
if (Test-Path "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\upload_err.txt") {
    $err = Get-Content "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\upload_err.txt" -Raw
    Write-Host "STDERR: $err"
}

Remove-Item $inputFile -Force -EA SilentlyContinue
