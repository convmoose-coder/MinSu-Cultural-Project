<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { folkCultureApi } from '@/api/frontendApi'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { createLogger } from '../utils/logger'

// 内联类型定义
interface FolkCulture {
  id: number;
  title: string;
  description: string;
  category: string;
  region: string;
  created_at?: string;
}

// 创建日志实例
const logger = createLogger('CultureDetailView');

const route = useRoute()
const culture = ref<FolkCulture | null>(null)
const error = ref<string | null>(null)
const loading = ref(false)

const handleRetry = () => {
  fetchCultureDetail()
}

// 监听路由变化，当ID改变时重新获取数据
watch(
  () => route.params.id,
  (newId, oldId) => {
    if (newId !== oldId) {
      logger.info('路由参数ID发生变化，重新获取文化详情', { oldId, newId });
      fetchCultureDetail()
    }
  }
)

onMounted(() => {
  logger.info('组件已挂载，开始获取文化详情');
  fetchCultureDetail()
})

const fetchCultureDetail = async () => {
  const cultureId = route.params.id as string
  logger.debug('开始获取文化详情', { cultureId });
  
  if (!cultureId) {
    logger.warn('未提供文化ID，无法获取详情');
    return
  }
  
  loading.value = true
  error.value = null
  const startTime = performance.now();
  
  try {
    logger.info('调用API获取文化详情', { cultureId });
    const response = await folkCultureApi.getFolkCultureDetail(cultureId)
    const endTime = performance.now();
    logger.info('成功获取文化详情', { 
      cultureId, 
      title: response?.data?.title, 
      responseTime: `${(endTime - startTime).toFixed(2)}ms` 
    });
    culture.value = response.data
  } catch (err) {
    const endTime = performance.now();
    logger.error('获取文化详情失败', { 
      cultureId, 
      error: err, 
      responseTime: `${(endTime - startTime).toFixed(2)}ms` 
    });
    error.value = '获取详情失败，请稍后重试'
  } finally {
    loading.value = false
    logger.debug('文化详情获取流程结束', { loading: false });
  }
}
</script>

<template>
  <div class="culture-detail">
    <LoadingSpinner v-if="loading" :full-screen="false" message="正在加载详情..." />
    
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
      <div class="error-actions">
        <button class="retry-btn" @click="handleRetry">重试</button>
        <router-link to="/culture" class="btn">返回列表</router-link>
      </div>
    </div>
    
    <div v-else-if="culture" class="detail-content">
      <div class="detail-header">
        <h1>{{ culture.title || '未知文化' }}</h1>
        <div class="meta-info">
          <span class="category-badge">{{ culture.category || '未分类' }}</span>
          <span class="region-badge">{{ culture.region || '未知地区' }}</span>
          <span class="date">{{ culture.created_at ? new Date(culture.created_at).toLocaleDateString('zh-CN') : '未知日期' }}</span>
        </div>
      </div>
      
      <div class="detail-body">
        <div class="description">
          <p>{{ culture.description }}</p>
        </div>
        
        <div class="related-content">
          <h3>相关推荐</h3>
          <!-- 这里可以添加相关内容推荐 -->
        </div>
      </div>
      
      <div class="action-buttons">
        <router-link to="/culture" class="btn">返回列表</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.culture-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 0;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.retry-btn {
  background-color: #8B4513;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.retry-btn:hover {
  background-color: #6d3510;
}

.btn {
  background-color: #6c757d;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  transition: background-color 0.3s;
  display: inline-block;
}

.btn:hover {
  background-color: #5a6268;
}

.detail-content {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.detail-header {
  background-color: #8B4513;
  color: white;
  padding: 2rem;
}

.detail-header h1 {
  font-size: 2.2rem;
  margin-bottom: 1rem;
}

.meta-info {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  font-size: 0.95rem;
}

.category-badge, .region-badge {
  padding: 0.35rem 0.85rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.category-badge {
  background-color: rgba(255, 255, 255, 0.3);
  color: white;
}

.region-badge {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.detail-body {
  padding: 2rem;
}

.description {
  line-height: 1.8;
  color: #444;
  margin-bottom: 2rem;
}

.related-content {
  margin-top: 2rem;
}

.related-content h3 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #333;
  border-bottom: 2px solid #8B4513;
  padding-bottom: 0.5rem;
}

.action-buttons {
  padding: 1.5rem 2rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .detail-header h1 {
    font-size: 1.8rem;
  }
  
  .meta-info {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .error-actions {
    flex-direction: column;
  }
  
  .error-actions .btn, .error-actions .retry-btn {
    width: 100%;
  }
}


.meta-info {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  font-size: 0.9rem;
}

.meta-info span {
  background-color: rgba(255, 255, 255, 0.2);
  padding: 0.3rem 0.8rem;
  border-radius: 15px;
}

.detail-body {
  padding: 2rem;
}

.description {
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: 3rem;
}

.related-content {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.related-content h3 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #8B4513;
}

.action-buttons {
  margin-top: 2rem;
  text-align: center;
}

@media (max-width: 768px) {
  .detail-header h1 {
    font-size: 1.8rem;
  }
  
  .detail-header, .detail-body {
    padding: 1.5rem;
  }
  
  .meta-info {
    flex-direction: column;
    gap: 0.5rem;
  }
}
</style>