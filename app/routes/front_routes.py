from flask import Blueprint, render_template, request, jsonify
from app.services.folk_culture_service import FolkCultureService

# 创建前台路由蓝图
front_bp = Blueprint('front', __name__, url_prefix='/')

@front_bp.route('/', methods=['GET'])
def index():
    """前台首页"""
    # 获取统计数据
    stats = {
        'total_cultures': FolkCultureService.get_total_cultures(),
        'total_categories': FolkCultureService.get_total_categories(),
        'total_regions': FolkCultureService.get_total_regions()
    }
    # 获取推荐文化
    recommended_cultures = FolkCultureService.get_recommended_cultures(8)
    # 获取热门文化
    popular_cultures = FolkCultureService.get_popular_cultures_by_views(5)
    # 获取轮播图数据
    carousel_items = FolkCultureService.get_carousel_items()
    
    return render_template('front/index.html', 
                          stats=stats,
                          recommended_cultures=recommended_cultures,
                          popular_cultures=popular_cultures,
                          carousel_items=carousel_items)

@front_bp.route('/list', methods=['GET'])
def culture_list():
    """民俗文化列表页"""
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    region = request.args.get('region', '')
    keyword = request.args.get('keyword', '')
    
    # 构建过滤条件
    filters = {}
    if category:
        filters['category'] = category
    if region:
        filters['region'] = region
    
    # 如果有关键词，使用搜索功能
    if keyword:
        cultures = FolkCultureService.search_cultures(keyword)
        # 模拟分页
        total = len(cultures)
        per_page = 10
        start = (page - 1) * per_page
        end = start + per_page
        page_cultures = cultures[start:end]
        
        pagination = {
            'items': page_cultures,
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page,
            'per_page': per_page
        }
    else:
        # 使用分页查询
        pagination = FolkCultureService.get_cultures_paginated(page=page, **filters)
    
    # 获取所有分类和地区用于筛选
    categories = FolkCultureService.get_all_categories()
    regions = FolkCultureService.get_all_regions()
    
    # 添加调试信息
    print(f"Pagination type: {type(pagination)}")
    print(f"Pagination keys: {list(pagination.keys()) if isinstance(pagination, dict) else 'Not a dict'}")
    if isinstance(pagination, dict) and 'items' in pagination:
        print(f"Items type: {type(pagination['items'])}")
        print(f"Items is iterable: {hasattr(pagination['items'], '__iter__')}")
    
    return render_template('front/list.html', 
                          pagination=pagination,
                          categories=categories,
                          regions=regions,
                          current_category=category,
                          current_region=region,
                          keyword=keyword)

@front_bp.route('/detail/<int:id>', methods=['GET'])
def culture_detail(id):
    """民俗文化详情页"""
    # 获取文化详情
    culture = FolkCultureService.get_culture_by_id(id)
    if not culture:
        return render_template('front/404.html'), 404
    
    # 增加浏览量
    FolkCultureService.increment_view_count(id)
    
    # 获取相关文化推荐
    related_cultures = FolkCultureService.get_related_cultures(id, 4)
    
    return render_template('front/detail.html', 
                          culture=culture,
                          related_cultures=related_cultures)

@front_bp.route('/search', methods=['GET'])
def search():
    """搜索页面"""
    keyword = request.args.get('keyword', '', type=str)
    results = []
    
    if keyword:
        results = FolkCultureService.search_cultures(keyword)
    
    return render_template('front/search.html', 
                          keyword=keyword,
                          results=results)

@front_bp.route('/category/<string:category>', methods=['GET'])
def category_page(category):
    """分类页面"""
    page = request.args.get('page', 1, type=int)
    pagination = FolkCultureService.get_cultures_paginated(page=page, category=category)
    
    return render_template('front/category.html', 
                          category=category,
                          pagination=pagination)

@front_bp.route('/region/<string:region>', methods=['GET'])
def region_page(region):
    """地区页面"""
    page = request.args.get('page', 1, type=int)
    pagination = FolkCultureService.get_cultures_paginated(page=page, region=region)
    
    return render_template('front/region.html', 
                          region=region,
                          pagination=pagination)

