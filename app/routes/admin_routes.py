from flask import Blueprint, jsonify, request, send_file
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
import os
from app.models.admin_user import AdminUser
from app.utils.db import db
from app.services.folk_culture_service import FolkCultureService

# 创建admin蓝图
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# 安全中间件 - 检查请求来源
@admin_bp.before_request
def check_admin_access():
    # 允许登录和注册接口
    if request.endpoint in ['admin.login', 'admin.register']:
        return
    
    # 检查JWT认证
    if not request.headers.get('Authorization'):
        return jsonify({'message': '未授权访问'}), 401
    
    # 检查Referer头，确保请求来自管理后台
    referer = request.headers.get('Referer', '')
    user_agent = request.headers.get('User-Agent', '')
    
    # 允许来自管理后台端口(5174)的请求
    if '5174' not in referer and 'admin' not in user_agent.lower():
        # 记录可疑访问
        print(f"可疑访问尝试: {request.remote_addr} - {request.path}")
        return jsonify({'message': '访问被拒绝'}), 403

# 模拟统计数据
stats_data = {
    'userCount': 156,
    'dataCount': 1284,
    'uploadCount': 35,
    'viewCount': 12500
}

# 模拟活动数据
recent_activities = [
    {
        'id': 1,
        'type': 'upload',
        'text': '管理员上传了新数据',
        'time': '今天 10:30'
    },
    {
        'id': 2,
        'type': 'user',
        'text': '新用户注册',
        'time': '昨天 14:20'
    },
    {
        'id': 3,
        'type': 'system',
        'text': '系统设置已更新',
        'time': '2天前'
    }
]

# 登录路由
@admin_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # 验证输入
    if not username or not password:
        return jsonify({'message': '用户名和密码不能为空'}), 400
    
    # 从数据库中查找用户
    admin_user = AdminUser.query.filter_by(username=username).first()
    
    # 验证用户是否存在以及密码是否正确
    if not admin_user or not check_password_hash(admin_user.password_hash, password):
        return jsonify({'message': '用户名或密码错误'}), 401
    
    # 创建访问令牌
    access_token = create_access_token(
        identity=username,
        expires_delta=timedelta(hours=24),
        additional_claims={
            'role': 'admin',
            'admin_id': admin_user.id  # 使用数据库中的管理员ID
        }
    )
    
    # 返回令牌和用户信息
    return jsonify({
        'token': access_token,
        'user': {
            'id': admin_user.id,
            'username': admin_user.username,
            'email': admin_user.email,
            'role': 'admin'
        }
    })

# 注册路由
@admin_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # 验证输入
    if not username or not email or not password:
        return jsonify({'message': '用户名、邮箱和密码不能为空'}), 400
    
    # 检查用户名是否已存在
    if AdminUser.query.filter_by(username=username).first():
        return jsonify({'message': '用户名已存在'}), 409
    
    # 检查邮箱是否已存在
    if AdminUser.query.filter_by(email=email).first():
        return jsonify({'message': '邮箱已被注册'}), 409
    
    # 创建新用户
    new_admin = AdminUser(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )
    
    db.session.add(new_admin)
    db.session.commit()
    
    return jsonify({'message': '管理员注册成功'}), 201

# 刷新令牌路由
@admin_bp.route('/auth/refresh', methods=['POST'])
@jwt_required()
def refresh_token():
    current_user = get_jwt_identity()
    
    # 创建新的访问令牌
    new_access_token = create_access_token(
        identity=current_user,
        expires_delta=timedelta(hours=24)
    )
    
    return jsonify({'token': new_access_token})

