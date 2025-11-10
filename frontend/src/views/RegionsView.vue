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
  <section class="regions-view">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">地区文化</h1>
      <p class="page-subtitle">探索不同地区的独特民俗文化特色</p>
    </div>
    
    <!-- 加载状态 -->
    <LoadingSpinner v-if="loading" :full-screen="false" message="正在加载地区数据..." />
    
    <!-- 错误状态 -->
    <div v-else-if="error" class="error-message">
      <div class="error-icon">⚠️</div>
      <p class="error-text">{{ error }}</p>
      <button class="btn-primary" @click="handleRetry">
        重试加载
      </button>
    </div>
    
    <!-- 主要内容 -->
    <div v-else class="regions-container">
      <!-- 地区选择侧边栏 -->
      <aside class="region-sidebar">
        <div class="region-sidebar-header">
          <h3 class="region-sidebar-title">选择地区</h3>
          <div class="region-count">{{ regions.length }}个地区</div>
        </div>
        
        <nav class="region-nav">
          <ul class="region-list">
            <li 
              v-for="region in regions" 
              :key="region"
              class="region-item"
              :class="{ active: selectedRegion === region }"
              @click="handleRegionChange(region)"
            >
              <span class="region-name">{{ region }}</span>
              <span class="region-badge">{{ cultures.length }}</span>
            </li>
          </ul>
        </nav>
      </aside>
      
      <!-- 文化内容区域 -->
      <main class="region-content">
        <div class="region-content-header">
          <h2 class="region-content-title">{{ selectedRegion }} 的民俗文化</h2>
          <div class="content-info">
            共 {{ cultures.length }} 项文化记录
          </div>
        </div>
        
        <!-- 无数据状态 -->
        <div v-if="cultures.length === 0" class="no-cultures">
          <div class="no-data-icon">📚</div>
          <h3>暂无文化记录</h3>
          <p>该地区目前还没有相关的民俗文化记录</p>
        </div>
        
        <!-- 文化卡片网格 -->
        <div v-else class="culture-grid">
          <FolkCultureCard 
            v-for="culture in cultures" 
            :key="culture.id"
            :culture="culture"
            class="culture-card"
          />
        </div>
      </main>
    </div>
  </section>
</template>

<style lang="scss" scoped>
.regions-view {
  max-width: var(--container-width);
  margin: 0 auto;
  padding: var(--spacing-section) var(--spacing-padding);
}

// 页面头部
.page-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.6s ease-out forwards;
  animation-delay: 0.1s;
}

.page-title {
  font-size: var(--font-size-2xl);
  color: var(--color-primary-dark);
  margin-bottom: var(--spacing-sm);
  font-weight: 700;
}

.page-subtitle {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  max-width: 700px;
  margin: 0 auto;
}

// 错误信息
.error-message {
  background-color: var(--color-error-bg);
  color: var(--color-error);
  padding: var(--spacing-xl);
  border-radius: var(--border-radius-lg);
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  align-items: center;
  margin-bottom: var(--spacing-xl);
  border: 1px solid var(--color-error-border);
  box-shadow: var(--shadow-sm);
}

.error-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-sm);
}

.error-text {
  font-size: var(--font-size-base);
  font-weight: 500;
}

// 容器布局
.regions-container {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: var(--spacing-xl);
  animation: fadeIn 0.8s ease-out;
}

// 侧边栏样式
.region-sidebar {
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
  height: fit-content;
  position: sticky;
  top: var(--spacing-lg);
}

.region-sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 2px solid var(--color-border);
}

.region-sidebar-title {
  font-size: var(--font-size-lg);
  color: var(--color-text-primary);
  margin: 0;
  font-weight: 600;
}

.region-count {
  background-color: var(--color-primary-light);
  color: var(--color-primary);
  font-size: var(--font-size-sm);
  padding: 0.25rem 0.5rem;
  border-radius: var(--border-radius-full);
  font-weight: 600;
}

.region-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.region-item {
  padding: var(--spacing-md) var(--spacing-sm);
  margin-bottom: var(--spacing-xs);
  border-radius: var(--border-radius-md);
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--color-text-secondary);
  border: 1px solid transparent;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 500;
  position: relative;
  overflow: hidden;
}

.region-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background-color: transparent;
  transition: background-color 0.3s ease;
}

.region-item:hover {
  background-color: var(--color-hover);
  color: var(--color-primary);
  transform: translateX(4px);
  box-shadow: var(--shadow-xs);
}

.region-item:hover::before {
  background-color: var(--color-primary);
}

.region-item.active {
  background-color: var(--color-primary);
  color: white;
  box-shadow: var(--shadow-md);
}

.region-item.active::before {
  background-color: var(--color-primary-dark);
}

.region-badge {
  background-color: rgba(0, 0, 0, 0.1);
  color: inherit;
  font-size: var(--font-size-xs);
  padding: 0.2rem 0.4rem;
  border-radius: var(--border-radius-full);
  font-weight: 600;
  min-width: 24px;
  text-align: center;
}

// 内容区域样式
.region-content {
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
}

.region-content-header {
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--color-border);
}

.region-content-title {
  font-size: var(--font-size-xl);
  color: var(--color-primary-dark);
  margin: 0 0 var(--spacing-xs) 0;
  font-weight: 700;
}

.content-info {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: 500;
}

// 无数据状态
.no-cultures {
  text-align: center;
  padding: var(--spacing-3xl) var(--spacing-xl);
  background-color: var(--color-background);
  border-radius: var(--border-radius-lg);
  border: 2px dashed var(--color-border);
}

.no-data-icon {
  font-size: 4rem;
  margin-bottom: var(--spacing-md);
  opacity: 0.6;
}

.no-cultures h3 {
  font-size: var(--font-size-lg);
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-sm);
  font-weight: 600;
}

.no-cultures p {
  font-size: var(--font-size-base);
  color: var(--color-text-muted);
  max-width: 400px;
  margin: 0 auto;
}

// 文化卡片网格
.culture-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-lg);
}

.culture-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.culture-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

// 动画效果
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

// 响应式设计
@media (max-width: 1024px) {
  .regions-container {
    grid-template-columns: 250px 1fr;
    gap: var(--spacing-lg);
  }
  
  .culture-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }
}

@media (max-width: 768px) {
  .regions-container {
    grid-template-columns: 1fr;
  }
  
  .region-sidebar {
    position: static;
    margin-bottom: var(--spacing-lg);
  }
  
  .region-list {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-xs);
  }
  
  .region-item {
    flex: 1;
    min-width: calc(50% - 8px);
    justify-content: center;
    text-align: center;
    padding: var(--spacing-sm);
    margin-bottom: 0;
  }
  
  .region-item::before {
    width: 100%;
    height: 4px;
    top: 0;
    left: 0;
  }
  
  .region-item:hover {
    transform: translateY(-2px);
  }
  
  .culture-grid {
    grid-template-columns: 1fr;
  }
  
  .page-title {
    font-size: var(--font-size-xl);
  }
  
  .region-content-title {
    font-size: var(--font-size-lg);
  }
}

@media (max-width: 480px) {
  .region-item {
    min-width: 100%;
  }
  
  .regions-view {
    padding: var(--spacing-lg) var(--spacing-sm);
  }
  
  .region-sidebar,
  .region-content {
    padding: var(--spacing-md);
  }
}
</style>