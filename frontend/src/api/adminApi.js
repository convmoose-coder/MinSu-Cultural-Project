import axios from 'axios'

// 创建后台API实例
const adminApi = axios.create({
  baseURL: '/api/admin',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加认证token
adminApi.interceptors.request.use(
  config => {
    const token = localStorage.getItem('adminToken')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误和认证失效
adminApi.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response) {
      // 处理特定错误状态码
      switch (error.response.status) {
        case 401:
          // 未认证，清除token并跳转到登录页
          localStorage.removeItem('adminToken')
          localStorage.removeItem('adminInfo')
          window.location.href = '/admin/login'
          break
        case 403:
          alert('没有权限执行此操作')
          break
        case 500:
          console.error('服务器内部错误')
          break
        default:
          console.error(`请求失败: ${error.response.status}`)
      }
      return Promise.reject(error.response.data || error.response)
    } else if (error.request) {
      // 请求已发出但没有收到响应
      console.error('网络错误，请检查您的连接')
      return Promise.reject('网络错误，请检查您的连接')
    } else {
      // 请求配置出错
      console.error('请求配置错误:', error.message)
      return Promise.reject(error)
    }
  }
)

// 管理员认证相关API
export const adminAuthApi = {
  // 管理员登录
  login(credentials) {
    return adminApi.post('/auth/login', credentials)
  },
  
  // 管理员注册
  register(adminData) {
    return adminApi.post('/auth/register', adminData)
  },
  
  // 获取当前管理员信息
  getProfile() {
    return adminApi.get('/auth/profile')
  },
  
  // 刷新token
  refreshToken() {
    return adminApi.post('/auth/refresh')
  },
  
  // 修改密码
  changePassword(passwordData) {
    return adminApi.put('/auth/change-password', passwordData)
  }
}

// 民俗文化管理API
export const folkCultureAdminApi = {
  // 批量上传民俗文化数据
  batchUpload(data) {
    return adminApi.post('/folk-culture/batch-upload', data)
  },
  
  // 获取民俗文化列表（带分页和筛选）
  getFolkCultureList(params) {
    return adminApi.get('/folk-culture', { params })
  },
  
  // 获取单个民俗文化详情
  getFolkCultureDetail(id) {
    return adminApi.get(`/folk-culture/${id}`)
  },
  
  // 创建民俗文化
  createFolkCulture(data) {
    return adminApi.post('/folk-culture', data)
  },
  
  // 更新民俗文化
  updateFolkCulture(id, data) {
    return adminApi.put(`/folk-culture/${id}`, data)
  },
  
  // 删除民俗文化
  deleteFolkCulture(id) {
    return adminApi.delete(`/folk-culture/${id}`)
  },
  
  // 批量删除民俗文化
  batchDeleteFolkCulture(ids) {
    return adminApi.delete('/folk-culture/batch', { data: { ids } })
  }
}

// 仪表盘统计API
export const dashboardApi = {
  // 获取仪表盘统计数据
  getDashboardStats() {
    return adminApi.get('/dashboard/stats')
  },
  
  // 获取最近添加的数据
  getRecentData(limit = 10) {
    return adminApi.get('/dashboard/recent', { params: { limit } })
  },
  
  // 获取数据分布统计
  getDataDistribution(type) {
    return adminApi.get(`/dashboard/distribution/${type}`)
  }
}

export default adminApi