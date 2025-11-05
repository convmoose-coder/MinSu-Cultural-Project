from typing import List, Optional
from app.models import FolkCulture
from app.schemas.folk_culture import FolkCultureCreate
from app.utils.db import db

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
    def create_culture(data: FolkCultureCreate) -> dict:
        """创建新的民俗文化记录"""
        new_culture = FolkCulture(
            title=data.title,
            description=data.description,
            category=data.category,
            region=data.region
        )
        db.session.add(new_culture)
        db.session.commit()
        return {
            'id': new_culture.id,
            'title': new_culture.title,
            'message': '民俗文化信息创建成功'
        }
    
    @staticmethod
    def get_all_regions() -> List[str]:
        """获取所有唯一的地区"""
        regions = db.session.query(FolkCulture.region).distinct().all()
        return [region[0] for region in regions]
    
    @staticmethod
    def get_all_categories() -> List[str]:
        """获取所有唯一的分类"""
        categories = db.session.query(FolkCulture.category).distinct().all()
        return [category[0] for category in categories]
