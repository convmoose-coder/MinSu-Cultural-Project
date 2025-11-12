<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import FolkCultureCard from '../components/FolkCultureCard.vue'
import { createLogger } from '../utils/logger'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import defaultImages from '@/assets/images/defaultImages.js'

// 内联类型定义，确保与FolkCultureCard组件属性匹配
interface FolkCulture {
  id: number;
  name: string; // 使用name而不是title
  description: string;
  category: string;
  region: string;
  image?: string;
  date?: string;
  created_at?: string;
}

// 创建日志实例
const logger = createLogger('RegionsView');

const route = useRoute()
const regions = ref([])
const allCultures = ref([])
const selectedRegion = ref('')
const error = ref('')
const loading = ref(true)

// 模拟数据 - 地区列表
const mockRegions = [
  '江南水乡',
  '塞北草原',
  '西南山地',
  '岭南风情',
  '西北大漠',
  '东北雪原',
  '中原大地',
  '东南沿海'
]

// 模拟数据 - 民俗文化列表
const mockCultures: FolkCulture[] = [
  // 江南水乡
  {
    id: 1,
    name: '苏州评弹',
    description: '苏州评弹是苏州地区特有的说唱艺术形式，被誉为江南曲艺的瑰宝。它融合了说、噱、弹、唱等艺术手法，内容多取材于历史故事和民间传说。',
    category: '传统艺术',
    region: '江南水乡',
    image: '@/assets/images/traditional.jpg',
    date: '2024-01-15'
  },
  {
    id: 2,
    name: '江南园林营造技艺',
    description: '江南园林以其精巧的设计和浓厚的文化底蕴闻名于世。园林营造技艺包括叠石、理水、植物配置等多个方面，体现了中国传统美学思想。',
    category: '传统工艺',
    region: '江南水乡',
    image: '@/assets/images/traditional.jpg',
    date: '2024-02-10'
  },
  // 塞北草原
  {
    id: 3,
    name: '蒙古族长调',
    description: '蒙古族长调是蒙古族传统音乐的代表，以其悠扬的旋律和丰富的情感表达闻名。它被誉为"草原音乐的活化石"，2005年被列入联合国非物质文化遗产名录。',
    category: '传统音乐',
    region: '塞北草原',
    image: '@/assets/images/traditional.jpg',
    date: '2024-03-05'
  },
  {
    id: 4,
    name: '那达慕大会',
    description: '那达慕大会是蒙古族的传统节日，意为"娱乐"或"游戏"。大会期间会举行赛马、摔跤、射箭等传统体育活动，是草原文化的重要组成部分。',
    category: '传统节日',
    region: '塞北草原',
    image: '@/assets/images/traditional.jpg',
    date: '2024-07-12'
  },
  // 西南山地
  {
    id: 5,
    name: '苗族银饰锻造技艺',
    description: '苗族银饰以其精湛的工艺和独特的造型闻名。银饰锻造技艺历史悠久，每件作品都凝聚着匠人的智慧和汗水，是苗族文化的重要载体。',
    category: '传统工艺',
    region: '西南山地',
    image: '@/assets/images/traditional.jpg',
    date: '2024-04-20'
  },
  {
    id: 6,
    name: '傣族泼水节',
    description: '泼水节是傣族的新年节日，通常在每年的4月中旬举行。节日期间，人们相互泼水祝福，象征着洗去过去一年的不顺，迎接新的开始。',
    category: '传统节日',
    region: '西南山地',
    image: '@/assets/images/traditional.jpg',
    date: '2024-04-13'
  },
  // 岭南风情
  {
    id: 7,
    name: '粤剧艺术',
    description: '粤剧是广东地区最具代表性的戏曲剧种，以其独特的唱腔和表演风格闻名。它融合了唱、做、念、打等艺术形式，深受岭南人民喜爱。',
    category: '传统艺术',
    region: '岭南风情',
    image: '@/assets/images/traditional.jpg',
    date: '2024-05-08'
  },
  {
    id: 8,
    name: '广彩瓷烧制技艺',
    description: '广彩瓷是广州地区特有的传统工艺美术品，以其色彩艳丽、图案繁复著称。广彩瓷烧制技艺包括制胎、施釉、彩绘、烧制等多个环节，工艺精湛。',
    category: '传统工艺',
    region: '岭南风情',
    image: '@/assets/images/traditional.jpg',
    date: '2024-05-22'
  },
  // 西北大漠
  {
    id: 9,
    name: '敦煌壁画艺术',
    description: '敦煌壁画是中国古代艺术的瑰宝，以其丰富的内容和精湛的技艺闻名于世。壁画描绘了佛本生故事、经变画等内容，色彩鲜艳，线条流畅。',
    category: '传统艺术',
    region: '西北大漠',
    image: '@/assets/images/traditional.jpg',
    date: '2024-06-15'
  },
  {
    id: 10,
    name: '维吾尔族十二木卡姆',
    description: '十二木卡姆是维吾尔族传统音乐的代表，是一种集歌、舞、乐于一体的综合艺术形式。它被誉为"东方音乐的活化石"，2005年被列入联合国非物质文化遗产名录。',
    category: '传统音乐',
    region: '西北大漠',
    image: '@/assets/images/traditional.jpg',
    date: '2024-06-30'
  },
  // 东北雪原
  {
    id: 11,
    name: '东北二人转',
    description: '东北二人转是东北地区最具代表性的民间艺术形式，以其幽默风趣的表演和通俗易懂的语言深受观众喜爱。它融合了说唱、舞蹈、杂技等多种艺术元素。',
    category: '传统艺术',
    region: '东北雪原',
    image: '@/assets/images/traditional.jpg',
    date: '2024-01-28'
  },
  // 中原大地
  {
    id: 12,
    name: '豫剧艺术',
    description: '豫剧是河南省的主要地方戏曲剧种，也是中国五大戏曲剧种之一。它以其高亢激昂的唱腔和质朴生动的表演风格著称，深受中原人民喜爱。',
    category: '传统艺术',
    region: '中原大地',
    image: '@/assets/images/traditional.jpg',
    date: '2024-03-20'
  },
  // 东南沿海
  {
    id: 13,
    name: '闽南语歌仔戏',
    description: '歌仔戏是闽南地区特有的戏曲剧种，以闽南语演唱，融合了民间歌谣、说唱和戏曲艺术。它是闽南文化的重要组成部分，深受海内外闽南人的喜爱。',
    category: '传统艺术',
    region: '东南沿海',
    image: '@/assets/images/traditional.jpg',
    date: '2024-04-05'
  }
]

