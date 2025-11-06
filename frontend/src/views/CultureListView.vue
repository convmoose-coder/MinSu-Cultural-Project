<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import FolkCultureCard from '../components/FolkCultureCard.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import folkCultureStore from '../stores/folkCultureStore'
import { useDataFetching } from '../composables/useDataFetching'
import { createLogger } from '../utils/logger'

// 获取store中的状态
const state = folkCultureStore.state

// 创建日志实例
const logger = createLogger('CultureListView')

// 筛选条件
const searchQuery = ref('')
const selectedCategory = ref('')

// 使用自定义Hook获取数据
const { refetch } = useDataFetching(() => folkCultureStore.loadAllFolkCultures())

// 计算属性：过滤文化数据
const filteredCultures = computed(() => {
  logger.debug('执行文化数据过滤', { 
    searchQuery: searchQuery.value, 
    selectedCategory: selectedCategory.value 
  })
  let result = state.folkCultures
  
  // 根据搜索词过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    logger.debug('应用搜索过滤', { query })
    result = result.filter(culture => 
      (culture.title && culture.title.toLowerCase().includes(query)) ||
      (culture.description && culture.description.toLowerCase().includes(query)) ||
      (culture.region && culture.region.toLowerCase().includes(query))
    )
  }
  
  // 根据分类过滤
  if (selectedCategory.value) {
    logger.debug('应用分类过滤', { category: selectedCategory.value })
    result = result.filter(culture => 
      culture.category === selectedCategory.value
    )
  }
  
  logger.debug('过滤完成', { resultCount: result.length })
  return result
})

// 加载分类数据
const loadCategories = async () => {
  logger.info('开始加载分类数据')
  try {
    await folkCultureStore.loadCategories()
    logger.info('分类数据加载成功', { count: state.categories.length })
  } catch (error) {
    logger.error('分类数据加载失败', { error })
    throw error
  }
}

// 组件挂载时加载分类数据
onMounted(() => {
  logger.info('组件已挂载，开始初始化数据')
  loadCategories()
})
</script>

<template>
  <div class="culture-list">
    <h2>民俗文化列表</h2>
    
    <div class="filters">
      <div class="search-box">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="搜索民俗文化..." 
          class="search-input"
        >
      </div>
      
      <div class="category-filter">
        <label for="category">分类筛选：</label>
        <select v-model="selectedCategory" id="category">
          <option value="">全部分类</option>
          <option v-for="category in state.categories" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
      </div>
    </div>
    
    <LoadingSpinner v-if="state.loading" />
    
    <div v-else-if="state.error" class="error-message">
      {{ state.error.message || '获取数据失败，请稍后重试' }}
      <button @click="refetch" class="retry-btn">重试</button>
    </div>
    
    <div v-else-if="filteredCultures.length === 0" class="no-results">
      没有找到符合条件的民俗文化
    </div>
    
    <div v-else class="culture-grid">
      <FolkCultureCard 
        v-for="culture in filteredCultures" 
        :key="culture.id"
        :culture="culture"
      />
    </div>
  </div>
</template>

<style scoped>
/* 中国传统文化主题 - 采用中国传统色彩 */
.culture-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 0;
  background-image: url('data:image/svg+xml;utf8,<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><path d="M20,20 L80,20 L80,80 L20,80 Z" fill="none" stroke="%23f0e6d2" stroke-width="1" opacity="0.2"/></svg>');
}

/* 标题样式 - 中国风设计 */
.culture-list h2 {
  font-size: 2.5rem;
  margin-bottom: 2.5rem;
  color: #8B4513;
  text-align: center;
  position: relative;
  padding-bottom: 1rem;
  font-family: 'STZhongsong', 'FangSong', serif;
}

.culture-list h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 4px;
  background: linear-gradient(90deg, transparent, #C8102E, transparent);
}

/* 筛选区域 - 中国传统卷轴风格 */
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  padding: 2rem;
  background-color: #fcf7e8;
  border-radius: 8px;
  align-items: flex-end;
  box-shadow: 0 4px 12px rgba(139, 69, 19, 0.1);
  border: 1px solid #e8d4b4;
}

/* 搜索框样式 */
.search-box {
  flex: 1;
  min-width: 250px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 2px solid #e8d4b4;
  border-radius: 4px;
  font-size: 1rem;
  background-color: white;
  transition: border-color 0.3s;
}

.search-input:focus {
  outline: none;
  border-color: #C8102E;
  box-shadow: 0 0 0 2px rgba(200, 16, 46, 0.1);
}

/* 分类筛选器样式 */
.category-filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  color: #5a3921;
}

.category-filter select {
  padding: 0.75rem 1rem;
  border: 2px solid #e8d4b4;
  border-radius: 4px;
  font-size: 1rem;
  background-color: white;
  cursor: pointer;
  transition: border-color 0.3s;
}

.category-filter select:focus {
  outline: none;
  border-color: #C8102E;
  box-shadow: 0 0 0 2px rgba(200, 16, 46, 0.1);
}

/* 状态提示样式 */
.loading, .error-message, .no-results {
  text-align: center;
  padding: 3rem 2rem;
  font-size: 1.2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

/* 错误提示样式 - 中国红色系 */
.error-message {
  background-color: #fff0f0;
  color: #C8102E;
  border: 1px solid #ffcdd2;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  align-items: center;
}

/* 重试按钮样式 - 中国传统红色 */
.retry-btn {
  background-color: #C8102E;
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.retry-btn:hover {
  background-color: #a60c23;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

/* 无结果提示样式 */
.no-results {
  background-color: #f0f0f0;
  color: #666;
}

/* 文化卡片网格 - 错落有致的排列 */
.culture-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2.5rem;
  margin-top: 1rem;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .culture-list h2 {
    font-size: 2rem;
  }
  
  .filters {
    flex-direction: column;
    align-items: stretch;
    padding: 1.5rem;
  }
  
  .search-box {
    min-width: auto;
  }
  
  .category-filter {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
  }
  
  .category-filter label {
    text-align: left;
  }
  
  .culture-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .loading, .error-message, .no-results {
    padding: 2rem 1rem;
  }
}
</style>