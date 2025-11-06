from flask import Blueprint, jsonify, request
from app.services.folk_culture_service import FolkCultureService
from app.schemas.folk_culture import FolkCultureCreate

# 创建前台路由蓝图（游客专用）
public_bp = Blueprint('public', __name__, url_prefix='/api')

# 获取所有民俗文化列表（前台游客访问）
@public_bp.route('/folk-culture', methods=['GET'])
def get_folk_culture_list():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    region = request.args.get('region')
    search = request.args.get('search')
    
    # 获取所有文化
    cultures = FolkCultureService.get_all_cultures()
    
    # 应用筛选
    if category:
        cultures = [c for c in cultures if c['category'] == category]
    if region:
        cultures = [c for c in cultures if c['region'] == region]
    if search:
        search = search.lower()
        cultures = [c for c in cultures if 'name' in c and search in c['name'].lower() or 'description' in c and search in c['description'].lower()]
    
    # 应用分页
    total = len(cultures)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_cultures = cultures[start:end]
    
    return jsonify({
        'data': paginated_cultures,
        'pagination': {
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    })

# 获取单个民俗文化详情（前台游客访问）
@public_bp.route('/folk-culture/<int:id>', methods=['GET'])
def get_folk_culture_detail(id):
    culture = FolkCultureService.get_culture_by_id(id)
    if not culture:
        return jsonify({'error': '民俗文化信息不存在'}), 404
    
    # 增加浏览量（可以在service层实现）
    FolkCultureService.increment_view_count(id)
    
    return jsonify(culture)

# 获取所有分类（前台游客访问）
@public_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = FolkCultureService.get_all_categories()
    return jsonify(categories)

# 获取所有地区（前台游客访问）
@public_bp.route('/regions', methods=['GET'])
def get_regions():
    regions = FolkCultureService.get_all_regions()
    return jsonify(regions)

# 搜索民俗文化（前台游客访问）
@public_bp.route('/search', methods=['GET'])
def search_folk_culture():
    keyword = request.args.get('q', '')
    if not keyword:
        return jsonify([])
    
    results = FolkCultureService.search_cultures(keyword)
    return jsonify(results)

# 获取热门民俗文化（前台游客访问）
@public_bp.route('/popular', methods=['GET'])
def get_popular_cultures():
    limit = request.args.get('limit', 10, type=int)
    popular_cultures = FolkCultureService.get_popular_cultures(limit)
    return jsonify(popular_cultures)

# 获取推荐民俗文化（前台游客访问）
@public_bp.route('/recommended', methods=['GET'])
def get_recommended_cultures():
    limit = request.args.get('limit', 5, type=int)
    recommended_cultures = FolkCultureService.get_recommended_cultures(limit)
    return jsonify(recommended_cultures)

# 获取首页推荐数据（前台游客访问）
@public_bp.route('/home', methods=['GET'])
def get_home_data():
    # 获取首页所需的全部数据
    popular_cultures = FolkCultureService.get_popular_cultures(5)
    latest_cultures = FolkCultureService.get_latest_cultures(5)
    categories = FolkCultureService.get_all_categories()[:6]  # 只返回前6个分类
    regions = FolkCultureService.get_all_regions()[:6]  # 只返回前6个地区
    
    return jsonify({
        'popular': popular_cultures,
        'latest': latest_cultures,
        'categories': categories,
        'regions': regions
    })

# 获取轮播图数据（前台游客访问）
@public_bp.route('/carousel', methods=['GET'])
def get_carousel_data():
    carousel_items = FolkCultureService.get_carousel_items()
    return jsonify(carousel_items)

# 获取民俗文化统计数据（前台游客访问）
@public_bp.route('/stats', methods=['GET'])
def get_public_stats():
    # 获取公开的统计数据
    total_cultures = FolkCultureService.get_total_cultures()
    total_categories = FolkCultureService.get_total_categories()
    total_regions = FolkCultureService.get_total_regions()
    
    return jsonify({
        'total_cultures': total_cultures,
        'total_categories': total_categories,
        'total_regions': total_regions
    })

# 相关推荐（基于当前民俗文化获取相关推荐）
@public_bp.route('/folk-culture/<int:id>/related', methods=['GET'])
def get_related_cultures(id):
    current_culture = FolkCultureService.get_culture_by_id(id)
    if not current_culture:
        return jsonify({'error': '民俗文化信息不存在'}), 404
    
    limit = request.args.get('limit', 4, type=int)
    related_cultures = FolkCultureService.get_related_cultures(id, limit)
    return jsonify(related_cultures)

# 按分类获取民俗文化（前台游客访问）
@public_bp.route('/category/<string:category_name>', methods=['GET'])
def get_cultures_by_category(category_name):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    cultures = FolkCultureService.get_cultures_by_category(category_name)
    
    # 应用分页
    total = len(cultures)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_cultures = cultures[start:end]
    
    return jsonify({
        'data': paginated_cultures,
        'pagination': {
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    })

# 按地区获取民俗文化（前台游客访问）
@public_bp.route('/region/<string:region_name>', methods=['GET'])
def get_cultures_by_region(region_name):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    cultures = FolkCultureService.get_cultures_by_region(region_name)
    
    # 应用分页
    total = len(cultures)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_cultures = cultures[start:end]
    
    return jsonify({
        'data': paginated_cultures,
        'pagination': {
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    })

# 高级搜索接口（前台游客访问）
@public_bp.route('/advanced-search', methods=['GET'])
def advanced_search():
    # 获取高级搜索参数
    name = request.args.get('name', '')
    description = request.args.get('description', '')
    category = request.args.get('category', '')
    region = request.args.get('region', '')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 执行高级搜索
    results = FolkCultureService.advanced_search(name, description, category, region)
    
    # 应用分页
    total = len(results)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = results[start:end]
    
    return jsonify({
        'data': paginated_results,
        'pagination': {
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        }
    })
