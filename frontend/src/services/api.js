import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: '',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器 - 添加认证token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin-token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器 - 处理常见错误
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    if (error.response) {
      // 401错误处理 - 未授权
      if (error.response.status === 401) {
      localStorage.removeItem('adminToken');
      localStorage.removeItem('adminUser');
      window.location.href = '/admin/login';
    }
    }
    return Promise.reject(error);
  }
);

// 认证相关API
export const auth = {
  // 登录
  login(username, password) {
    return api.post('/api/admin/login', { username, password });
  },
  
  // 退出登录
  logout() {
    return api.post('/api/admin/logout');
  },
  
  // 获取用户信息
  getProfile() {
    return api.get('/admin/profile');
  }
};

// 仪表盘相关API
export const dashboard = {
  // 获取仪表盘数据
  getDashboardData() {
    return api.get('/admin/dashboard');
  }
};

// 批量上传相关API
export const batchUpload = {
  // 上传文件
  uploadFile(formData) {
    return api.post('/admin/batch-upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          // 可以在这里通过事件总线或其他方式传递进度
          console.log('上传进度:', percentCompleted);
        }
      }
    });
  },
  
  // 获取上传模板
  getTemplate(dataType) {
    return api.get(`/admin/templates/${dataType}`);
  }
};

// 民俗文化相关API
export const folkCulture = {
  // 获取文化列表
  getCultures(params) {
    return api.get('/folk-culture', { params });
  },
  
  // 获取文化详情
  getCultureDetail(id) {
    return api.get(`/folk-culture/${id}`);
  },
  
  // 创建文化信息
  createCulture(data) {
    return api.post('/folk-culture', data);
  },
  
  // 更新文化信息
  updateCulture(id, data) {
    return api.put(`/folk-culture/${id}`, data);
  },
  
  // 删除文化信息
  deleteCulture(id) {
    return api.delete(`/folk-culture/${id}`);
  }
};

export default api;