import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: '/api/admin',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器 - 添加token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin-token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    // 处理token过期等错误
    if (error.response?.status === 401) {
      // 清除本地存储的token
      localStorage.removeItem('admin-token');
      // 可以在这里添加重定向到登录页的逻辑
      window.location.href = '/admin/login';
    }
    return Promise.reject(error.response?.data || error.message);
  }
);

interface LoginParams {
  username: string;
  password: string;
  remember?: boolean;
}

interface LoginResponse {
  token: string;
  user: {
    id: string;
    username: string;
    role: string;
  };
}

interface RegisterParams {
  username: string;
  password: string;
  confirmPassword: string;
  email: string;
}

interface RegisterResponse {
  id: string;
  username: string;
  email: string;
}

// 认证相关API
export const authService = {
  // 登录
  login: async (params: LoginParams): Promise<LoginResponse> => {
    try {
      // 调用真实的后端API
      const response = await api.post<LoginResponse>('/auth/login', params);
      return response;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  // 注册
  register: async (params: RegisterParams): Promise<RegisterResponse> => {
    try {
      // 模拟API调用
      // const response = await api.post<RegisterResponse>('/register', params);
      
      // 模拟响应数据
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            id: 'new-user-' + Date.now(),
            username: params.username,
            email: params.email
          });
        }, 500);
      });
    } catch (error) {
      console.error('Register error:', error);
      throw error;
    }
  },

  // 退出登录
  logout: async (): Promise<void> => {
    try {
      // 模拟API调用
      // await api.post('/logout');
      
      // 清除本地存储的token
      localStorage.removeItem('admin-token');
    } catch (error) {
      console.error('Logout error:', error);
      // 即使API调用失败，也清除本地token
      localStorage.removeItem('admin-token');
    }
  },

  // 获取当前用户信息
  getCurrentUser: async () => {
    try {
      // 模拟API调用
      // const response = await api.get('/me');
      
      // 模拟响应数据
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            id: '1',
            username: 'admin',
            role: 'admin',
            email: 'admin@example.com',
            createdAt: '2023-01-01T00:00:00Z'
          });
        }, 300);
      });
    } catch (error) {
      console.error('Get current user error:', error);
      throw error;
    }
  },

  // 刷新token
  refreshToken: async (): Promise<{ token: string }> => {
    try {
      // 模拟API调用
      // const response = await api.post('/refresh');
      
      // 模拟响应数据
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            token: 'mock-refreshed-token-' + Date.now()
          });
        }, 300);
      });
    } catch (error) {
      console.error('Refresh token error:', error);
      throw error;
    }
  },

  // 检查token是否有效
  checkToken: (): boolean => {
    const token = localStorage.getItem('admin-token');
    return !!token;
  }
};

export default authService;