// 计算属性：过滤当前地区的文化
const cultures = computed(() => {
  if (!selectedRegion.value) return []
  return allCultures.value.filter(culture => culture.region === selectedRegion.value)
})

// 为每个文化项添加默认图片
const ensureCulturesHaveImages = (cultureItems: FolkCulture[]) => {
  return cultureItems.map(culture => ({
    ...culture,
    image: culture.image || defaultImages.culture
  }))
}

// 获取数据
const fetchData = async () => {
  logger.info('开始获取地区和文化数据');
  const startTime = performance.now();
  
  try {
    loading.value = true
    error.value = ''
    
    // 模拟API延迟
    await new Promise(resolve => setTimeout(resolve, 800));
    
    // 使用模拟数据
    regions.value = mockRegions
    allCultures.value = ensureCulturesHaveImages(mockCultures)
    
    // 检查URL中是否有地区参数
    const urlRegion = route.query.region
    if (urlRegion && typeof urlRegion === 'string' && regions.value.includes(urlRegion)) {
      selectedRegion.value = urlRegion
    } else if (regions.value.length > 0) {
      // 默认选择第一个地区
      selectedRegion.value = regions.value[0]
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
  } finally {
    loading.value = false
  }
}

// 处理地区变更
const handleRegionChange = (region: string) => {
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
    <!-- 页面头部，与其他页面保持一致的渐变背景 -->
    <div class="regions-header">
      <div class="header-content">
        <h1>地区分类</h1>
        <p>探索中国各地丰富多彩的民族文化</p>
      </div>
    </div>
    
    <LoadingSpinner v-if="loading" :full-screen="false" message="正在加载地区数据..." />
    
    <div v-else-if="error" class="error-message">
      <p>{{ error }}</p>
      <button class="retry-btn" @click="handleRetry">重试</button>
    </div>
    
    <div class="regions-content">
      <div class="regions-container">
      <div class="region-list">
        <h3>选择地区</h3>
        <ul>
          <li 
            v-for="region in regions" 
            :key="region"
            :class="{ active: selectedRegion === region }"
            class="touch-feedback"
            @click="handleRegionChange(region)"
          >
            {{ region }}
          </li>
        </ul>
      </div>
      
      <div class="region-content">
        <h3>{{ selectedRegion }}</h3>
        
        <div v-if="cultures.length === 0" class="no-cultures">
          该地区暂无民族文化记录
        </div>
        
        <div v-else class="culture-grid">
          <div v-for="culture in cultures" :key="culture.id" class="touch-feedback">
            <FolkCultureCard 
              :culture="culture"
            />
          </div>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<style scoped>
.regions-view {
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* 页面头部渐变背景，与首页和民族文化页面保持一致 */
.regions-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 60px 20px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.regions-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.regions-header p {
  font-size: 1.2rem;
  opacity: 0.9;
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
  background-color: #667eea;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s, transform 0.2s;
  font-weight: 500;
}

.retry-btn:hover {
  background-color: #5a5fc7;
  transform: translateY(-1px);
}

.retry-btn:active {
  transform: translateY(0);
}

.regions-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.regions-container {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
  background-color: white;
  border-radius: 10px;
  padding: 30px;
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
  margin-bottom: 1.5rem;
  color: #1e293b;
  font-size: 1.3rem;
  font-weight: 600;
}

.region-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.region-list li {
  padding: 12px 20px;
  margin-bottom: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #475569;
  border: 1px solid transparent;
  font-size: 16px;
  font-weight: 500;
}

.region-list li:hover {
  background-color: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border-color: #667eea;
}

.region-list li.active {
  background-color: #667eea;
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
  color: #1e293b;
  font-size: 1.6rem;
  font-weight: 600;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #667eea;
  display: inline-block;
}

.no-cultures {
  text-align: center;
  padding: 4rem;
  color: #64748b;
  background-color: #f8fafc;
  border-radius: 10px;
  font-size: 1.1rem;
  border: 1px dashed #e2e8f0;
}

.culture-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 30px;
}

/* 响应式布局，与其他页面保持一致 */
  @media (max-width: 992px) {
    .regions-container {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }
    
    .region-list {
      display: flex;
      overflow-x: auto;
      padding-bottom: 0.5rem;
      -webkit-overflow-scrolling: touch;
    }
    
    .region-list li {
      white-space: nowrap;
      margin-right: 0.75rem;
      margin-bottom: 0;
      padding: 10px 16px;
    }
    
    .culture-grid {
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 20px;
    }
  }

  @media (max-width: 768px) {
    .regions-header {
      padding: 40px 15px;
    }
    
    .regions-header h1 {
      font-size: 2rem;
    }
    
    .regions-header p {
      font-size: 1rem;
    }
    
    .regions-content {
      padding: 20px 15px;
    }
    
    .regions-container {
      padding: 20px;
      border-radius: 8px;
    }
    
    .region-content h3 {
      font-size: 1.4rem;
    }
    
    .culture-grid {
      grid-template-columns: 1fr;
      gap: 20px;
    }
    
    .no-cultures {
      padding: 3rem 1.5rem;
      font-size: 1rem;
    }
  }

  @media (max-width: 480px) {
    .regions-header h1 {
      font-size: 1.8rem;
    }
    
    .region-list {
      padding-bottom: 10px;
    }
    
    .region-list li {
      font-size: 14px;
      padding: 8px 12px;
      border-radius: 6px;
    }
    
    .regions-container {
      padding: 16px;
    }
    
    .region-content h3 {
      font-size: 1.25rem;
    }
  }

  /* 触摸动效优化 - 与其他页面保持一致 */
  .touch-feedback {
    touch-action: manipulation;
    -webkit-tap-highlight-color: transparent;
    user-select: none;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    position: relative;
    transition: transform 0.1s ease;
    overflow: hidden;
  }

  /* 触摸反馈相关样式需要同步更新颜色 */
  .touch-feedback:active {
    transform: scale(0.97);
    background-color: rgba(102, 126, 234, 0.05);
  }

  .touch-feedback::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(102, 126, 234, 0.1);
    opacity: 0;
    transition: opacity 0.2s;
    border-radius: inherit;
    pointer-events: none;
    z-index: 1;
  }

  .touch-feedback:active::before {
    opacity: 1;
  }

  /* 触摸滑动优化 */
  .regions-view {
    -webkit-overflow-scrolling: touch;
    overflow-x: hidden;
  }

  /* 确保区域内容容器也有触摸反馈 */
  .region-content {
    position: relative;
  }

  /* 触摸相关的全局优化 */
  .culture-grid {
    touch-action: manipulation;
  }

  /* 地区列表项触摸效果增强 */
  .region-list li {
    position: relative;
    touch-action: manipulation;
    -webkit-tap-highlight-color: transparent;
  }

  /* 引入与首页和民族文化页面一致的动画效果 */
  @keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
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

  @keyframes pulse {
    0%, 100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.02);
    }
  }

  /* 动画类 */
  .float-animation {
    animation: float 6s ease-in-out infinite;
  }

  .fade-in-up {
    animation: fadeInUp 0.8s ease-out forwards;
  }

  .pulse-animation {
    animation: pulse 3s infinite;
  }

  /* 为文化卡片添加悬停动画效果 */
  .culture-grid > div {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .culture-grid > div:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15);
  }

  /* 为地区选择项添加入场动画 */
  .region-list li {
    animation: fadeInUp 0.5s ease-out backwards;
  }

  .region-list li:nth-child(1) { animation-delay: 0.1s; }
  .region-list li:nth-child(2) { animation-delay: 0.2s; }
  .region-list li:nth-child(3) { animation-delay: 0.3s; }
  .region-list li:nth-child(4) { animation-delay: 0.4s; }
  .region-list li:nth-child(5) { animation-delay: 0.5s; }
  .region-list li:nth-child(6) { animation-delay: 0.6s; }
  .region-list li:nth-child(7) { animation-delay: 0.7s; }
  .region-list li:nth-child(8) { animation-delay: 0.8s; }

  /* 为标题添加淡入动画 */
  .regions-header h1,
  .regions-header p,
  .region-content h3 {
    animation: fadeInUp 0.8s ease-out;
  }

</style>