@front_bp.route('/about', methods=['GET'])
def about():
    """关于页面"""
    return render_template('front/about.html')

@front_bp.route('/contact', methods=['GET'])
def contact():
    """联系页面"""
    return render_template('front/contact.html')

# API路由
def register_api_routes(app):
    """注册API路由"""
    @app.route('/api/cultures', methods=['GET'])
    def api_cultures():
        """获取民俗文化列表API"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取过滤参数
        filters = {}
        for field in ['category', 'region']:
            value = request.args.get(field)
            if value:
                filters[field] = value
        
        pagination = FolkCultureService.get_cultures_paginated(
            page=page, 
            per_page=per_page, 
            **filters
        )
        
        return jsonify(pagination)
    
    @app.route('/api/cultures/<int:id>', methods=['GET'])
    def api_culture_detail(id):
        """获取民俗文化详情API"""
        culture = FolkCultureService.get_culture_by_id(id)
        if not culture:
            return jsonify({'error': '文化信息不存在'}), 404
        
        # 增加浏览量
        FolkCultureService.increment_view_count(id)
        
        return jsonify(culture)
    
    @app.route('/api/search', methods=['GET'])
    def api_search():
        """搜索API"""
        keyword = request.args.get('keyword', '', type=str)
        if not keyword:
            return jsonify({'error': '请提供搜索关键词'}), 400
        
        results = FolkCultureService.search_cultures(keyword)
        return jsonify({
            'keyword': keyword,
            'total': len(results),
            'results': results
        })
    
    @app.route('/api/recommended', methods=['GET'])
    def api_recommended():
        """获取推荐文化API"""
        limit = request.args.get('limit', 5, type=int)
        cultures = FolkCultureService.get_recommended_cultures(limit)
        return jsonify(cultures)
    
    @app.route('/api/popular', methods=['GET'])
    def api_popular():
        """获取热门文化API"""
        limit = request.args.get('limit', 5, type=int)
        cultures = FolkCultureService.get_popular_cultures_by_views(limit)
        return jsonify(cultures)
    
    @app.route('/api/carousel', methods=['GET'])
    def api_carousel():
        """获取轮播图数据API"""
        items = FolkCultureService.get_carousel_items()
        return jsonify(items)
    
    @app.route('/api/categories', methods=['GET'])
    def api_categories():
        """获取所有分类API"""
        categories = FolkCultureService.get_all_categories()
        return jsonify(categories)
    
    @app.route('/api/regions', methods=['GET'])
    def api_regions():
        """获取所有地区API"""
        regions = FolkCultureService.get_all_regions()
        return jsonify(regions)
    
    @app.route('/api/stats', methods=['GET'])
    def api_stats():
        """获取统计数据API"""
        stats = {
            'total_cultures': FolkCultureService.get_total_cultures(),
            'total_categories': FolkCultureService.get_total_categories(),
            'total_regions': FolkCultureService.get_total_regions()
        }
        return jsonify(stats)

# 定义一个函数来注册前台路由
def register_front_routes(app):
    """注册前台路由"""
    app.register_blueprint(front_bp)
    # 注册API路由
    register_api_routes(app)
    
    # 注册404错误处理
    @app.errorhandler(404)
    def page_not_found(e):
        # 获取推荐文化和分类数据用于错误页面展示
        from app.services.folk_culture_service import FolkCultureService
        
        # 获取推荐文化（限制数量，避免加载过多）
        recommended_cultures = FolkCultureService.get_recommended_cultures(6)
        
        # 获取所有分类
        categories = FolkCultureService.get_all_categories()
        
        # 获取当前年份
        from datetime import datetime
        current_year = datetime.now().year
        
        # 渲染404页面，传递推荐文化和分类数据
        return render_template('front/404.html', 
                               recommended_cultures=recommended_cultures,
                               categories=categories,
                               current_year=current_year), 404