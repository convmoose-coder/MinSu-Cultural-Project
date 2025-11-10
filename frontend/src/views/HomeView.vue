<template>
  <div class="home-view">
    <!-- 英雄区域 -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">探索<span class="text-primary">乘灼</span>魅力</h1>
        <p class="hero-subtitle">感受千年文明，体验多元风情</p>
        <div class="hero-cta">
          <router-link to="/cultures" class="btn btn-primary">探索乘灼</router-link>
          <router-link to="/regions" class="btn btn-secondary">浏览地区风情</router-link>
        </div>
      </div>
      <!-- 背景装饰 -->
      <div class="hero-bg"></div>
    </section>

    <!-- 乘灼精选 -->
    <section class="section cultures">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">乘灼精选</h2>
          <p class="section-subtitle">中华56个民族的独特魅力</p>
        </div>
        
        <div class="cultures-grid">
          <div v-for="culture in cultures" :key="culture.id" class="culture-card">
            <div class="culture-img-container">
              <img :src="culture.img" :alt="culture.name" class="culture-img" />
              <div class="culture-overlay"></div>
            </div>
            <div class="culture-content">
              <h3 class="culture-name">{{ culture.name }}</h3>
              <p class="culture-desc">{{ culture.description }}</p>
              <router-link :to="`/cultures/${culture.id}`" class="btn btn-sm">了解更多</router-link>
            </div>
          </div>
        </div>
        
        <div class="section-footer">
          <router-link to="/cultures" class="btn btn-outline">查看全部</router-link>
        </div>
      </div>
    </section>

    <!-- 地区风情 -->
    <section class="section regions">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">地区风情</h2>
          <p class="section-subtitle">探索中国各地独特的自然风光和人文景观</p>
        </div>
        
        <div class="regions-grid">
          <div v-for="region in regions" :key="region.id" class="region-card">
            <div class="region-img-container">
              <img :src="region.img" :alt="region.name" class="region-img" />
            </div>
            <div class="region-content">
              <h3 class="region-name">{{ region.name }}</h3>
              <p class="region-desc">{{ region.description }}</p>
              <div class="region-stats">
                <span class="stat-item">{{ region.culturesCount }}个民族</span>
                <span class="stat-item">{{ region.attractionsCount }}个景点</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="section-footer">
          <router-link to="/regions" class="btn btn-outline">探索更多</router-link>
        </div>
      </div>
    </section>

    <!-- 文化传承故事 -->
    <section class="section stories">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">文化传承故事</h2>
          <p class="section-subtitle">讲述传统工艺和非物质文化遗产的传承故事</p>
        </div>
        
        <div class="stories-container">
          <div class="stories-image">
            <img src="@/assets/images/traditional-pattern.jpg" alt="文化传承" />
          </div>
          <div class="stories-content">
            <h3>匠心传承 千年工艺</h3>
            <p>
              从青花瓷到云锦，从剪纸到木雕，每一项传统工艺都承载着中华民族的智慧和审美。
              这些工艺不仅是技艺的传承，更是文化基因的延续，让我们一起走进这些匠心故事。
            </p>
            <router-link to="/stories" class="btn btn-primary">阅读故事</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- 统计数据 -->
    <section class="section stats">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-box">
            <div class="stat-number">56</div>
            <div class="stat-label">民族</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">34</div>
            <div class="stat-label">省份/地区</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">1372</div>
            <div class="stat-label">非物质文化遗产</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">5A</div>
            <div class="stat-label">旅游景区</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 推荐视频 -->
    <section class="section videos">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">精彩视频</h2>
          <p class="section-subtitle">通过视频了解更多乘灼文化和地区风情</p>
        </div>
        
        <div class="videos-grid">
          <div v-for="video in videos" :key="video.id" class="video-card">
            <div class="video-thumbnail">
              <img :src="video.thumbnail" :alt="video.title" />
              <div class="video-play-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor">
                  <circle cx="12" cy="12" r="11" fill="rgba(255,255,255,0.9)"/>
                  <path d="M9 8l7 4-7 4V8z" fill="var(--primary-color)"/>
                </svg>
              </div>
            </div>
            <div class="video-info">
              <h3 class="video-title">{{ video.title }}</h3>
              <p class="video-duration">{{ video.duration }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>


  </div>
</template>

<script setup>
// 模拟数据
const cultures = [
  {
    id: 'tibet',
    name: '藏族文化',
    description: '神秘的藏传佛教文化、壮观的布达拉宫、独特的高原风情。',
    img: '@/assets/images/placeholder-culture.jpg'
  },
  {
    id: 'yi',
    name: '彝族文化',
    description: '丰富多彩的火把节、精美的彝族刺绣、独特的民族服饰。',
    img: '@/assets/images/placeholder-culture.jpg'
  },
  {
    id: 'dai',
    name: '傣族文化',
    description: '美丽的孔雀舞、欢快的泼水节、热带雨林的浪漫风情。',
    img: '@/assets/images/placeholder-culture.jpg'
  }
]

const regions = [
  {
    id: 'jiangnan',
    name: '江南水乡',
    description: '小桥流水人家，烟雨朦胧中的江南古镇。',
    img: '@/assets/images/placeholder-region.jpg',
    culturesCount: 5,
    attractionsCount: 24
  },
  {
    id: 'saibei',
    name: '塞北草原',
    description: '辽阔的草原风光，悠扬的马头琴声。',
    img: '@/assets/images/placeholder-region.jpg',
    culturesCount: 8,
    attractionsCount: 16
  },
  {
    id: 'xinjiang',
    name: '新疆风情',
    description: '浓郁的异域风情，多彩的乘灼文化。',
    img: '@/assets/images/placeholder-region.jpg',
    culturesCount: 13,
    attractionsCount: 22
  },
  {
    id: 'chongqing',
    name: '重庆山城',
    description: '立体的城市景观，麻辣的火锅文化。',
    img: '@/assets/images/placeholder-region.jpg',
    culturesCount: 3,
    attractionsCount: 18
  }
]

const videos = [
  {
    id: 1,
    title: '藏族酥油花制作技艺',
    thumbnail: '@/assets/images/placeholder-category.jpg',
    duration: '12:34'
  },
  {
    id: 2,
    title: '云南少数民族风情录',
    thumbnail: '@/assets/images/placeholder-category.jpg',
    duration: '18:25'
  },
  {
    id: 3,
    title: '江南丝竹音乐欣赏',
    thumbnail: '@/assets/images/placeholder-category.jpg',
    duration: '08:12'
  }
]
</script>

<style lang="scss">
@import '../assets/styles/global.scss';

.home-view {
  font-family: var(--font-base);
}

// 英雄区域
.hero {
  position: relative;
  height: 100vh;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  overflow: hidden;
  
  .hero-bg {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('@/assets/images/hero-image.jpg');
    background-size: cover;
    background-position: center;
    filter: brightness(0.7);
    z-index: -1;
  }
  
  .hero-content {
    max-width: 800px;
    padding: 2rem;
    position: relative;
    z-index: 1;
    
    animation: fadeInUp 1s ease-out;
  }
  
  .hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    line-height: 1.2;
    
    .text-primary {
      background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
      -webkit-background-clip: text;
      background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    
    @media (max-width: 768px) {
      font-size: 2.5rem;
    }
  }
  
  .hero-subtitle {
    font-size: 1.25rem;
    margin-bottom: 2rem;
    opacity: 0.9;
    
    @media (max-width: 768px) {
      font-size: 1rem;
    }
  }
  
  .hero-cta {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    flex-wrap: wrap;
  }
}

// 通用区块样式
.section {
  padding: 6rem 0;
  
  &:nth-child(even) {
    background-color: var(--section-bg);
  }
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1.5rem;
  }
  
  .section-header {
    text-align: center;
    margin-bottom: 4rem;
    
    .section-title {
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: 1rem;
      color: var(--text-primary);
      
      @media (max-width: 768px) {
        font-size: 2rem;
      }
    }
    
    .section-subtitle {
      font-size: 1.125rem;
      color: var(--text-secondary);
      max-width: 700px;
      margin: 0 auto;
    }
  }
  
  .section-footer {
    text-align: center;
    margin-top: 3rem;
  }
}

