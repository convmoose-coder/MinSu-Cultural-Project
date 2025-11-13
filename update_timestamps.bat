@echo off
setlocal enabledelayedexpansion

REM 获取当前日期和时间，设置为环境变量
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "year=!dt:~0,4!"
set "month=!dt:~4,2!"
set "day=!dt:~6,2!"
set "hour=!dt:~8,2!"
set "minute=!dt:~10,2!"
set "second=!dt:~12,2!"

REM 格式化时间戳
set "chineseFormat=!year!年!month!月!day!日 !hour!:!minute!:!second!"
set "isoFormat=!year!-!month!-!day!"

echo 开始更新文档时间戳...
echo 当前时间: !chineseFormat!

REM 使用PowerShell命令更新README.md中的时间戳
powershell -Command "$content = Get-Content 'README.md' -Raw; $updated = $content -replace '\*\*最后更新时间：.*?\*\*', '**最后更新时间：!chineseFormat!**'; Set-Content 'README.md' -Value $updated -Encoding UTF8"
echo README.md 已更新为最新时间戳

REM 使用PowerShell命令更新CHANGELOG.md中的时间戳
powershell -Command "$content = Get-Content 'CHANGELOG.md' -Raw; $updated = $content -replace '## \[(\\d+\\.\\d+\\.\\d+)\] - (\\d{4}-\\d{2}-\\d{2})', '## [\\1] - !isoFormat!'; Set-Content 'CHANGELOG.md' -Value $updated -Encoding UTF8"
echo CHANGELOG.md 已更新为最新日期: !isoFormat!

echo 时间戳更新完成！
pause