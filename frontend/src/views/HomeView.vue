<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Search, 
  ArrowRight, 
  Location, 
  Calendar, 
  Star,
  View,
  Share,
  StarFilled,
  Download,
  Plus,
  MoreFilled
} from '@element-plus/icons-vue'
import CustomButton from '@/components/CustomButton.vue'
import ButtonGroup from '@/components/ButtonGroup.vue'
import FolkCultureCard from '@/components/FolkCultureCard.vue'
import { getFolkCultures, getRegions } from '@/api/culture'
import defaultImages from '@/assets/images/defaultImages.js'

const router = useRouter()
const loading = ref(false) // 将初始值改为false，避免不必要的加载状态
const cultures = ref([])
const regions = ref([])

// 统计数据
const stats = ref({
  cultureCount: 0,
  regionCount: 0,
  visitCount: 0
})

// 特色民俗文化（取前6个）
const featuredCultures = computed(() => {
  return cultures.value.slice(0, 6)
})

// 特色地区（取前6个）
const featuredRegions = computed(() => {
  return regions.value.slice(0, 6)
})

// 获取民俗文化数据
const fetchCultures = async () => {
  try {
    const response = await getFolkCultures({ limit: 6 })
    cultures.value = response.data.data || []
    stats.value.cultureCount = response.data.total || cultures.value.length
  } catch (error) {
    console.error('获取民俗文化数据失败:', error)
    // 使用模拟数据作为后备
    cultures.value = [
      { id: 1, name: '春节', region: '全国', category: '节日', description: '中国最重要的传统节日' },
      { id: 2, name: '端午节', region: '全国', category: '节日', description: '纪念屈原的传统节日' },
      { id: 3, name: '京剧', region: '北京', category: '戏曲', description: '中国传统戏曲的代表' },
      { id: 4, name: '剪纸', region: '全国', category: '手工艺', description: '中国传统民间艺术' },
      { id: 5, name: '舞龙舞狮', region: '全国', category: '表演', description: '中国传统表演艺术' },
      { id: 6, name: '中秋赏月', region: '全国', category: '节日', description: '团圆赏月的传统习俗' }
    ]
    stats.value.cultureCount = 100 // 模拟数据
  }
}

// 获取地区数据
const fetchRegions = async () => {
  try {
    const response = await getRegions({ limit: 6 })
    // 处理API返回的地区名称数组，转换为组件需要的对象格式
    if (Array.isArray(response.data)) {
      regions.value = response.data.map((name, index) => ({
        id: index + 1,
        name: name || '未知地区',
        culture_count: 0 // 实际项目中应该从API获取准确的数量
      }))
    } else {
      regions.value = response.data?.data || []
    }
    stats.value.regionCount = response.data?.total || regions.value.length
  } catch (error) {
    console.error('获取地区数据失败:', error)
    // 使用模拟数据作为后备
    regions.value = [
      { id: 1, name: '北京', description: '中国首都，传统文化与现代文明交融', culture_count: 25 },
      { id: 2, name: '上海', description: '国际化大都市，海派文化发源地', culture_count: 20 },
      { id: 3, name: '广东', description: '岭南文化中心，改革开放前沿', culture_count: 30 },
      { id: 4, name: '四川', description: '天府之国，巴蜀文化发源地', culture_count: 28 },
      { id: 5, name: '云南', description: '多民族聚居，民族文化丰富多彩', culture_count: 35 },
      { id: 6, name: '陕西', description: '中华文明发源地，历史文化悠久', culture_count: 32 }
    ]
    stats.value.regionCount = 34 // 模拟数据
  }
}

// 模拟访问次数
const generateVisitCount = () => {
  // 生成一个随机的大数作为访问次数
  stats.value.visitCount = Math.floor(Math.random() * 100000) + 50000
}

// 导航到民俗文化页面
const navigateToCulture = () => {
  router.push('/culture')
}

// 导航到地区浏览页面
const navigateToRegions = () => {
  router.push('/regions')
}

// 导航到特定地区
const navigateToRegion = (regionId) => {
  router.push(`/regions/${regionId}`)
}

// 处理图片加载错误
const handleImageError = (event) => {
  event.target.src = defaultImages.region
}

// 动画相关
const visibleSections = ref({
  hero: false,
  culture: false,
  regions: false
})

// 检查元素是否在视口中
const isElementInViewport = (el) => {
  const rect = el.getBoundingClientRect()
  return (
    rect.top <= (window.innerHeight || document.documentElement.clientHeight) * 0.8 &&
    rect.bottom >= 0
  )
}

