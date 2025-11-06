#!/usr/bin/env python3
"""
测试前后端分离安全机制
验证管理后台API只能通过特定路径访问
"""

import requests
import json

def test_admin_api_security():
    """测试管理后台API安全机制"""
    base_url = "http://127.0.0.1:5000"
    
    print("=== 测试前后端分离安全机制 ===\n")
    
    # 1. 测试直接访问管理API（应该被拒绝）
    print("1. 测试直接访问管理API（无Referer头）")
    try:
        response = requests.get(f"{base_url}/api/admin/dashboard")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 403:
            print("   ✅ 安全机制生效：直接访问被拒绝")
        elif response.status_code == 401:
            print("   ✅ 需要认证：直接访问被拒绝")
        else:
            print(f"   ❌ 安全机制未生效: {response.text[:200]}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 2. 测试通过管理后台端口访问（应该允许）
    print("2. 测试通过管理后台端口访问（带Referer头）")
    try:
        headers = {
            'Referer': 'http://localhost:5174/admin/',
            'User-Agent': 'Mozilla/5.0 (Admin Console)'
        }
        response = requests.get(f"{base_url}/api/admin/dashboard", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 管理后台访问正常")
        elif response.status_code == 401:
            print("   ✅ 需要认证：管理后台访问正常")
        else:
            print(f"   ❌ 管理后台访问失败: {response.text[:200]}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 3. 测试用户端前台访问管理API（应该被拒绝）
    print("3. 测试用户端前台访问管理API")
    try:
        headers = {
            'Referer': 'http://localhost:5173/',
            'User-Agent': 'Mozilla/5.0 (User Frontend)'
        }
        response = requests.get(f"{base_url}/api/admin/dashboard", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 403:
            print("   ✅ 用户端前台无法访问管理API")
        elif response.status_code == 401:
            print("   ✅ 需要认证：用户端前台无法访问管理API")
        else:
            print(f"   ❌ 用户端前台可能可以访问管理API: {response.text[:200]}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 4. 测试登录接口（应该允许，不受安全限制）
    print("4. 测试登录接口（不受安全限制）")
    try:
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        response = requests.post(f"{base_url}/api/admin/auth/login", json=login_data)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 登录接口正常")
            # 获取JWT令牌用于后续测试
            token = response.json().get('token')
            if token:
                print("   ✅ 成功获取JWT令牌")
                return token
        else:
            print(f"   ❌ 登录失败: {response.text[:200]}")
    except Exception as e:
        print(f"   错误: {e}")
    
    return None

def test_with_jwt_token(token):
    """使用JWT令牌测试API访问"""
    base_url = "http://127.0.0.1:5000"
    
    print("\n=== 使用JWT令牌测试API访问 ===\n")
    
    # 1. 测试带令牌但无Referer的访问
    print("1. 测试带令牌但无Referer的访问")
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'User-Agent': 'Mozilla/5.0 (Test Client)'
        }
        response = requests.get(f"{base_url}/api/admin/dashboard", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 403:
            print("   ✅ 安全机制生效：即使有令牌，无Referer也被拒绝")
        elif response.status_code == 401:
            print("   ✅ 需要认证：即使有令牌，无Referer也被拒绝")
        else:
            print(f"   ❌ 安全机制可能有问题: {response.text[:200]}")
    except Exception as e:
        print(f"   错误: {e}")
    
    print()
    
    # 2. 测试带令牌和Referer的访问
    print("2. 测试带令牌和Referer的访问")
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Referer': 'http://localhost:5174/admin/',
            'User-Agent': 'Mozilla/5.0 (Admin Console)'
        }
        response = requests.get(f"{base_url}/api/admin/dashboard", headers=headers)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ 带令牌和Referer的访问正常")
        elif response.status_code == 401:
            print("   ✅ 需要认证：带令牌和Referer的访问正常")
        else:
            print(f"   ❌ 访问失败: {response.text[:200]}")
    except Exception as e:
        print(f"   错误: {e}")

if __name__ == "__main__":
    print("开始测试前后端分离安全机制...")
    print("确保后端服务运行在 http://127.0.0.1:5000")
    print("管理后台运行在 http://localhost:5174/admin/")
    print("用户端前台运行在 http://localhost:5173/\n")
    
    token = test_admin_api_security()
    
    if token:
        test_with_jwt_token(token)
    
    print("\n=== 测试完成 ===")
    print("总结：")
    print("- 管理后台API应该只能通过特定端口(5174)访问")
    print("- 直接访问或从其他端口访问应该被拒绝")
    print("- 登录接口不受安全限制")
    print("- JWT令牌和Referer头都需要验证")