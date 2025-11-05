import axios from 'axios';
import { createLogger } from '../utils/logger';

// 创建日志实例
const logger = createLogger('FolkCultureService');

// 辅助函数：清理日志中的敏感数据
function sanitizeData(data) {
  if (!data || typeof data !== 'object') return data;
  
  // 深拷贝对象以避免修改原始数据
  const sanitized = { ...data };
  
  // 移除可能的敏感字段（根据业务需求调整）
  const sensitiveFields = ['password', 'token', 'secret', 'apiKey'];
  sensitiveFields.forEach(field => {
    if (field in sanitized) {
      sanitized[field] = '******';
    }
  });
  
  return sanitized;
}

const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

export class FolkCultureService {
  static async getCultures() {
    const endpoint = '/folkcultures';
    logger.info('开始获取所有文化数据', { endpoint });
    const startTime = performance.now();
    
    try {
      logger.debug('发送GET请求', { endpoint });
      const response = await apiClient.get(endpoint);
      const endTime = performance.now();
      logger.info('成功获取文化数据', {
        endpoint,
        status: response.status,
        dataLength: Array.isArray(response.data) ? response.data.length : 'N/A',
        responseTime: `${(endTime - startTime).toFixed(2)}ms`
      });
      return { data: response.data };
    } catch (error) {
      const endTime = performance.now();
      logger.error('获取文化数据失败', {
        endpoint,
        error: error.message,
        status: error.response?.status,
        responseTime: `${(endTime - startTime).toFixed(2)}ms`
      });
      throw error;
    }
  }

  static async getCultureById(id) {
    const endpoint = `/folkcultures/${id}`;
    logger.info('开始获取单个文化数据', { endpoint, id });
    const startTime = performance.now();
    
    try {
      logger.debug('发送GET请求', { endpoint, id });
      const response = await apiClient.get(endpoint);
      const endTime = performance.now();
      logger.info('成功获取单个文化数据', {
        endpoint,
        id,
        status: response.status,
        responseTime: `${(endTime - startTime).toFixed(2)}ms`
      });
      return { data: response.data };
    } catch (error) {
      const endTime = performance.now();
      logger.error('获取单个文化数据失败', {
        endpoint,
        id,
        error: error.message,
        status: error.response?.status,
        responseTime: `${(endTime - startTime).toFixed(2)}ms`
      });
      throw error;
    }
  }

  static async createCulture(data) {
    const endpoint = '/folkcultures';
    logger.info('开始创建文化数据', { endpoint });
    const startTime = performance.now();
    
    try {
      logger.debug('发送POST请求', { endpoint, data: sanitizeData(data) });
      const response = await apiClient.post(endpoint, data);
      const endTime = performance.now();
      logger.info('成功创建文化数据', {
        endpoint,
        id: response.data?.id,
        status: response.status,
        responseTime: `${(endTime - startTime).toFixed(2)}ms`
      });
      return { data: response.data };
    } catch (error) {
      const endTime = performance.now();
      logger.error('创建文化数据失败', {
        endpoint,
        error: error.message,
        status: error.response?.status,
        responseTime: `${(endTime - startTime).toFixed(2)}ms`
      });
      throw error;
    }
  }

  static async getRegions() {
    const endpoint = '/regions';
    logger.info('开始获取地区列表', { endpoint });
    const startTime = performance.now();
    
    try {
      logger.debug('发送GET请求', { endpoint });
      const response = await apiClient.get(endpoint);
      const endTime = performance.now();
      logger.info('成功获取地区列表', {
        endpoint,
        count: Array.isArray(response.data) ? response.data.length : 'N/A',
        status: response.status,
        responseTime: `${(endTime - startTime).toFixed(2)}ms`
      });
      return { data: response.data };
    } catch (error) {
      const endTime = performance.now();
      logger.error('获取地区列表失败', {
        endpoint,
        error: error.message,
        status: error.response?.status,
        responseTime: `${(endTime - startTime).toFixed(2)}ms`
      });
      throw error;
    }
  }

  static async getCategories() {
    const endpoint = '/categories';
    logger.info('开始获取分类列表', { endpoint });
    const startTime = performance.now();
    
    try {
      logger.debug('发送GET请求', { endpoint });
      const response = await apiClient.get(endpoint);
      const endTime = performance.now();
      logger.info('成功获取分类列表', {
        endpoint,
        count: Array.isArray(response.data) ? response.data.length : 'N/A',
        status: response.status,
        responseTime: `${(endTime - startTime).toFixed(2)}ms`
      });
      return { data: response.data };
    } catch (error) {
      const endTime = performance.now();
      logger.error('获取分类列表失败', {
        endpoint,
        error: error.message,
        status: error.response?.status,
        responseTime: `${(endTime - startTime).toFixed(2)}ms`
      });
      throw error;
    }
  }

  // 添加缺失的getFolkCulturesByRegion方法
  static async getFolkCulturesByRegion(region) {
    const endpoint = `/folkcultures/region/${region || 'all'}`;
    logger.info('开始获取特定地区的文化数据', { endpoint, region });
    const startTime = performance.now();
    
    try {
      logger.debug('发送GET请求', { endpoint, region });
      const response = await apiClient.get(endpoint);
      const endTime = performance.now();
      logger.info('成功获取特定地区的文化数据', {
        endpoint,
        region,
        count: Array.isArray(response.data) ? response.data.length : 'N/A',
        status: response.status,
        responseTime: `${(endTime - startTime).toFixed(2)}ms`
      });
      return response.data;
    } catch (error) {
      const endTime = performance.now();
      logger.error('获取特定地区的文化数据失败', {
        endpoint,
        region,
        error: error.message,
        status: error.response?.status,
        responseTime: `${(endTime - startTime).toFixed(2)}ms`
      });
      throw error;
    }
  }
}

export default FolkCultureService;