import os
import sys
from app.utils.db import db, init_db
from app import create_app
from app.models.folk_culture import FolkCulture

# 创建Flask应用
app = create_app()

# 初始化数据库
with app.app_context():
    # 创建所有表
    db.create_all()
    
    # 创建几个示例民俗文化记录
    sample_cultures = [
        {
            'title': '春节习俗',
            'description': '中国最重要的传统节日，包含贴春联、吃年夜饭、放鞭炮等习俗',
            'category': '传统节日',
            'region': '全国'
        },
        {
            'title': '剪纸艺术',
            'description': '用剪刀或刻刀在纸上剪刻花纹，用于装饰生活或配合其他民俗活动',
            'category': '传统工艺',
            'region': '华北地区'
        },
        {
            'title': '京剧表演',
            'description': '中国传统戏曲之一，以唱、念、做、打为表演手段',
            'category': '民间艺术',
            'region': '北京'
        },
        {
            'title': '端午节习俗',
            'description': '纪念屈原的传统节日，有吃粽子、赛龙舟等习俗',
            'category': '传统节日',
            'region': '江南地区'
        },
        {
            'title': '皮影戏',
            'description': '用兽皮或纸板做成的人物剪影来表演故事的民间戏剧',
            'category': '民间艺术',
            'region': '西北地区'
        }
    ]
    
    for culture_data in sample_cultures:
        # 检查是否已存在相同标题的记录
        existing = FolkCulture.query.filter_by(title=culture_data['title']).first()
        if not existing:
            culture = FolkCulture(**culture_data)
            db.session.add(culture)
    
    # 提交更改
    db.session.commit()
    print("数据库初始化成功！")
    print("已创建表结构和示例数据。")
    print(f"成功创建了 {len(sample_cultures)} 条民俗文化记录。")