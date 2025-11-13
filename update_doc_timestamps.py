#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文档时间戳自动更新脚本

此脚本用于自动更新README.md和CHANGELOG.md文件中的时间戳，使其反映当前本地时间。
同时提供验证功能，确保显示的时间与实际修改时间一致。
"""

import os
import re
import datetime
import argparse
from pathlib import Path

def get_current_timestamp():
    """
    获取当前本地时间戳，返回两种格式：
    1. 中文格式: 2024年11月15日 16:30:00
    2. ISO格式: 2024-11-15
    """
    now = datetime.datetime.now()
    chinese_format = now.strftime("%Y年%m月%d日 %H:%M:%S")
    iso_format = now.strftime("%Y-%m-%d")
    return chinese_format, iso_format

def update_readme_timestamp(readme_path):
    """
    更新README.md文件中的时间戳
    """
    if not os.path.exists(readme_path):
        print(f"错误: README.md文件不存在于路径 {readme_path}")
        return False
    
    chinese_format, _ = get_current_timestamp()
    
    # 读取文件内容
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新时间戳 - 使用正则表达式匹配现有的时间戳行
    timestamp_pattern = r'\*\*最后更新时间：.*?\*\*'
    new_timestamp_line = f'**最后更新时间：{chinese_format}**'
    
    if re.search(timestamp_pattern, content):
        updated_content = re.sub(timestamp_pattern, new_timestamp_line, content)
    else:
        # 如果没有找到时间戳行，在文件开头添加（在标题之后）
        lines = content.split('\n')
        if len(lines) > 0:
            # 假设第一行是标题
            updated_content = lines[0] + '\n\n<!-- 此时间会在下次更新时自动更新为本地时间 -->\n' + new_timestamp_line + '\n' + '\n'.join(lines[1:])
        else:
            updated_content = content + '\n\n<!-- 此时间会在下次更新时自动更新为本地时间 -->\n' + new_timestamp_line
    
    # 写回文件
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"已更新README.md时间戳为: {chinese_format}")
    return True

def update_changelog_timestamp(changelog_path):
    """
    更新CHANGELOG.md文件中的最新版本时间戳
    """
    if not os.path.exists(changelog_path):
        print(f"错误: CHANGELOG.md文件不存在于路径 {changelog_path}")
        return False
    
    _, iso_format = get_current_timestamp()
    
    # 读取文件内容
    with open(changelog_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新最新版本的日期 - 查找[未发布]下方的第一个版本条目
    # 或者更新第一个版本条目的日期
    version_pattern = r'## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})'
    
    if re.search(version_pattern, content):
        updated_content = re.sub(version_pattern, f'## [\\1] - {iso_format}', content, 1)  # 只替换第一个匹配项
        print(f"已更新CHANGELOG.md最新版本日期为: {iso_format}")
    else:
        print("警告: 在CHANGELOG.md中未找到符合格式的版本条目")
        # 如果未找到版本条目，则添加一个初始版本
        if "[未发布]" in content:
            # 在[未发布]部分后添加新版本
            parts = content.split("## [未发布]")
            if len(parts) > 1:
                new_version_section = f"## [未发布]\n\n### 新增\n\n### 变更\n\n### 修复\n\n### 移除\n\n## [1.0.0] - {iso_format}\n\n### 新增\n- 初始版本\n"
                updated_content = parts[0] + new_version_section + parts[1].split("## ", 1)[1] if len(parts) > 1 and "## " in parts[1] else parts[0] + new_version_section
            else:
                updated_content = content + f"\n## [1.0.0] - {iso_format}\n\n### 新增\n- 初始版本\n"
            print(f"已在CHANGELOG.md中添加初始版本，日期为: {iso_format}")
        else:
            updated_content = content
            print("错误: CHANGELOG.md格式不符合预期，无法更新时间戳")
    
    # 写回文件
    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    return True

def verify_timestamps(readme_path, changelog_path):
    """
    验证README.md和CHANGELOG.md中的时间戳是否与当前本地时间一致
    """
    if not os.path.exists(readme_path) or not os.path.exists(changelog_path):
        print("错误: 验证失败，文件不存在")
        return False
    
    current_chinese_format, current_iso_format = get_current_timestamp()
    current_date = datetime.datetime.now().date()
    
    # 验证README.md
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    readme_timestamp_match = re.search(r'\*\*最后更新时间：(.*?)\*\*', readme_content)
    if readme_timestamp_match:
        readme_timestamp = readme_timestamp_match.group(1)
        # 解析README中的日期
        try:
            readme_date_str = readme_timestamp.split(' ')[0]  # 获取日期部分
            readme_date = datetime.datetime.strptime(readme_date_str, "%Y年%m月%d日").date()
            
            if readme_date == current_date:
                print(f"✓ README.md日期验证成功：{readme_date_str}")
            else:
                print(f"✗ README.md日期验证失败：显示{readme_date_str}，当前应为{current_date.strftime('%Y年%m月%d日')}")
                return False
        except ValueError:
            print(f"✗ README.md日期格式验证失败：{readme_timestamp}")
            return False
    else:
        print("✗ README.md中未找到时间戳")
        return False
    
    # 验证CHANGELOG.md
    with open(changelog_path, 'r', encoding='utf-8') as f:
        changelog_content = f.read()
    
    changelog_timestamp_match = re.search(r'## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})', changelog_content)
    if changelog_timestamp_match:
        changelog_version = changelog_timestamp_match.group(1)
        changelog_date = changelog_timestamp_match.group(2)
        
        # 解析CHANGELOG中的日期
        try:
            changelog_date_obj = datetime.datetime.strptime(changelog_date, "%Y-%m-%d").date()
            
            if changelog_date_obj == current_date:
                print(f"✓ CHANGELOG.md版本 {changelog_version} 日期验证成功：{changelog_date}")
            else:
                print(f"✗ CHANGELOG.md日期验证失败：显示{changelog_date}，当前应为{current_date.strftime('%Y-%m-%d')}")
                return False
        except ValueError:
            print(f"✗ CHANGELOG.md日期格式验证失败：{changelog_date}")
            return False
    else:
        print("✗ CHANGELOG.md中未找到符合格式的版本时间戳")
        return False
    
    print("所有时间戳验证通过！")
    return True

def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='更新文档时间戳工具')
    parser.add_argument('--verify-only', action='store_true', help='仅验证时间戳，不进行更新')
    parser.add_argument('--readme', type=str, default='README.md', help='README.md文件路径')
    parser.add_argument('--changelog', type=str, default='CHANGELOG.md', help='CHANGELOG.md文件路径')
    
    args = parser.parse_args()
    
    # 获取绝对路径
    base_dir = Path(__file__).parent
    readme_path = os.path.join(base_dir, args.readme)
    changelog_path = os.path.join(base_dir, args.changelog)
    
    print(f"文档时间戳更新工具")
    print(f"- README.md: {readme_path}")
    print(f"- CHANGELOG.md: {changelog_path}")
    print()
    
    if args.verify_only:
        print("开始验证时间戳...")
        verify_timestamps(readme_path, changelog_path)
    else:
        print("开始更新时间戳...")
        # 更新README.md
        readme_success = update_readme_timestamp(readme_path)
        
        # 更新CHANGELOG.md
        changelog_success = update_changelog_timestamp(changelog_path)
        
        if readme_success and changelog_success:
            print()
            print("更新完成！开始验证...")
            verify_timestamps(readme_path, changelog_path)
        else:
            print("更新失败，请检查错误信息")

if __name__ == "__main__":
    main()