// 检查可见区域
const checkVisibility = () => {
  const sections = {
    hero: document.querySelector('.hero-section'),
    culture: document.querySelector('.featured-culture-section'),
    regions: document.querySelector('.regions-section')
  }
  
  Object.keys(sections).forEach(key => {
    if (sections[key] && isElementInViewport(sections[key])) {
      visibleSections.value[key] = true
    }
  })
}

// 组件挂载时获取数据
onMounted(() => {
  // 移除原来的延时加载，直接并行加载数据
  Promise.all([
    fetchCultures(),
    fetchRegions()
  ]).catch(error => {
    console.error('数据加载失败:', error)
    ElMessage.error('数据加载失败，请刷新页面重试')
  })
  
  generateVisitCount()
  loading.value = false
  
  // 初始检查可见区域
  nextTick(() => {
    checkVisibility()
    visibleSections.value.hero = true // 英雄区域默认可见
  })
  
  // 添加滚动监听
  window.addEventListener('scroll', checkVisibility)
})

// 组件卸载时移除监听
onUnmounted(() => {
  window.removeEventListener('scroll', checkVisibility)
})
</script>

<template>
  <div class="home-view">
    <!-- 英雄区 -->
    <section class="hero-section" :class="{ 'visible': visibleSections.hero }">
      <div class="container">
        <div class="hero-content">
          <div class="hero-text" v-motion-slide-visible-once-left>
            <h1 class="hero-title">探索中华民俗文化</h1>
            <p class="hero-subtitle">传承千年文明，弘扬民族精神</p>
            <div class="hero-actions">
              <ButtonGroup size="large" gap>
                <CustomButton 
                  variant="primary" 
                  size="large"
                  icon="ArrowRight"
                  @click="navigateTo('/explore')"
                >
                  探索民俗文化
                </CustomButton>
                <CustomButton 
                  variant="outline" 
                  size="large"
                  icon="View"
                  @click="navigateTo('/regions')"
                >
                  浏览地区
                </CustomButton>
              </ButtonGroup>
            </div>
          </div>
          <div class="hero-image" v-motion-slide-visible-once-right>
            <img src="@/assets/images/hero-image.jpg" alt="民俗文化" />
          </div>
        </div>
      </div>
      <div class="hero-decoration">
        <div class="decoration-pattern"></div>
      </div>
    </section>

    <!-- 民俗文化展示 -->
    <section class="featured-culture-section" :class="{ 'visible': visibleSections.culture }">
      <div class="container">
        <div class="section-header" v-motion-slide-visible-once-bottom>
          <h2 class="section-title">民俗文化</h2>
          <p class="section-subtitle">领略中华大地的多元文化魅力</p>
        </div>

        <div class="culture-grid" v-if="!loading">
          <FolkCultureCard 
            v-for="(culture, index) in featuredCultures" 
            :key="culture.id"
            :culture="culture"
            v-motion-slide-visible-once-bottom
            :delay="index * 100"
          />
        </div>

        <div v-else class="loading-container">
          <el-skeleton :rows="3" animated />
        </div>

        <div class="section-footer" v-motion-slide-visible-once-bottom>
          <el-button type="text" class="view-more-btn" @click="navigateToCulture">
            查看更多文化
            <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>
      </div>
    </section>

    <!-- 热门地区 -->
    <section class="regions-section traditional-pattern" :class="{ 'visible': visibleSections.regions }">
      <div class="container">
        <div class="section-header" v-motion-slide-visible-once-bottom>
          <h2 class="section-title">热门地区</h2>
          <CustomButton 
            variant="ghost" 
            size="small"
            icon="ArrowRight"
            @click="navigateTo('/regions')"
          >
            查看全部
          </CustomButton>
        </div>

        <div class="regions-grid" v-if="!loading">
          <div 
            v-for="(region, index) in featuredRegions" 
            :key="region.id || index"
            class="region-card"
            v-motion-slide-visible-once-bottom
            :delay="index * 100"
            @click="() => { if (region.id) navigateToRegion(region.id) }"
          >
            <div class="region-image">
              <img :src="region.image || defaultImages.region" :alt="region.name || '地区图片'" @error="handleImageError" />
            </div>
            <div class="region-content">
              <h3 class="region-name">{{ region.name || '未知地区' }}</h3>
              <p class="region-description">{{ region.description || '暂无描述' }}</p>
              <div class="region-stats">
                <span class="stat-item">
                  <el-icon><Document /></el-icon>
                  {{ region.culture_count || 0 }} 项文化
                </span>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="loading-container">
          <el-skeleton :rows="3" animated />
        </div>

        <div class="section-footer" v-motion-slide-visible-once-bottom>
          <el-button type="text" class="view-more-btn" @click="navigateToRegions">
            查看所有地区
            <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>
      </div>
    </section>

    <!-- 介绍区 -->
    <section class="intro-section">
      <div class="container">
        <div class="intro-content">
          <div class="intro-text" v-motion-slide-visible-once-left>
            <h2 class="intro-title">关于民俗文化平台</h2>
            <p class="intro-description">
              我们的民俗文化平台致力于收集、整理和展示中华大地上丰富多彩的民俗文化。
              从北国的冰雪文化到南疆的热带风情，从东海之滨的渔家习俗到西域高原的游牧传统，
              每一种文化都是中华民族宝贵的精神财富。
            </p>
            <p class="intro-description">
              通过我们的平台，您可以深入了解各地的民俗传统、节庆活动、民间艺术和生活方式，
              感受中华文化的博大精深和多元一体。
            </p>
            <div class="section-header">
              <CustomButton 
                variant="ghost" 
                size="small"
                icon="MoreFilled"
                @click="navigateTo('/about')"
              >
                了解更多
              </CustomButton>
            </div>
            <div class="intro-stats">
              <div class="stat-item">
                <div class="stat-number">{{ stats.cultureCount }}</div>
                <div class="stat-label">民俗文化</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ stats.regionCount }}</div>
                <div class="stat-label">覆盖地区</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ stats.visitCount }}</div>
                <div class="stat-label">访问次数</div>
              </div>
            </div>
          </div>
          <div class="intro-image" v-motion-slide-visible-once-right>
            <img src="@/assets/intro-image.jpg" alt="民俗文化介绍" />
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style lang="scss">
@use '@/assets/styles/global.scss' as *;