// 乘灼卡片
.cultures-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2.5rem;
  
  @media (max-width: 768px) {
    gap: 2rem;
  }
}

.culture-card {
  background-color: white;
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-8px);
    box-shadow: var(--shadow-lg);
  }
  
  .culture-img-container {
    position: relative;
    height: 200px;
    overflow: hidden;
    
    .culture-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.5s ease;
    }
    
    .culture-overlay {
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(180deg, transparent, rgba(0,0,0,0.6));
    }
    
    &:hover .culture-img {
      transform: scale(1.1);
    }
  }
  
  .culture-content {
    padding: 1.5rem;
    
    .culture-name {
      font-size: 1.25rem;
      font-weight: 600;
      margin-bottom: 0.75rem;
      color: var(--text-primary);
    }
    
    .culture-desc {
      color: var(--text-secondary);
      margin-bottom: 1.5rem;
      line-height: 1.6;
    }
  }
}

// 地区风情卡片
.regions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2.5rem;
  
  @media (max-width: 768px) {
    gap: 2rem;
  }
}

.region-card {
  background-color: white;
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-8px);
    box-shadow: var(--shadow-lg);
  }
  
  .region-img-container {
    height: 200px;
    overflow: hidden;
    
    .region-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.5s ease;
    }
    
    &:hover .region-img {
      transform: scale(1.1);
    }
  }
  
  .region-content {
    padding: 1.5rem;
    
    .region-name {
      font-size: 1.25rem;
      font-weight: 600;
      margin-bottom: 0.75rem;
      color: var(--text-primary);
    }
    
    .region-desc {
      color: var(--text-secondary);
      margin-bottom: 1rem;
      line-height: 1.6;
    }
    
    .region-stats {
      display: flex;
      gap: 1.5rem;
      
      .stat-item {
        font-size: 0.875rem;
        color: var(--text-secondary);
      }
    }
  }
}

