# 简化版文档时间戳更新脚本

# 获取当前时间戳
$now = Get-Date
$chineseFormat = $now.ToString("yyyy年MM月dd日 HH:mm:ss")
$isoFormat = $now.ToString("yyyy-MM-dd")

# 文件路径
$readmePath = ".\README.md"
$changelogPath = ".\CHANGELOG.md"

Write-Output "开始更新文档时间戳..."

# 更新README.md
if (Test-Path $readmePath) {
    $content = Get-Content $readmePath -Raw -Encoding UTF8
    $updated = $content -replace '\*\*最后更新时间：.*?\*\*', "**最后更新时间：$chineseFormat**"
    Set-Content $readmePath -Value $updated -Encoding UTF8
    Write-Output "README.md 已更新: $chineseFormat"
} else {
    Write-Output "错误: README.md 文件不存在"
}

# 更新CHANGELOG.md
if (Test-Path $changelogPath) {
    $content = Get-Content $changelogPath -Raw -Encoding UTF8
    $updated = $content -replace '## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})', "## [\1] - $isoFormat"
    Set-Content $changelogPath -Value $updated -Encoding UTF8
    Write-Output "CHANGELOG.md 已更新: $isoFormat"
} else {
    Write-Output "错误: CHANGELOG.md 文件不存在"
}

Write-Output "时间戳更新完成！"