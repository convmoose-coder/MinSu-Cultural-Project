@echo off

echo 更新文档时间戳...

REM 获取当前日期和时间（中文格式）
for /f "tokens=1-6 delims=/: " %%a in ('time/t') do set "current_time=%%a:%%b:00"
for /f "tokens=1-3 delims=/ " %%a in ('date/t') do set "current_date=%%a年%%b月%%c日"
set "chinese_timestamp=%current_date% %current_time%"

echo 当前时间: %chinese_timestamp%

REM 使用PowerShell更新README.md中的时间戳
powershell -Command "$content = Get-Content 'README.md' -Raw; $updated = $content -replace '最后更新时间：[0-9]{4}年[0-9]{2}月[0-9]{2}日 [0-9]{2}:[0-9]{2}:[0-9]{2}', '最后更新时间：%chinese_timestamp%'; Set-Content 'README.md' $updated"

REM 获取当前日期（ISO格式）
for /f "tokens=1-3 delims=/ " %%a in ('date/t') do set "iso_date=%%a-%%b-%%c"

echo 当前ISO日期: %iso_date%

REM 使用PowerShell更新CHANGELOG.md中的最新版本日期
powershell -Command "$content = Get-Content 'CHANGELOG.md' -Raw; $updated = $content -replace '\[1\.0\.0\] - [0-9]{4}-[0-9]{2}-[0-9]{2}', '[1.0.0] - %iso_date%'; Set-Content 'CHANGELOG.md' $updated"

echo 时间戳更新完成！