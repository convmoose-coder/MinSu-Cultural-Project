@echo off

REM 验证文档时间戳脚本

echo 开始验证文档时间戳...

REM 检查README.md中的时间戳格式
powershell -Command "$content = Get-Content 'README.md' -Raw; if ($content -match '\*\*最后更新时间：([0-9]{4}年[0-9]{2}月[0-9]{2}日 [0-9]{2}:[0-9]{2}:[0-9]{2})\*\*') { Write-Host '✓ README.md时间戳格式正确: ' $matches[1]; exit 0 } else { Write-Host '✗ README.md时间戳格式错误'; exit 1 }"
set "readme_status=%errorlevel%"

REM 检查CHANGELOG.md中的时间戳格式
powershell -Command "$content = Get-Content 'CHANGELOG.md' -Raw; if ($content -match '## \[(\d+\.\d+\.\d+)\] - ([0-9]{4}-[0-9]{2}-[0-9]{2})') { Write-Host '✓ CHANGELOG.md版本 ' $matches[1] ' 日期格式正确: ' $matches[2]; exit 0 } else { Write-Host '✗ CHANGELOG.md日期格式错误'; exit 1 }"
set "changelog_status=%errorlevel%"

REM 验证时间戳更新机制说明
echo.
echo 自动更新机制说明：
echo 1. README.md包含格式为 "最后更新时间：YYYY年MM月DD日 HH:mm:ss" 的时间戳
echo 2. CHANGELOG.md中的版本条目使用 "## [x.y.z] - YYYY-MM-DD" 格式
echo 3. 文档更新时，可运行update_timestamps.bat脚本自动更新为当前本地时间
echo 4. 时间戳已添加特殊标记(TIMESTAMP_MARKER)方便自动识别
echo 5. 验证脚本(verify_timestamps.bat)可检查时间戳格式是否正确

echo.
if %readme_status% EQU 0 if %changelog_status% EQU 0 (
    echo 验证完成：所有时间戳格式正确！
) else (
    echo 验证完成：部分时间戳格式验证失败！
)

echo.
echo 时间戳验证脚本执行完毕。