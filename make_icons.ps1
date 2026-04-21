Add-Type -AssemblyName System.Drawing
$iconDir = "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\jm-toolbox\assets\icons"
$icons = @("home","home-active","history","history-active","about","about-active","share")

foreach ($name in $icons) {
    $bmp = New-Object System.Drawing.Bitmap(81, 81)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.Clear([System.Drawing.Color]::FromArgb(200, 200, 200))
    $g.Dispose()
    $bmp.Save("$iconDir\$name.png", [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
}
Write-Output "icons created"
