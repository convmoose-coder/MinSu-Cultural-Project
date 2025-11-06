import axios from 'axios'

// 创建前台API实例
const frontendApi = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
frontendApi.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
frontendApi.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    if (error.response) {
      // 处理特定错误状态码
      switch (error.response.status) {
        case 404:
          console.error('请求的资源不存在')
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

// 民俗文化展示API
export const folkCultureApi = {
  // 获取民俗文化列表
  getFolkCultureList(params = {}) {
    return frontendApi.get('/folk-culture', { params })
  },
  
  // 获取民俗文化详情
  getFolkCultureDetail(id) {
    return frontendApi.get(`/folk-culture/${id}`)
  },
  
  // 获取热门民俗文化
  getPopularFolkCulture(limit = 5) {
    return frontendApi.get('/folk-culture/popular', { params: { limit } })
  },
  
  // 获取最新添加的民俗文化
  getLatestFolkCulture(limit = 5) {
    return frontendApi.get('/folk-culture/latest', { params: { limit } })
  },
  
  // 根据类别获取民俗文化
  getFolkCultureByCategory(category, params = {}) {
    return frontendApi.get(`/folk-culture/category/${category}`, { params })
  },
  
  // 根据地区获取民俗文化
  getFolkCultureByRegion(region, params = {}) {
    return frontendApi.get(`/folk-culture/region/${region}`, { params })
  }
}

// 地区文化API
export const regionApi = {
  // 获取所有地区列表
  getRegions() {
    return frontendApi.get('/regions')
  },
  
  // 获取地区详情
  getRegionDetail(id) {
    return frontendApi.get(`/regions/${id}`)
  },
  
  // 获取地区文化特色
  getRegionFeatures(regionId) {
    return frontendApi.get(`/regions/${regionId}/features`)
  }
}

// 搜索API
export const searchApi = {
  // 搜索民俗文化
  searchFolkCulture(query, params = {}) {
    return frontendApi.get('/search/folk-culture', { 
      params: { query, ...params } 
    })
  },
  
  // 全局搜索
  globalSearch(query, params = {}) {
    return frontendApi.get('/search', { 
      params: { query, ...params } 
    })
  }
}

// 系统信息API
export const systemApi = {
  // 获取系统信息
  getSystemInfo() {
    return frontendApi.get('/system/info')
  },
  
  // 获取网站配置
  getSiteConfig() {
    return frontendApi.get('/system/config')
  }
}

export default frontendApi