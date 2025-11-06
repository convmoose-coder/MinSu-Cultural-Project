from typing import List, Optional, Dict, Any
from app.models.folk_culture import FolkCulture
from app.schemas.folk_culture import FolkCultureCreate
from app.utils.db import db
from sqlalchemy import desc, or_
import random
from datetime import datetime

class FolkCultureService:
    """民俗文化服务类"""
    
    @staticmethod
    def get_all_cultures() -> List[dict]:
        """获取所有民俗文化信息"""
        cultures = FolkCulture.query.all()
        return [culture.to_dict() for culture in cultures]
    
    @staticmethod
    def get_culture_by_id(id: int) -> Optional[dict]:
        """根据ID获取民俗文化详情"""
        culture = FolkCulture.query.get(id)
        return culture.to_dict() if culture else None
    
    @staticmethod
    def create_culture(data: Any) -> dict:
        """创建新的民俗文化记录，支持schema对象和字典"""
        # 支持从schema对象或字典创建
        if hasattr(data, 'dict'):
            data_dict = data.dict()
        else:
            data_dict = data
        
        new_culture = FolkCulture(
            title=data_dict.get('title', data_dict.get('name', '')),
            description=data_dict.get('description', ''),
            category=data_dict.get('category', ''),
            region=data_dict.get('region', ''),
            view_count=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(new_culture)
        db.session.commit()
        return new_culture.to_dict()
    
    @staticmethod
    def get_all_regions() -> List[str]:
        """获取所有地区名称"""
        regions = db.session.query(FolkCulture.region).distinct().all()
        # 返回地区名称列表
        return [region[0] for region in regions]
    
    @staticmethod
    def get_region_by_id(id: int) -> Optional[Dict]:
        """根据ID获取地区详情"""
        region_names = FolkCultureService.get_all_regions()
        # 重新创建包含id和name的格式
        regions = [{'id': i + 1, 'name': region} for i, region in enumerate(region_names)]
        for region in regions:
            if region['id'] == id:
                # 获取该地区的文化数量
                culture_count = FolkCulture.query.filter_by(region=region['name']).count()
                return {
                    **region,
                    'culture_count': culture_count
                }
        return None
    
    @staticmethod
    def get_region_features(region_id: int) -> List[Dict]:
        """获取地区文化特色"""
        region_names = FolkCultureService.get_all_regions()
        # 重新创建包含id和name的格式
        regions = [{'id': i + 1, 'name': region} for i, region in enumerate(region_names)]
        region_name = None
        
        for region in regions:
            if region['id'] == region_id:
                region_name = region['name']
                break
        
        if not region_name:
            return []
        
        # 获取该地区的所有文化类别及其数量
        cultures = FolkCulture.query.filter_by(region=region_name).all()
        category_count = {}
        
        for culture in cultures:
            if culture.category in category_count:
                category_count[culture.category] += 1
            else:
                category_count[culture.category] = 1
        
        # 转换为所需格式
        return [{
            'category': category,
            'count': count
        } for category, count in category_count.items()]
    
    @staticmethod
    def get_all_categories() -> List[str]:
        """获取所有唯一的分类"""
        categories = db.session.query(FolkCulture.category).distinct().all()
        return [category[0] for category in categories]
    
    @staticmethod
    def get_popular_cultures(limit: int = 5) -> List[dict]:
        """获取热门民俗文化（模拟实现，基于ID倒序）"""
        cultures = FolkCulture.query.order_by(desc(FolkCulture.id)).limit(limit).all()
        return [culture.to_dict() for culture in cultures]
    
    @staticmethod
    def get_latest_cultures(limit: int = 5) -> List[dict]:
        """获取最新添加的民俗文化"""
        cultures = FolkCulture.query.order_by(desc(FolkCulture.id)).limit(limit).all()
        return [culture.to_dict() for culture in cultures]
    
    @staticmethod
    def get_cultures_by_category(category: str) -> List[dict]:
        """根据类别获取民俗文化"""
        cultures = FolkCulture.query.filter_by(category=category).all()
        return [culture.to_dict() for culture in cultures]
    
    @staticmethod
    def get_cultures_by_region(region: str) -> List[dict]:
        """根据地区获取民俗文化"""
        cultures = FolkCulture.query.filter_by(region=region).all()
        return [culture.to_dict() for culture in cultures]
    
    @staticmethod
    def update_culture(id: int, data: dict) -> Optional[dict]:
        """更新民俗文化信息"""
        culture = FolkCulture.query.get(id)
        if not culture:
            return None
        
        for key, value in data.items():
            if hasattr(culture, key):
                setattr(culture, key, value)
        
        db.session.commit()
        return culture.to_dict()
    
    @staticmethod
    def delete_culture(id: int) -> bool:
        """删除指定ID的民俗文化记录"""
        try:
            culture = FolkCulture.query.get(id)
            if culture:
                db.session.delete(culture)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            return False
    
    @staticmethod
    def search_cultures(keyword: str) -> List[dict]:
        """搜索民俗文化信息"""
        keyword = keyword.lower()
        cultures = FolkCulture.query.filter(
            or_(
                FolkCulture.title.ilike(f'%{keyword}%'),
                FolkCulture.description.ilike(f'%{keyword}%')
            )
        ).all()
        return [culture.to_dict() for culture in cultures]
    
    @staticmethod
    def get_recommended_cultures(limit: int = 5) -> List[dict]:
        """获取推荐的民俗文化"""
        # 获取所有文化，然后随机选择
        all_cultures = FolkCulture.query.all()
        if len(all_cultures) <= limit:
            return [culture.to_dict() for culture in all_cultures]
        
        # 随机选择limit个文化
        selected_cultures = random.sample(all_cultures, limit)
        return [culture.to_dict() for culture in selected_cultures]
    
    @staticmethod
    def increment_view_count(id: int) -> bool:
        """增加民俗文化的浏览量"""
        culture = FolkCulture.query.get(id)
        if not culture:
            return False
        
        # 确保view_count属性存在
        if hasattr(culture, 'view_count'):
            culture.view_count = (culture.view_count or 0) + 1
            db.session.commit()
        return True
    
    @staticmethod
    def get_carousel_items() -> List[dict]:
        """获取轮播图数据"""
        # 获取最新的几个文化作为轮播图
        cultures = FolkCulture.query.order_by(desc(FolkCulture.id)).limit(5).all()
        carousel_items = []
        
        for culture in cultures:
            item = {
                'id': culture.id,
                'title': culture.title,
                'description': culture.description[:100] + '...' if len(culture.description) > 100 else culture.description,
                'image': '',  # 如果有图片字段，可以在这里添加
                'link': f'/detail/{culture.id}'
            }
            carousel_items.append(item)
        
        return carousel_items
    
    @staticmethod
    def batch_delete_cultures(ids: List[int]) -> dict:
        """批量删除民俗文化信息"""
        success_count = 0
        
        for id in ids:
            if FolkCultureService.delete_culture(id):
                success_count += 1
        
        return {
            'success_count': success_count,
            'total_count': len(ids)
        }
    
    @staticmethod
    def get_total_cultures() -> int:
        """获取民俗文化总数"""
        return FolkCulture.query.count()
    
    @staticmethod
    def get_total_categories() -> int:
        """获取分类总数"""
        return len(FolkCultureService.get_all_categories())
    
    @staticmethod
    def get_total_regions() -> int:
        """获取地区总数"""
        return len(FolkCultureService.get_all_regions())
    
    @staticmethod
    def get_related_cultures(id: int, limit: int = 4) -> List[dict]:
        """获取相关的民俗文化"""
        current_culture = FolkCulture.query.get(id)
        if not current_culture:
            return []
        
        # 根据相同分类获取相关文化
        related_cultures = FolkCulture.query.filter(
            FolkCulture.category == current_culture.category,
            FolkCulture.id != id
        ).limit(limit).all()
        
        # 如果同分类的文化不够，则补充同地区的文化
        if len(related_cultures) < limit:
            additional_cultures = FolkCulture.query.filter(
                FolkCulture.region == current_culture.region,
                FolkCulture.id != id,
                ~FolkCulture.id.in_([c.id for c in related_cultures])
            ).limit(limit - len(related_cultures)).all()
            related_cultures.extend(additional_cultures)
        
        return [culture.to_dict() for culture in related_cultures]
    
    @staticmethod
    def advanced_search(name: str = '', description: str = '', category: str = '', region: str = '') -> List[dict]:
        """高级搜索功能"""
        query = FolkCulture.query
        
        if name:
            query = query.filter(FolkCulture.title.ilike(f'%{name}%'))
        if description:
            query = query.filter(FolkCulture.description.ilike(f'%{description}%'))
        if category:
            query = query.filter(FolkCulture.category == category)
        if region:
            query = query.filter(FolkCulture.region == region)
        
        cultures = query.all()
        return [culture.to_dict() for culture in cultures]
    
    @staticmethod
    def get_popular_cultures_by_views(limit: int = 5) -> List[dict]:
        """根据浏览量获取热门民俗文化"""
        # 尝试按浏览量排序，如果没有view_count字段则按ID排序
        try:
            cultures = FolkCulture.query.order_by(desc(FolkCulture.view_count)).limit(limit).all()
        except:
            # 如果view_count字段不存在，回退到按ID排序
            cultures = FolkCulture.query.order_by(desc(FolkCulture.id)).limit(limit).all()
        
        return [culture.to_dict() for culture in cultures]
    
    @staticmethod
    def update_culture_with_dict(id: int, data: Dict) -> Optional[dict]:
        """使用字典更新民俗文化信息"""
        return FolkCultureService.update_culture(id, data)
    
    @staticmethod
    def get_cultures_by_ids(ids: List[int]) -> List[dict]:
        """根据ID列表获取民俗文化"""
        cultures = FolkCulture.query.filter(FolkCulture.id.in_(ids)).all()
        return [culture.to_dict() for culture in cultures]
    
    @staticmethod
    def get_cultures_paginated(page: int = 1, per_page: int = 10, **filters) -> Dict:
        """分页获取民俗文化"""
        query = FolkCulture.query
        
        # 应用过滤条件
        for key, value in filters.items():
            if hasattr(FolkCulture, key) and value is not None:
                if isinstance(value, str) and '%' not in value:
                    query = query.filter(getattr(FolkCulture, key).ilike(f'%{value}%'))
                else:
                    query = query.filter(getattr(FolkCulture, key) == value)
        
        # 分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': [item.to_dict() for item in pagination.items],
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages,
            'per_page': pagination.per_page
        }