// 直接定义缺失的变量
$spacing-3xl: 64px;
$spacing-2xl: 48px;
$spacing-xl: 32px;
$spacing-lg: 24px;
$spacing-md: 16px;
$spacing-sm: 8px;
$spacing-xs: 4px;
$font-size-4xl: 36px;
$font-size-3xl: 30px;
$font-size-2xl: 24px;
$font-size-xl: 20px;
$font-size-lg: 18px;
$font-size-base: 16px;
$font-size-sm: 14px;
$text-primary: #2d3748;
$text-secondary: #718096;
$primary-color: #3182ce;
$primary-dark: #2c5282;
$secondary-color: #805ad5;
$secondary-dark: #553c9a;
$bg-primary: #ffffff;
$bg-secondary: #f7fafc;
$border-radius-lg: 12px;
$shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
$shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
$shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
$line-height-tight: 1.25;
$line-height-relaxed: 1.75;
$font-family-chinese: 'PingFang SC', 'Microsoft YaHei', sans-serif;

.home-view {
  width: 100%;
}

// 英雄区域
.hero-section {
  @include hero-gradient;
  padding: $spacing-3xl 0;
  position: relative;
  overflow: hidden;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s ease-out;
  
  &.visible {
    opacity: 1;
    transform: translateY(0);
  }
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    @include hero-pattern;
    z-index: 0;
  }
  
  .container {
    position: relative;
    z-index: 1;
  }
  
  .hero-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: $spacing-xl;
    
    @include responsive(md) {
      flex-direction: column;
      text-align: center;
    }
  }
  
  .hero-text {
    flex: 1;
    
    .hero-title {
      @include hero-title;
      color: $text-primary;
      margin-bottom: $spacing-lg;
      
      @include responsive(md) {
        font-size: $font-size-3xl;
      }
    }
    
    .hero-subtitle {
      @include hero-subtitle;
      color: $text-secondary;
      margin-bottom: $spacing-2xl;
      
      @include responsive(md) {
        font-size: $font-size-lg;
      }
    }
    
    .hero-actions {
      display: flex;
      flex-direction: column;
      gap: $spacing-lg;
      margin-top: $spacing-xl;
      
      .secondary-actions {
        display: flex;
        gap: $spacing-md;
        justify-content: center;
        
        @include responsive(md) {
          justify-content: flex-start;
        }
      }
    }
  }
  
  .hero-image {
    flex: 1;
    
    img {
      width: 100%;
      height: auto;
      border-radius: $border-radius-lg;
      box-shadow: $shadow-xl;
    }
  }
  
  .hero-decoration {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1;
    opacity: 0.1;
    pointer-events: none;
    
    .decoration-pattern {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-image: 
        radial-gradient(circle at 10% 20%, rgba($primary-color, 0.3) 0%, transparent 50%),
        radial-gradient(circle at 90% 80%, rgba($secondary-color, 0.3) 0%, transparent 50%);
    }
  }
}