# 修改密码路由
@admin_bp.route('/auth/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    current_user = get_jwt_identity()
    admin_user = AdminUser.query.filter_by(username=current_user).first()
    
    if not admin_user:
        return jsonify({'message': '用户不存在'}), 404
    
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    # 验证输入
    if not old_password or not new_password:
        return jsonify({'message': '请提供旧密码和新密码'}), 400
    
    # 验证旧密码
    if not check_password_hash(admin_user.password_hash, old_password):
        return jsonify({'message': '旧密码错误'}), 401
    
    # 更新密码
    admin_user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    
    return jsonify({'message': '密码修改成功'})

# 获取仪表盘统计数据
@admin_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    # 返回仪表盘统计数据
    return jsonify(stats_data)

# 获取仪表盘数据
@admin_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard_data():
    # 返回仪表盘数据（兼容旧版API）
    return jsonify({
        'stats': stats_data,
        'recentActivities': recent_activities
    })

# 获取最近添加的数据
@admin_bp.route('/dashboard/recent', methods=['GET'])
@jwt_required()
def get_recent_data():
    limit = request.args.get('limit', 10, type=int)
    recent_cultures = FolkCultureService.get_latest_cultures(limit)
    return jsonify(recent_cultures)

# 获取数据分布统计
@admin_bp.route('/dashboard/distribution/<string:type>', methods=['GET'])
@jwt_required()
def get_data_distribution(type):
    if type == 'category':
        # 获取分类分布
        categories = FolkCultureService.get_all_categories()
        distribution = []
        for category in categories:
            count = len(FolkCultureService.get_cultures_by_category(category))
            distribution.append({
                'name': category,
                'count': count
            })
        return jsonify(distribution)
    elif type == 'region':
        # 获取地区分布
        regions = FolkCultureService.get_all_regions()
        distribution = []
        for region in regions:
            count = len(FolkCultureService.get_cultures_by_region(region['name']))
            distribution.append({
                'name': region['name'],
                'count': count
            })
        return jsonify(distribution)
    else:
        return jsonify({'message': '不支持的数据类型'}), 400

# 批量上传数据
@admin_bp.route('/batch-upload', methods=['POST'])
@jwt_required()
def batch_upload():
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({'message': '没有文件上传'}), 400
        
        file = request.files['file']
        data_type = request.form.get('data_type', 'folk_culture')
        upload_mode = request.form.get('mode', 'append')
        
        # 检查文件扩展名
        if not (file.filename.endswith('.csv') or file.filename.endswith('.xlsx')):
            return jsonify({'message': '只支持CSV和Excel文件'}), 400
        
        # 读取文件内容
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # 模拟处理数据
        success_count = len(df) - 2  # 模拟有2条失败
        warning_count = 0
        error_count = 2
        errors = [
            '第5行：名称不能为空',
            '第12行：地区代码格式不正确'
        ]
        
        # 模拟更新统计数据
        stats_data['uploadCount'] += 1
        stats_data['dataCount'] += success_count
        
        # 添加新活动记录
        recent_activities.insert(0, {
            'id': len(recent_activities) + 1,
            'type': 'upload',
            'text': f'管理员上传了{data_type}数据，成功{success_count}条',
            'time': datetime.now().strftime('%H:%M')
        })
        
        return jsonify({
            'successCount': success_count,
            'warningCount': warning_count,
            'errorCount': error_count,
            'errors': errors,
            'message': '上传完成'
        })
        
    except Exception as e:
        return jsonify({'message': f'上传失败：{str(e)}'}), 500

# 获取模板
@admin_bp.route('/templates/<data_type>', methods=['GET'])
@jwt_required()
def get_template(data_type):
    # 验证数据类型
    valid_types = ['folk_culture', 'users', 'events']
    if data_type not in valid_types:
        return jsonify({'message': '不支持的数据类型'}), 400
    
    # 返回模板信息（前端需要这些信息）
    return jsonify({
        'message': '模板获取成功',
        'data_type': data_type,
        'download_url': f'/api/admin/templates/{data_type}/download',
        'fields': [
            {'name': 'name', 'description': '名称', 'required': True},
            {'name': 'description', 'description': '描述', 'required': False},
            {'name': 'category', 'description': '分类', 'required': True}
        ]
    })

# 下载模板文件
@admin_bp.route('/templates/<data_type>/download', methods=['GET'])
@jwt_required()
def download_template(data_type):
    # 验证数据类型
    valid_types = ['folk_culture', 'users', 'events']
    if data_type not in valid_types:
        return jsonify({'message': '不支持的数据类型'}), 400
    
    # 创建一个简单的Excel模板
    df = pd.DataFrame({
        'name': ['示例名称'],
        'description': ['示例描述'],
        'category': ['示例分类']
    })
    
    # 创建内存中的Excel文件
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=data_type)
    output.seek(0)
    
    # 返回文件
    filename = f'{data_type}_template.xlsx'
    return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# 获取用户信息