// 文化传承故事
.stories-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
  
  @media (max-width: 992px) {
    grid-template-columns: 1fr;
    text-align: center;
  }
  
  .stories-image {
    border-radius: var(--border-radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-lg);
    
    img {
      width: 100%;
      height: auto;
      object-fit: cover;
    }
  }
  
  .stories-content {
    
    h3 {
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 1.5rem;
      color: var(--text-primary);
    }
    
    p {
      font-size: 1.125rem;
      line-height: 1.8;
      color: var(--text-secondary);
      margin-bottom: 2rem;
    }
  }
}

// 统计数据
.stats {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    text-align: center;
  }
  
  .stat-box {
    
    .stat-number {
      font-size: 3rem;
      font-weight: 800;
      margin-bottom: 0.5rem;
    }
    
    .stat-label {
      font-size: 1.125rem;
      opacity: 0.9;
    }
  }
}

// 视频卡片
.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2.5rem;
  
  @media (max-width: 768px) {
    gap: 2rem;
  }
}

.video-card {
  background-color: white;
  border-radius: var(--border-radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-8px);
    box-shadow: var(--shadow-lg);
  }
  
  .video-thumbnail {
    position: relative;
    height: 180px;
    cursor: pointer;
    overflow: hidden;
    
    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.5s ease;
    }
    
    .video-play-icon {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      color: var(--primary-color);
      opacity: 0.9;
      transition: all 0.3s ease;
    }
    
    &:hover img {
      transform: scale(1.1);
    }
    
    &:hover .video-play-icon {
      transform: translate(-50%, -50%) scale(1.1);
      opacity: 1;
    }
  }
  
  .video-info {
    padding: 1.5rem;
    
    .video-title {
      font-size: 1.125rem;
      font-weight: 600;
      margin-bottom: 0.5rem;
      color: var(--text-primary);
    }
    
    .video-duration {
      font-size: 0.875rem;
      color: var(--text-secondary);
    }
  }
}

// 订阅区域
.subscribe {
  background-color: var(--primary-light);
  
  .subscribe-content {
    text-align: center;
    max-width: 700px;
    margin: 0 auto;
    
    h2 {
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 1rem;
      color: var(--text-primary);
    }
    
    p {
      font-size: 1.125rem;
      color: var(--text-secondary);
      margin-bottom: 2rem;
    }
    
    .subscribe-form {
      display: flex;
      gap: 1rem;
      
      @media (max-width: 768px) {
        flex-direction: column;
      }
      
      input {
        flex: 1;
        padding: 1rem 1.5rem;
        border: none;
        border-radius: var(--border-radius-md);
        font-size: 1rem;
        box-shadow: var(--shadow-sm);
        
        &:focus {
          outline: none;
          box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1);
        }
      }
    }
  }
}

// 动画
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>