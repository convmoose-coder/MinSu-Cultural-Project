<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { folkCultureApi } from '@/api/culture'
import FolkCultureCard from '../components/FolkCultureCard.vue'
import { createLogger } from '../utils/logger'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { useDataFetching } from '../composables/useDataFetching'

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
const logger = createLogger('RegionsView');

const route = useRoute()
const regions = ref([])
const allCultures = ref([])
const selectedRegion = ref('')
const error = ref('')

// 使用自定义Hook处理加载状态
const { data: regionsData, loading: loadingRegions, error: regionsError, refetch: refetchRegions } = useDataFetching(
  folkCultureApi.getRegions
)

const { data: culturesData, loading: loadingCultures } = useDataFetching(
  () => folkCultureApi.getCultures(),
  { autoFetch: false }
)

// 计算属性：过滤当前地区的文化
const cultures = computed(() => {
  if (!selectedRegion.value) return []
  return allCultures.value.filter(culture => culture.region === selectedRegion.value)
})

// 总加载状态
const loading = computed(() => loadingRegions.value || loadingCultures.value)

// 获取数据
const fetchData = async () => {
  logger.info('开始获取地区和文化数据');
  const startTime = performance.now();
  
  try {
    error.value = ''
    logger.debug('重置错误状态');
    
    // 获取地区列表
    logger.info('开始获取地区列表');
    await refetchRegions()
    if (regionsData.value) {
      regions.value = regionsData.value.data
      logger.info('成功获取地区列表', { count: regions.value.length });
    }
    
    // 获取所有文化数据
    logger.info('开始获取文化数据');
    await culturesData.refetch()
    if (culturesData.data) {
      allCultures.value = culturesData.data.data
      logger.info('成功获取文化数据', { count: allCultures.value.length });
    }
    
    // 检查URL中是否有地区参数
    const urlRegion = route.query.region
    logger.debug('检查URL地区参数', { urlRegion });
    
    if (urlRegion && regions.value.includes(urlRegion)) {
      selectedRegion.value = urlRegion
      logger.info('设置选中地区为URL参数', { selectedRegion: selectedRegion.value });
    } else if (regions.value.length > 0) {
      // 默认选择第一个地区
      selectedRegion.value = regions.value[0]
      logger.info('设置默认选中地区', { selectedRegion: selectedRegion.value });
    }
    
    const endTime = performance.now();
    logger.info('数据获取完成', { responseTime: `${(endTime - startTime).toFixed(2)}ms` });
  } catch (err) {
    const endTime = performance.now();
    logger.error('获取数据失败', { 
      error: err, 
      responseTime: `${(endTime - startTime).toFixed(2)}ms` 
    });
    error.value = '获取数据失败，请稍后重试'
  }
}

// 处理地区变更
const handleRegionChange = (region) => {
  logger.debug('切换地区', { newRegion: region });
  selectedRegion.value = region
}

// 重试操作
const handleRetry = () => {
  logger.info('用户点击重试按钮');
  fetchData()
}

onMounted(() => {
  logger.info('RegionsView组件已挂载，开始初始化数据');
  fetchData()
})
</script>

<template>
  <div class="regions-view">
    <h2>地区分类</h2>
    
    <LoadingSpinner v-if="loading" :full-screen="false" message="正在加载地区数据..." />
    
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
      <button class="retry-btn" @click="handleRetry">重试</button>
    </div>
    
    <div v-else class="regions-container">
      <div class="region-list">
        <h3>选择地区</h3>
        <ul>
          <li 
            v-for="region in regions" 
            :key="region"
            :class="{ active: selectedRegion === region }"
            @click="handleRegionChange(region)"
          >
            {{ region }}
          </li>
        </ul>
      </div>
      
      <div class="region-content">
        <h3>{{ selectedRegion }} 的民俗文化</h3>
        
        <div v-if="cultures.length === 0" class="no-cultures">
          该地区暂无民俗文化记录
        </div>
        
        <div v-else class="culture-grid">
          <FolkCultureCard 
            v-for="culture in cultures" 
            :key="culture.id"
            :culture="culture"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.regions-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 0;
}

.regions-view h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #333;
  text-align: center;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
  margin-bottom: 2rem;
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

.regions-container {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.region-list {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.region-list h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #333;
  font-size: 1.2rem;
}

.region-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.region-list li {
  padding: 0.75rem 1rem;
  margin-bottom: 0.25rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  color: #555;
  border: 1px solid transparent;
}

.region-list li:hover {
  background-color: #f0f0f0;
  color: #8B4513;
  border-color: #8B4513;
}

.region-list li.active {
  background-color: #8B4513;
  color: white;
}

.region-content {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.region-content h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #333;
  font-size: 1.4rem;
}

.no-cultures {
  text-align: center;
  padding: 3rem;
  color: #666;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.culture-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
}

/* 响应式调整 */
@media (max-width: 992px) {
  .regions-container {
    grid-template-columns: 200px 1fr;
  }
}

@media (max-width: 768px) {
  .regions-container {
    grid-template-columns: 1fr;
  }
  
  .culture-grid {
    grid-template-columns: 1fr;
  }
}
</style>