@admin_bp.route('/auth/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    admin_user = AdminUser.query.filter_by(username=current_user).first()
    
    if admin_user:
        return jsonify({
            'username': admin_user.username,
            'email': admin_user.email
        })
    
    return jsonify({'message': '用户不存在'}), 404

# 退出登录
@admin_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # JWT是无状态的，客户端删除token即可
    return jsonify({'message': '退出成功'}), 200

# 民俗文化管理路由
@admin_bp.route('/folk-culture', methods=['GET'])
@jwt_required()
def admin_get_folk_culture_list():
    """获取民俗文化列表（管理员专用，支持分页和筛选）"""
    # 这里可以添加更复杂的筛选和分页逻辑
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    region = request.args.get('region')
    
    # 获取所有文化
    cultures = FolkCultureService.get_all_cultures()
    
    # 应用筛选
    if category:
        cultures = [c for c in cultures if c['category'] == category]
    if region:
        cultures = [c for c in cultures if c['region'] == region]
    
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

@admin_bp.route('/folk-culture/<int:id>', methods=['GET'])
@jwt_required()
def admin_get_folk_culture_detail(id):
    """获取单个民俗文化详情（管理员专用）"""
    culture = FolkCultureService.get_culture_by_id(id)
    if not culture:
        return jsonify({'error': '民俗文化信息不存在'}), 404
    return jsonify(culture)

@admin_bp.route('/folk-culture', methods=['POST'])
@jwt_required()
def admin_create_folk_culture():
    """创建民俗文化（管理员专用）"""
    data = request.get_json()
    try:
        # 这里可以添加更严格的管理员权限验证和数据验证
        result = FolkCultureService.create_culture(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@admin_bp.route('/folk-culture/<int:id>', methods=['PUT'])
@jwt_required()
def admin_update_folk_culture(id):
    """更新民俗文化（管理员专用）"""
    data = request.get_json()
    result = FolkCultureService.update_culture(id, data)
    if not result:
        return jsonify({'error': '民俗文化信息不存在'}), 404
    return jsonify(result)

@admin_bp.route('/folk-culture/<int:id>', methods=['DELETE'])
@jwt_required()
def admin_delete_folk_culture(id):
    """删除民俗文化（管理员专用）"""
    success = FolkCultureService.delete_culture(id)
    if not success:
        return jsonify({'error': '民俗文化信息不存在'}), 404
    return jsonify({'message': '删除成功'})

@admin_bp.route('/folk-culture/batch', methods=['DELETE'])
@jwt_required()
def admin_batch_delete_folk_culture():
    """批量删除民俗文化（管理员专用）"""
    data = request.get_json()
    ids = data.get('ids', [])
    if not isinstance(ids, list) or not ids:
        return jsonify({'error': '请提供有效的ID列表'}), 400
    
    result = FolkCultureService.batch_delete_cultures(ids)
    return jsonify(result)

@admin_bp.route('/folk-culture/batch-upload', methods=['POST'])
@jwt_required()
def batch_upload_folk_culture():
    """批量上传民俗文化数据"""
    # 复用原有的批量上传逻辑
    return batch_upload()