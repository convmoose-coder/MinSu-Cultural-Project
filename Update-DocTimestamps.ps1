#!/usr/bin/env pwsh
# 文档时间戳自动更新脚本 - PowerShell 版本

<#
.SYNOPSIS
更新README.md和CHANGELOG.md文件中的时间戳，使其反映当前本地时间。

.DESCRIPTION
此脚本自动更新文档文件中的时间戳，并提供验证功能确保显示的时间与当前时间一致。

.PARAMETER VerifyOnly
仅验证时间戳，不进行更新

.PARAMETER ReadmePath
README.md文件路径，默认为当前目录下的README.md

.PARAMETER ChangelogPath
CHANGELOG.md文件路径，默认为当前目录下的CHANGELOG.md

.EXAMPLE
# 更新时间戳并验证
./Update-DocTimestamps.ps1

# 仅验证时间戳
./Update-DocTimestamps.ps1 -VerifyOnly

# 指定自定义路径
./Update-DocTimestamps.ps1 -ReadmePath "./docs/README.md" -ChangelogPath "./docs/CHANGELOG.md"
#>

param(
    [switch]$VerifyOnly = $false,
    [string]$ReadmePath = ".\README.md",
    [string]$ChangelogPath = ".\CHANGELOG.md"
)

function Get-CurrentTimestamp {
    <#
    .SYNOPSIS
    获取当前本地时间戳，返回自定义对象包含两种格式
    #>
    $now = Get-Date
    return [PSCustomObject]@{ 
        ChineseFormat = $now.ToString("yyyy年MM月dd日 HH:mm:ss")
        ISOFormat = $now.ToString("yyyy-MM-dd")
        DateOnly = $now.Date
    }
}

function Update-ReadmeTimestamp {
    <#
    .SYNOPSIS
    更新README.md文件中的时间戳
    #>
    param(
        [string]$Path
    )
    
    if (-not (Test-Path -Path $Path -PathType Leaf)) {
        Write-Host "错误: README.md文件不存在于路径 $Path" -ForegroundColor Red
        return $false
    }
    
    $timestamp = Get-CurrentTimestamp
    
    # 读取文件内容
    $content = Get-Content -Path $Path -Raw -Encoding UTF8
    
    # 更新时间戳
    $updatedContent = $content
    if ($content -match '\*\*最后更新时间：.*?\*\*') {
        $updatedContent = $content -replace '\*\*最后更新时间：.*?\*\*', "**最后更新时间：$($timestamp.ChineseFormat)**"
    } else {
        # 如果没有找到时间戳行，在文件开头添加
        $lines = $content -split "`n"
        if ($lines.Count -gt 0) {
            # 假设第一行是标题
            $updatedContent = $lines[0] + "`n`n<!-- TIMESTAMP_MARKER:README -->`n<!-- 此时间会在下次更新时自动更新为本地时间 -->`n**最后更新时间：$($timestamp.ChineseFormat)**`n<!-- TIMESTAMP_END -->`n" + ($lines | Select-Object -Skip 1) -join "`n"
        } else {
            $updatedContent = $content + "`n`n<!-- TIMESTAMP_MARKER:README -->`n<!-- 此时间会在下次更新时自动更新为本地时间 -->`n**最后更新时间：$($timestamp.ChineseFormat)**`n<!-- TIMESTAMP_END -->"
        }
    }
    
    # 写回文件
    Set-Content -Path $Path -Value $updatedContent -Encoding UTF8
    
    Write-Host "已更新README.md时间戳为: $($timestamp.ChineseFormat)" -ForegroundColor Green
    return $true
}

function Update-ChangelogTimestamp {
    <#
    .SYNOPSIS
    更新CHANGELOG.md文件中的最新版本时间戳
    #>
    param(
        [string]$Path
    )
    
    if (-not (Test-Path -Path $Path -PathType Leaf)) {
        Write-Host "错误: CHANGELOG.md文件不存在于路径 $Path" -ForegroundColor Red
        return $false
    }
    
    $timestamp = Get-CurrentTimestamp
    
    # 读取文件内容
    $content = Get-Content -Path $Path -Raw -Encoding UTF8
    
    # 更新最新版本的日期
    $updatedContent = $content
    if ($content -match '## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})') {
        $updatedContent = $content -replace '## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})', "## [\1] - $($timestamp.ISOFormat)"
        Write-Host "已更新CHANGELOG.md最新版本日期为: $($timestamp.ISOFormat)" -ForegroundColor Green
    } else {
        Write-Host "警告: 在CHANGELOG.md中未找到符合格式的版本条目" -ForegroundColor Yellow
        # 如果未找到版本条目，则添加一个初始版本
        if ($content -match '\[未发布\]') {
            # 在[未发布]部分后添加新版本
            $parts = $content -split '## \[未发布\]'
            if ($parts.Count -gt 1) {
                $newVersionSection = "## [未发布]`n`n### 新增`n`n### 变更`n`n### 修复`n`n### 移除`n`n## [1.0.0] - $($timestamp.ISOFormat)`n`n### 新增`n- 初始版本`n"
                if ($parts[1] -match '## ') {
                    $updatedContent = $parts[0] + $newVersionSection + ($parts[1] -split '## ', 2)[1]
                } else {
                    $updatedContent = $parts[0] + $newVersionSection
                }
            } else {
                $updatedContent = $content + "`n## [1.0.0] - $($timestamp.ISOFormat)`n`n### 新增`n- 初始版本`n"
            }
            Write-Host "已在CHANGELOG.md中添加初始版本，日期为: $($timestamp.ISOFormat)" -ForegroundColor Green
        } else {
            Write-Host "错误: CHANGELOG.md格式不符合预期，无法更新时间戳" -ForegroundColor Red
            return $false
        }
    }
    
    # 写回文件
    Set-Content -Path $Path -Value $updatedContent -Encoding UTF8
    
    return $true
}

