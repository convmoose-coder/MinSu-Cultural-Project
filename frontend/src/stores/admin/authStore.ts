import { defineStore } from 'pinia';
import authService from '@/services/admin/authService';

interface User {
  id: string;
  username: string;
  role: string;
  email?: string;
  createdAt?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: null,
    token: localStorage.getItem('admin-token'),
    isAuthenticated: !!localStorage.getItem('admin-token'),
    isLoading: false,
    error: null
  }),

  getters: {
    // 获取当前用户信息
    currentUser: (state) => state.user,
    // 检查是否已登录
    loggedIn: (state) => state.isAuthenticated,
    // 检查是否为管理员角色
    isAdmin: (state) => state.user?.role === 'admin',
    // 获取登录错误信息
    loginError: (state) => state.error
  },

  actions: {
    // 登录
    async login(username: string, password: string) {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await authService.login({ username, password });
        
        // 保存token
        this.token = response.token;
        localStorage.setItem('admin-token', response.token);
        
        // 设置用户信息
        this.user = response.user;
        this.isAuthenticated = true;
        
        return response;
      } catch (error) {
        this.error = error instanceof Error ? error.message : '登录失败';
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // 注册
    async register(userData: {
      username: string;
      email: string;
      password: string;
      confirmPassword: string;
    }) {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await authService.register(userData);
        return response;
      } catch (error) {
        this.error = error instanceof Error ? error.message : '注册失败';
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    // 退出登录
    async logout() {
      try {
        await authService.logout();
      } finally {
        // 清除本地状态
        this.user = null;
        this.token = null;
        this.isAuthenticated = false;
        localStorage.removeItem('admin-token');
      }
    },

    // 获取当前用户信息
    async fetchCurrentUser() {
      if (!this.token) return;
      
      this.isLoading = true;
      
      try {
        const userData = await authService.getCurrentUser();
        this.user = userData as User;
        this.isAuthenticated = true;
      } catch (error) {
        // 如果获取用户信息失败，清除认证状态
        this.logout();
        console.error('Failed to fetch user:', error);
      } finally {
        this.isLoading = false;
      }
    },

    // 清除错误信息
    clearError() {
      this.error = null;
    }
  }
});

// 如果项目中没有安装pinia，这里提供一个简单的替代实现
// 这部分代码只有在pinia不可用时才会被使用
let fallbackAuthStore: {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
} = {
  user: null,
  token: localStorage.getItem('admin-token'),
  isAuthenticated: !!localStorage.getItem('admin-token')
};

export const fallbackAuth = {
  getState: () => fallbackAuthStore,
  login: async (username: string, password: string) => {
    const response = await authService.login({ username, password });
    fallbackAuthStore = {
      user: response.user,
      token: response.token,
      isAuthenticated: true
    };
    localStorage.setItem('admin-token', response.token);
    return response;
  },
  logout: async () => {
    await authService.logout();
    fallbackAuthStore = {
      user: null,
      token: null,
      isAuthenticated: false
    };
  },
  checkAuth: () => {
    return fallbackAuthStore.isAuthenticated;
  }
};