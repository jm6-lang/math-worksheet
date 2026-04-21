# Get file content and SHA
$filePath = "C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\resource-portal\docs\.vitepress\theme\components\ZiWeiCalculator.vue"
$content = [System.IO.File]::ReadAllText($filePath)
$b64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content))

$sha = "d0d96c34dfad5bf95f046abde548e69b2ee657d1"

# Write to temp file for gh
$tempFile = "C:\tmp\gh_content.txt"
[System.IO.File]::WriteAllText($tempFile, $b64)

# Run gh command
$cmd = "gh api repos/jm6-lang/resource-portal/contents/docs/.vitepress/theme/components/ZiWeiCalculator.vue --method PUT -F message='fix: UMD模块需要调用才能获取导出对象' -F content@$tempFile -F sha=$sha"
Invoke-Expression $cmd