function Test-Timestamps {
    <#
    .SYNOPSIS
    验证README.md和CHANGELOG.md中的时间戳是否与当前本地时间一致
    #>
    param(
        [string]$ReadmePath,
        [string]$ChangelogPath
    )
    
    if (-not (Test-Path -Path $ReadmePath -PathType Leaf) -or -not (Test-Path -Path $ChangelogPath -PathType Leaf)) {
        Write-Host "错误: 验证失败，文件不存在" -ForegroundColor Red
        return $false
    }
    
    $timestamp = Get-CurrentTimestamp
    $allVerified = $true
    
    # 验证README.md
    $readmeContent = Get-Content -Path $ReadmePath -Raw -Encoding UTF8
    
    if ($readmeContent -match '\*\*最后更新时间：(.*?)\*\*') {
        $readmeTimestamp = $matches[1]
        # 解析README中的日期
        try {
            $readmeDateStr = $readmeTimestamp.Split(' ')[0]  # 获取日期部分
            $readmeDate = [DateTime]::ParseExact($readmeDateStr, "yyyy年MM月dd日", $null).Date
            
            if ($readmeDate -eq $timestamp.DateOnly) {
                Write-Host "✓ README.md日期验证成功：$readmeDateStr" -ForegroundColor Green
            } else {
                Write-Host "✗ README.md日期验证失败：显示$readmeDateStr，当前应为$($timestamp.DateOnly.ToString("yyyy年MM月dd日"))" -ForegroundColor Red
                $allVerified = $false
            }
        } catch {
            Write-Host "✗ README.md日期格式验证失败：$readmeTimestamp" -ForegroundColor Red
            $allVerified = $false
        }
    } else {
        Write-Host "✗ README.md中未找到时间戳" -ForegroundColor Red
        $allVerified = $false
    }
    
    # 验证CHANGELOG.md
    $changelogContent = Get-Content -Path $ChangelogPath -Raw -Encoding UTF8
    
    if ($changelogContent -match '## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})') {
        $changelogVersion = $matches[1]
        $changelogDate = $matches[2]
        
        # 解析CHANGELOG中的日期
        try {
            $changelogDateObj = [DateTime]::ParseExact($changelogDate, "yyyy-MM-dd", $null).Date
            
            if ($changelogDateObj -eq $timestamp.DateOnly) {
                Write-Host "✓ CHANGELOG.md版本 $changelogVersion 日期验证成功：$changelogDate" -ForegroundColor Green
            } else {
                Write-Host "✗ CHANGELOG.md日期验证失败：显示$changelogDate，当前应为$($timestamp.DateOnly.ToString("yyyy-MM-dd"))" -ForegroundColor Red
                $allVerified = $false
            }
        } catch {
            Write-Host "✗ CHANGELOG.md日期格式验证失败：$changelogDate" -ForegroundColor Red
            $allVerified = $false
        }
    } else {
        Write-Host "✗ CHANGELOG.md中未找到符合格式的版本时间戳" -ForegroundColor Red
        $allVerified = $false
    }
    
    if ($allVerified) {
        Write-Host "所有时间戳验证通过！" -ForegroundColor Green
    }
    
    return $allVerified
}

# 主函数
Write-Host "文档时间戳更新工具（PowerShell版本）" -ForegroundColor Cyan
Write-Host "- README.md: $ReadmePath" -ForegroundColor Cyan
Write-Host "- CHANGELOG.md: $ChangelogPath" -ForegroundColor Cyan
Write-Host

if ($VerifyOnly) {
    Write-Host "开始验证时间戳..." -ForegroundColor Cyan
    Test-Timestamps -ReadmePath $ReadmePath -ChangelogPath $ChangelogPath
} else {
    Write-Host "开始更新时间戳..." -ForegroundColor Cyan
    # 更新README.md
    $readmeSuccess = Update-ReadmeTimestamp -Path $ReadmePath
    
    # 更新CHANGELOG.md
    $changelogSuccess = Update-ChangelogTimestamp -Path $ChangelogPath
    
    if ($readmeSuccess -and $changelogSuccess) {
        Write-Host
        Write-Host "更新完成！开始验证..." -ForegroundColor Cyan
        Test-Timestamps -ReadmePath $ReadmePath -ChangelogPath $ChangelogPath
    } else {
        Write-Host "更新失败，请检查错误信息" -ForegroundColor Red
    }
}

Write-Host "`n脚本执行完毕。" -ForegroundColor Cyan