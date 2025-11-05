from flask import Blueprint, jsonify, request
from app.services.folk_culture_service import FolkCultureService
from app.schemas.folk_culture import FolkCultureCreate

# 创建蓝图
folk_culture_bp = Blueprint('folk_culture', __name__)

@folk_culture_bp.route('/folkcultures', methods=['GET'])
def get_folk_cultures():
    """获取所有民俗文化信息"""
    cultures = FolkCultureService.get_all_cultures()
    return jsonify(cultures)

@folk_culture_bp.route('/folkcultures/<int:id>', methods=['GET'])
def get_folk_culture(id):
    """根据ID获取民俗文化详情"""
    culture = FolkCultureService.get_culture_by_id(id)
    if not culture:
        return jsonify({'error': '民俗文化信息不存在'}), 404
    return jsonify(culture)

@folk_culture_bp.route('/folkcultures', methods=['POST'])
def create_folk_culture():
    """创建新的民俗文化记录"""
    data = request.get_json()
    try:
        # 验证数据
        if not all(key in data for key in ['title', 'description', 'category', 'region']):
            return jsonify({'error': '缺少必要的字段'}), 400
        
        # 创建请求模型
        folk_culture_data = FolkCultureCreate(
            title=data.get('title'),
            description=data.get('description'),
            category=data.get('category'),
            region=data.get('region')
        )
        
        result = FolkCultureService.create_culture(folk_culture_data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@folk_culture_bp.route('/regions', methods=['GET'])
def get_regions():
    """获取所有地区"""
    regions = FolkCultureService.get_all_regions()
    return jsonify(regions)

@folk_culture_bp.route('/categories', methods=['GET'])
def get_categories():
    """获取所有分类"""
    categories = FolkCultureService.get_all_categories()
    return jsonify(categories)
