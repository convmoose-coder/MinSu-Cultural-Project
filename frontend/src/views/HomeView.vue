<script setup>
import { ref, computed, onMounted } from 'vue'
import FolkCultureCard from '../components/FolkCultureCard.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import folkCultureStore from '../stores/folkCultureStore'
import { useDataFetching } from '../composables/useDataFetching'

// 获取store中的状态
const state = folkCultureStore.state

// 计算属性：获取前4个特色民俗文化
const featuredCultures = computed(() => {
  return state.folkCultures.slice(0, 4)
})

// 使用自定义Hook获取民俗文化数据
const { refetch: refetchCultures } = useDataFetching(() => folkCultureStore.loadAllFolkCultures())

// 单独加载地区数据
const loadRegions = async () => {
  await folkCultureStore.loadRegions()
}

// 组件挂载时加载数据
onMounted(() => {
  loadRegions()
})
</script>

<template>
  <div class="home">
    <section class="hero">
      <div class="hero-content">
        <h1>探索中国丰富多彩的民俗文化</h1>
        <p>穿越时空，感受中华民族五千年文明的魅力</p>
      </div>
    </section>
    
    <section class="featured">
      <h2>特色民俗文化</h2>
      <LoadingSpinner v-if="state.loading" />
      <div v-else-if="state.error" class="error-message">
        获取数据失败，请稍后重试
      </div>
      <div v-else class="culture-grid">
        <FolkCultureCard 
          v-for="culture in featuredCultures" 
          :key="culture.id"
          :culture="culture"
        />
      </div>
    </section>
    
    <section class="regions">
      <h2>按地区浏览</h2>
      <div class="region-tags">
        <router-link 
          v-for="region in state.regions" 
          :key="region"
          :to="{ path: '/regions', query: { region } }"
          class="region-tag"
        >
          {{ region }}
        </router-link>
      </div>
    </section>
    
    <section class="intro">
      <div class="intro-content">
        <h2>关于中国民俗文化</h2>
        <p>中国民俗文化是中华民族在长期的历史发展过程中形成的物质文化和非物质文化遗产的总和，包括传统节日、民间艺术、饮食习惯、服饰文化、建筑风格等多个方面。</p>
        <p>我们致力于收集、整理和展示全国各地丰富多彩的民俗文化资源，让更多的人了解和传承中华优秀传统文化。</p>
        <router-link to="/culture" class="btn">了解更多</router-link>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home {
  padding: 2rem 0;
}

.hero {
  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('/hero-bg.jpg');
  background-size: cover;
  background-position: center;
  color: white;
  padding: 6rem 0;
  text-align: center;
  margin-bottom: 3rem;
}

.hero-content h1 {
  font-size: 2.8rem;
  margin-bottom: 1rem;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 4px;
  text-align: center;
  margin: 1rem 0;
}

/* 调整文化网格布局以适应新组件 */
.culture-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .culture-grid {
    grid-template-columns: 1fr;
  }
}

.hero-content p {
  font-size: 1.4rem;
  max-width: 800px;
  margin: 0 auto;
}

.featured {
  margin-bottom: 3rem;
}

.featured h2 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  text-align: center;
  color: #8B4513;
}

.culture-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.culture-grid .card {
  cursor: pointer;
}

.culture-grid .region {
  color: #8B4513;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
}

.regions {
  margin-bottom: 3rem;
  background-color: #f5f5f5;
  padding: 2rem;
  border-radius: 8px;
}

.regions h2 {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  text-align: center;
  color: #8B4513;
}

.region-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.region-tag {
  background-color: #8B4513;
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  text-decoration: none;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.region-tag:hover {
  background-color: #A0522D;
}

.intro {
  background-color: #8B4513;
  color: white;
  padding: 3rem 0;
  text-align: center;
}

.intro-content {
  max-width: 800px;
  margin: 0 auto;
}

.intro-content h2 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
}

.intro-content p {
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
  line-height: 1.8;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .hero-content p {
    font-size: 1.1rem;
  }
  
  .culture-grid {
    grid-template-columns: 1fr;
  }
}
</style>