import axios from 'axios'

// 创建axios实例
const apiClient = axios.create({
  baseURL: '/api', // 保持与vite.config.js中的代理配置一致
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    // 可以在这里添加token等认证信息
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API请求错误:', error)
    return Promise.reject(error)
  }
)

// API接口
export const folkCultureApi = {
  // 获取所有民俗文化
  getAll: () => apiClient.get('/folkcultures'),
  
  // 根据ID获取民俗文化详情
  getById: (id) => apiClient.get(`/folkcultures/${id}`),
  
  // 创建新的民俗文化记录
  create: (data) => apiClient.post('/folkcultures', data),
  
  // 获取所有地区
  getRegions: () => apiClient.get('/regions'),
  
  // 获取所有分类
  getCategories: () => apiClient.get('/categories')
}

// 导出apiClient实例以供其他模块使用
export default apiClient