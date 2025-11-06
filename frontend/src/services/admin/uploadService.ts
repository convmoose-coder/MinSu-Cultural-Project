import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: '/api/admin',
  timeout: 30000, // 上传文件时设置较长的超时时间
  headers: {
    'Content-Type': 'multipart/form-data'
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
    if (error.response?.status === 401) {
      localStorage.removeItem('admin-token');
      window.location.href = '/admin/login';
    }
    return Promise.reject(error.response?.data || error.message);
  }
);

interface UploadResponse {
  success: boolean;
  message: string;
  data?: {
    total: number;
    success: number;
    failed: number;
    errors?: Array<{
      row: number;
      error: string;
    }>;
  };
}

interface FileValidationResult {
  valid: boolean;
  error?: string;
}

// 数据上传相关API
export const uploadService = {
  // 批量上传数据
  batchUpload: async (file: File, dataType: string): Promise<UploadResponse> => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('type', dataType);
      
      // 模拟API调用
      // const response = await api.post<UploadResponse>('/upload/batch', formData);
      
      // 模拟上传延迟和响应
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            success: true,
            message: '上传成功',
            data: {
              total: 100,
              success: 95,
              failed: 5,
              errors: [
                { row: 10, error: '数据格式错误' },
                { row: 25, error: '必填字段为空' }
              ]
            }
          });
        }, 2000);
      });
    } catch (error) {
      console.error('Batch upload error:', error);
      throw error;
    }
  },

  // 验证上传文件
  validateFile: (file: File): FileValidationResult => {
    // 检查文件大小（最大10MB）
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      return {
        valid: false,
        error: `文件大小不能超过${maxSize / 1024 / 1024}MB`
      };
    }
    
    // 检查文件类型
    const allowedTypes = ['text/csv', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
    const allowedExtensions = ['.csv', '.xls', '.xlsx'];
    
    const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
    
    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
      return {
        valid: false,
        error: '只支持CSV、XLS、XLSX格式的文件'
      };
    }
    
    return { valid: true };
  },

  // 获取上传历史
  getUploadHistory: async () => {
    try {
      // 模拟API调用
      // const response = await api.get('/upload/history');
      
      // 模拟响应数据
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            success: true,
            data: [
              {
                id: '1',
                filename: '民族文化数据_20230501.csv',
                type: 'culture',
                size: 1024000,
                uploadedAt: '2023-05-01T10:30:00Z',
                status: 'success',
                total: 150,
                success: 145,
                failed: 5
              },
              {
                id: '2',
                filename: '民族节日数据.xlsx',
                type: 'festival',
                size: 2048000,
                uploadedAt: '2023-04-28T14:20:00Z',
                status: 'success',
                total: 80,
                success: 80,
                failed: 0
              }
            ]
          });
        }, 500);
      });
    } catch (error) {
      console.error('Get upload history error:', error);
      throw error;
    }
  },

  // 下载上传模板
  downloadTemplate: async (type: string) => {
    try {
      // 模拟下载功能
      // 实际项目中应该调用真实的后端API获取模板文件
      console.log(`Download template for type: ${type}`);
      
      // 这里可以添加实际的下载逻辑
      // window.location.href = `/api/admin/upload/template?type=${type}`;
      
      alert('模板下载功能开发中');
    } catch (error) {
      console.error('Download template error:', error);
      throw error;
    }
  }
};

export default uploadService;