// 区域通用样式
.featured-culture-section,
.regions-section,
.intro-section {
  padding: $spacing-3xl 0;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s ease-out;
  
  &.visible {
    opacity: 1;
    transform: translateY(0);
  }
  
  @include responsive(md) {
    padding: $spacing-2xl 0;
  }
}

.section-header {
  text-align: center;
  margin-bottom: $spacing-3xl;
  
  .section-title {
    @include section-title;
    color: $text-primary;
    margin-bottom: $spacing-md;
    
    @include responsive(md) {
      font-size: $font-size-2xl;
    }
  }
  
  .section-subtitle {
    @include section-subtitle;
    color: $text-secondary;
    max-width: 600px;
    margin: 0 auto;
  }
}

.section-footer {
  text-align: center;
  margin-top: $spacing-xl;
  
  .view-more-btn {
    @include link-button;
    @include link-theme("primary");
  }
}

// 特色民俗文化区
.featured-culture-section {
  background-color: $bg-primary;
  
  .culture-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: $spacing-xl;
    
    @include responsive(md) {
      grid-template-columns: 1fr;
      gap: $spacing-lg;
    }
  }
}

// 地区浏览区
.regions-section {
  @include section-bg("secondary");
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('@/assets/images/traditional-pattern.svg');
    background-repeat: repeat;
    opacity: 0.03;
    pointer-events: none;
  }
  
  .container {
    position: relative;
    z-index: 1;
  }
  
  .regions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: $spacing-xl;
    
    @include responsive(md) {
      grid-template-columns: 1fr;
      gap: $spacing-lg;
    }
  }
  
  .region-card {
    @include card;
    @include card-hover;
    overflow: hidden;
    cursor: pointer;
    
    .region-image {
      height: 200px;
      overflow: hidden;
      
      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s ease;
      }
    }
    
    &:hover .region-image img {
      transform: scale(1.05);
    }
    
    .region-content {
      padding: $spacing-lg;
      
      .region-name {
        font-size: $font-size-xl;
        font-weight: 600;
        color: $text-primary;
        margin-bottom: $spacing-sm;
      }
      
      .region-description {
        color: $text-secondary;
        margin-bottom: $spacing-md;
        line-height: $line-height-relaxed;
      }
      
      .region-stats {
        display: flex;
        gap: $spacing-md;
        
        .stat-item {
          display: flex;
          align-items: center;
          gap: $spacing-xs;
          color: #ADB5BD;
          font-size: $font-size-sm;
        }
      }
    }
  }
}

// 介绍区
.intro-section {
  background-color: $bg-primary;
  
  .intro-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: $spacing-3xl;
    
    @include responsive(md) {
      flex-direction: column;
      text-align: center;
    }
  }
  
  .intro-text {
    flex: 1;
    
    .intro-title {
      font-size: $font-size-3xl;
      font-weight: 600;
      color: $text-primary;
      margin-bottom: $spacing-xl;
      
      @include responsive(md) {
        font-size: $font-size-2xl;
      }
    }
    
    .intro-description {
      font-size: $font-size-base;
      color: $text-secondary;
      line-height: $line-height-relaxed;
      margin-bottom: $spacing-lg;
    }
    
    .intro-stats {
      display: flex;
      gap: $spacing-xl;
      margin-top: $spacing-2xl;
      
      @include responsive(md) {
        justify-content: center;
      }
      
      .stat-item {
        text-align: center;
        
        .stat-number {
          font-size: $font-size-3xl;
          font-weight: 700;
          color: $primary-color;
          margin-bottom: $spacing-xs;
        }
        
        .stat-label {
          font-size: $font-size-sm;
          color: #ADB5BD;
        }
      }
    }
  }
  
  .intro-image {
    flex: 1;
    
    img {
      width: 100%;
      height: auto;
      border-radius: $border-radius-lg;
      box-shadow: $shadow-xl;
    }
  }
}

// 加载状态
.loading-container {
  @include loading-skeleton;
}
</style>