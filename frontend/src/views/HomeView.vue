<template>
  <div class="home-view">
    <!-- 英雄区域 -->
    <section class="hero-section" ref="heroRef">
      <!-- 粒子背景 -->
      <div class="particles-container" ref="particlesRef"></div>
      
      <!-- 渐变背景 -->
      <div class="gradient-overlay"></div>
      
      <!-- 内容容器 -->
      <div class="hero-content">
        <div class="text-container">
          <h1 class="hero-title animate-fade-in-up">
            探索中国<span class="highlight">多元文化</span>
          </h1>
          <p class="hero-subtitle animate-fade-in-up-delay">
            深入了解中华民族丰富多样的地域文化与传统艺术
          </p>
          
          <!-- 按钮组 -->
          <div class="button-group animate-fade-in-up-delay-2">
            <modern-button 
              size="large" 
              variant="primary"
              @click="handleExplore"
            >
              开始探索
              <template #icon-right>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
              </template>
            </modern-button>
            
            <modern-button 
              size="large" 
              variant="outline"
              @click="handleViewGallery"
            >
              浏览图库
            </modern-button>
          </div>
        </div>
        
        <!-- 统计数据 -->
        <div class="stats-container animate-fade-in-up-delay-3">
          <div class="stat-item">
            <span class="stat-number">{{ statistics.regions || 0 }}</span>
            <span class="stat-label">地区</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ statistics.cultures || 0 }}</span>
            <span class="stat-label">文化</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ statistics.artworks || 0 }}</span>
            <span class="stat-label">艺术品</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">{{ statistics.stories || 0 }}</span>
            <span class="stat-label">故事</span>
          </div>
        </div>
      </div>
    </section>

    <!-- 民族文化展示区域 -->
    <section class="culture-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">
            <span class="title-decoration"></span>
            民族文化瑰宝
            <span class="title-decoration"></span>
          </h2>
          <p class="section-description">
            中国拥有56个民族，每个民族都有着独特而丰富的文化遗产
          </p>
        </div>
        
        <!-- 文化卡片网格 -->
        <div class="culture-grid">
          <culture-card
            v-for="(culture, index) in cultures"
            :key="culture.id || index"
            :id="culture.id"
            :title="culture.title"
            :subtitle="culture.subtitle"
            :image="culture.image"
            :description="culture.description"
            :category="culture.category"
            :tags="culture.tags"
            :created-at="culture.createdAt"
            :author="culture.author"
            :tag-color="culture.tagColor"
            @click="handleCultureClick(culture)"
            @action-click="handleCultureAction(culture)"
            @favorite-change="handleFavoriteChange"
          />
        </div>
        
        <!-- 查看更多按钮 -->
        <div class="view-more-container">
          <modern-button 
            size="medium" 
            variant="primary"
            @click="loadMoreCultures"
            :loading="loadingCultures"
          >
            查看更多民族文化
          </modern-button>
        </div>
      </div>
    </section>

    <!-- 地区风情展示区域 -->
    <section class="region-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">
            <span class="title-decoration"></span>
            地区风情特色
            <span class="title-decoration"></span>
          </h2>
          <p class="section-description">
            不同地域孕育出各具特色的文化传统和生活方式
          </p>
        </div>
        
        <!-- 地区卡片网格 -->
        <div class="region-grid">
          <region-card
            v-for="(region, index) in regions"
            :key="region.id || index"
            :id="region.id"
            :title="region.title"
            :subtitle="region.subtitle"
            :image="region.image"
            :stats="region.stats"
            :tags="region.tags"
            :gradient-start-color="region.gradientStart"
            :gradient-end-color="region.gradientEnd"
            :gradient-direction="region.gradientDirection || 'bottom'"
            :content-position="region.contentPosition || 'bottom'"
            @click="handleRegionClick(region)"
            @action-click="handleRegionAction(region)"
          />
        </div>
        
        <!-- 探索更多按钮 -->
        <div class="view-more-container">
          <modern-button 
            size="medium" 
            variant="secondary"
            @click="exploreMoreRegions"
            :loading="loadingRegions"
          >
            探索更多地区文化
          </modern-button>
        </div>
      </div>
    </section>

    <!-- 文化展示区域 -->
    <section class="showcase-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">
            <span class="title-decoration"></span>
            文化精选展示
            <span class="title-decoration"></span>
          </h2>
          <p class="section-description">
            精选中国传统文化艺术作品和非物质文化遗产
          </p>
        </div>
        
        <!-- 展示网格 -->
        <div class="showcase-grid">
          <div v-for="(item, index) in showcaseItems" :key="item.id || index" class="showcase-card">
            <img
              :src="item.image"
              :alt="item.title"
              class="showcase-image"
            />
            <div class="showcase-content">
              <h3 class="showcase-title">{{ item.title }}</h3>
              <p class="showcase-category">{{ item.category }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>


  </div>
</template>

<script>
import ModernButton from '../components/ModernButton.vue'
import CultureCard from '../components/CultureCard.vue'
import RegionCard from '../components/RegionCard.vue'

export default {
  name: 'HomeView',
  components: {
    'modern-button': ModernButton,
    'culture-card': CultureCard,
    'region-card': RegionCard
  },
  data() {
    return {
      // 粒子背景引用
      heroRef: null,
      particlesRef: null,
      particles: [],
      
      // 统计数据
      statistics: {
        regions: 34,
        cultures: 56,
        artworks: 1200,
        stories: 5000
      },
      
      // 民族文化数据
      cultures: [],
      loadingCultures: false,
      
      // 地区数据
      regions: [],
      loadingRegions: false,
      
      // 展示数据
      showcaseItems: [],
      

    }
  },
  mounted() {
    this.initializeParticles();
    this.loadInitialData();
  },
  beforeUnmount() {
    this.destroyParticles();
  },
  methods: {
    // 加载初始数据
    async loadInitialData() {
      try {
        // 尝试从API加载数据，如果失败则使用默认数据
        await Promise.all([
          this.fetchCultures().catch(() => this.setDefaultCultures()),
          this.fetchRegions().catch(() => this.setDefaultRegions()),
          this.fetchShowcaseItems().catch(() => this.setDefaultShowcaseItems())
        ]);
      } catch (error) {
        console.error('加载数据失败:', error);
        // 确保使用默认数据
        this.setDefaultCultures();
        this.setDefaultRegions();
        this.setDefaultShowcaseItems();
      }
    },
    
    // 获取民族文化数据
    async fetchCultures() {
      // 模拟API调用
      throw new Error('API不可用'); // 触发默认数据加载
    },
    
    // 获取地区数据
    async fetchRegions() {
      // 模拟API调用
      throw new Error('API不可用'); // 触发默认数据加载
    },
    
    // 获取展示数据
    async fetchShowcaseItems() {
      // 模拟API调用
      throw new Error('API不可用'); // 触发默认数据加载
    },
    
    // 设置默认民族文化数据
    setDefaultCultures() {
      // 确保cultures数组存在
      if (!this.cultures) {
        this.cultures = [];
      }
      
      // 添加丰富的民族文化数据
      this.cultures = [
        {
          id: '1',
          title: '藏族文化',
          subtitle: '雪域高原的神秘文明',
          image: 'frontend/src/assets/images/traditional.jpg',
          description: '藏族文化是中国传统文化的重要组成部分，拥有悠久的历史和丰富的内涵。从藏传佛教到传统艺术，从民间习俗到建筑风格，都展现出独特的魅力。',
          category: '高原文化',
          tags: ['宗教', '艺术', '习俗', '建筑'],
          tagColor: '#E91E63',
          createdAt: '2024-01-15',
          author: '文化研究中心',
          popularity: 98
        },
        {
          id: '2',
          title: '彝族文化',
          subtitle: '火的民族的热情文化',
          image: 'frontend/src/assets/images/traditional.jpg',
          description: '彝族是中国第六大少数民族，有着深厚的文化底蕴。火把节是彝族最盛大的传统节日，展现了彝族人民对火的崇拜和对生活的热爱。',
          category: '山地文化',
          tags: ['节日', '音乐', '舞蹈', '服饰'],
          tagColor: '#FF5722',
          createdAt: '2024-01-10',
          author: '民族文化协会',
          popularity: 92
        },
        {
          id: '3',
          title: '傣族文化',
          subtitle: '水的民族的灵动艺术',
          image: 'frontend/src/assets/images/traditional.jpg',
          description: '傣族主要分布在云南地区，有着独特的水文化。泼水节是傣族的传统节日，象征着洗去污垢和祝福。傣族的孔雀舞和象脚鼓舞闻名中外。',
          category: '水乡文化',
          tags: ['水文化', '舞蹈', '节日', '音乐'],
          tagColor: '#03A9F4',
          createdAt: '2024-01-08',
          author: '云南文化研究',
          popularity: 95
        },
        {
          id: '4',
          title: '维吾尔族文化',
          subtitle: '丝路明珠的多元文化',
          image: 'frontend/src/assets/images/traditional.jpg',
          description: '维吾尔族文化融合了东西方文明的精华，以其绚丽多彩的歌舞艺术、精美的手工艺品和独特的饮食文化而闻名。',
          category: '丝路文化',
          tags: ['音乐', '舞蹈', '手工艺', '美食'],
          tagColor: '#4CAF50',
          createdAt: '2024-01-05',
          author: '新疆文化研究',
          popularity: 88
        },
        {
          id: '5',
          title: '蒙古族文化',
          subtitle: '草原文化的豪迈风情',
          image: 'frontend/src/assets/images/traditional.jpg',
          description: '蒙古族有着悠久的历史和丰富的文化遗产，那达慕大会、马头琴、长调民歌等都是蒙古族文化的重要组成部分。',
          category: '草原文化',
          tags: ['音乐', '体育', '文学', '服饰'],
          tagColor: '#FF9800',
          createdAt: '2024-01-01',
          author: '草原文化协会',
          popularity: 90
        },
        {
          id: '6',
          title: '汉族传统文化',
          subtitle: '华夏文明的深厚底蕴',
          image: 'frontend/src/assets/images/traditional.jpg',
          description: '汉族文化是中华文明的主体，拥有五千年的悠久历史，包括儒家思想、汉服文化、传统节日等丰富多彩的文化元素。',
          category: '华夏文化',
          tags: ['哲学', '文学', '节日', '服饰'],
          tagColor: '#2196F3',
          createdAt: '2023-12-28',
          author: '中国传统文化研究会',
          popularity: 97
        }
      ];
    },
    
    // 设置默认地区数据
    setDefaultRegions() {
      this.regions = [
        {
          id: '1',
          title: '江南水乡',
          subtitle: '小桥流水人家',
          image: '/images/placeholder-region.jpg',
          stats: {
            attractions: 156,
            cultures: 48
          },
          tags: ['水乡', '园林', '古镇', '吴文化'],
          gradientStart: 'rgba(156, 39, 176, 0.8)',
          gradientEnd: 'rgba(0, 188, 212, 0.3)',
          gradientDirection: 'bottom',
          contentPosition: 'bottom'
        },
        {
          id: '2',
          title: '塞北草原',
          subtitle: '天苍苍野茫茫',
          image: '/images/placeholder-region.jpg',
          stats: {
            area: 400000,
            cultures: 24
          },
          tags: ['草原', '游牧', '蒙古包', '马头琴'],
          gradientStart: 'rgba(233, 30, 99, 0.8)',
          gradientEnd: 'rgba(255, 152, 0, 0.3)',
          gradientDirection: 'bottom',
          contentPosition: 'bottom'
        },
        {
          id: '3',
          title: '西南山地',
          subtitle: '多彩民族文化',
          image: '/images/placeholder-region.jpg',
          stats: {
            cultures: 30,
            attractions: 89
          },
          tags: ['山地', '少数民族', '梯田', '民俗'],
          gradientStart: 'rgba(76, 175, 80, 0.8)',
          gradientEnd: 'rgba(139, 195, 74, 0.3)',
          gradientDirection: 'bottom',
          contentPosition: 'bottom'
        }
      ];
    },
    
    // 设置默认展示数据
    setDefaultShowcaseItems() {
      this.showcaseItems = [
        {
          id: '1',
          title: '传统绘画',
          category: '艺术形式',
          image: '/images/placeholder-category.jpg'
        },
        {
          id: '2',
          title: '民间工艺',
          category: '手工艺术',
          image: '/images/placeholder-category.jpg'
        },
        {
          id: '3',
          title: '戏曲艺术',
          category: '表演艺术',
          image: '/images/placeholder-category.jpg'
        },
        {
          id: '4',
          title: '传统建筑',
          category: '建筑艺术',
          image: '/images/placeholder-category.jpg'
        },
        {
          id: '5',
          title: '传统音乐',
          category: '音乐艺术',
          image: '/images/placeholder-category.jpg'
        },
        {
          id: '6',
          title: '传统舞蹈',
          category: '舞蹈艺术',
          image: '/images/placeholder-category.jpg'
        }
      ];
    },
    
    // 跳转到所有民族文化页面
    loadMoreCultures() {
      // 使用路由跳转到/minzu路径
      this.$router.push('/minzu');
    },
    
    // 探索更多地区
    async exploreMoreRegions() {
      this.loadingRegions = true;
      try {
        // 模拟加载延迟
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // 添加更多默认数据
        const moreRegions = [
          {
            id: '4',
            title: '岭南风情',
            subtitle: '开放包容的海洋文化',
            image: '/images/placeholder-region.jpg',
            stats: {
              attractions: 134,
              cultures: 28
            },
            tags: ['岭南', '粤菜', '骑楼', '侨乡'],
            gradientStart: 'rgba(255, 193, 7, 0.8)',
            gradientEnd: 'rgba(255, 87, 34, 0.3)',
            gradientDirection: 'bottom',
            contentPosition: 'bottom'
          },
          {
            id: '5',
            title: '西北大漠',
            subtitle: '丝绸之路的文明交汇',
            image: '/images/placeholder-region.jpg',
            stats: {
              history: 2000,
              cultures: 35
            },
            tags: ['沙漠', '丝路', '石窟', '绿洲'],
            gradientStart: 'rgba(121, 85, 72, 0.8)',
            gradientEnd: 'rgba(229, 194, 152, 0.3)',
            gradientDirection: 'bottom',
            contentPosition: 'bottom'
          }
        ];
        
        this.regions = [...this.regions, ...moreRegions];
      } catch (error) {
        console.error('加载更多地区数据失败:', error);
      } finally {
        this.loadingRegions = false;
      }
    },
    
    // 处理探索按钮点击
    handleExplore() {
      console.log('开始探索');
    },
    
    // 处理浏览图库按钮点击
    handleViewGallery() {
      console.log('浏览图库');
    },
    
    // 处理文化卡片点击
    handleCultureClick(culture) {
      console.log('点击文化卡片:', culture.title);
    },
    
    // 处理文化卡片操作
    handleCultureAction(culture) {
      console.log('文化卡片操作:', culture.title);
    },
    
    // 处理收藏状态变化
    handleFavoriteChange(data) {
      console.log('收藏状态变化:', data);
    },
    
    // 处理地区卡片点击
    handleRegionClick(region) {
      console.log('点击地区卡片:', region.title);
    },
    
    // 处理地区卡片操作
    handleRegionAction(region) {
      console.log('地区卡片操作:', region.title);
    },
    

    
    // 初始化粒子背景
    initializeParticles() {
      if (!this.$refs.particlesRef) return;
      
      const count = 50;
      const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];
      
      for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        // 随机样式
        const size = Math.random() * 10 + 5;
        const color = colors[Math.floor(Math.random() * colors.length)];
        const opacity = Math.random() * 0.5 + 0.1;
        
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.backgroundColor = color;
        particle.style.opacity = opacity;
        particle.style.position = 'absolute';
        particle.style.borderRadius = '50%';
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.animationDuration = `${Math.random() * 30 + 20}s`;
        particle.style.animationDelay = `${Math.random() * 10}s`;
        particle.style.transform = 'translateY(0)';
        
        this.$refs.particlesRef.appendChild(particle);
        this.particles.push(particle);
      }
    },
    
    // 销毁粒子背景
    destroyParticles() {
      this.particles.forEach(particle => {
        if (particle.parentNode) {
          particle.parentNode.removeChild(particle);
        }
      });
      this.particles = [];
    }
  }
}
</script>

<style lang="scss" scoped>
.home-view {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  color: #111827;
  overflow-x: hidden;
}

/* 英雄区域样式 */
.hero-section {
  position: relative;
  height: 100vh;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  overflow: hidden;
  background-color: #0f172a;

  .particles-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    overflow: hidden;
  }

  .particle {
    animation: float linear infinite;
  }

  .gradient-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      135deg,
      rgba(15, 23, 42, 0.8) 0%,
      rgba(30, 58, 138, 0.8) 50%,
      rgba(15, 23, 42, 0.8) 100%
    );
  }

  .hero-content {
    position: relative;
    z-index: 10;
    width: 100%;
    max-width: 1200px;
    padding: 0 2rem;
  }

  .text-container {
    margin-bottom: 3rem;
  }

  .hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    line-height: 1.2;
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);

    .highlight {
      color: #60a5fa;
      position: relative;
      
      &::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        border-radius: 2px;
      }
    }
  }

  .hero-subtitle {
    font-size: 1.25rem;
    margin-bottom: 2.5rem;
    opacity: 0.9;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }

  .button-group {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
  }

  .stats-container {
    display: flex;
    justify-content: center;
    gap: 3rem;
    flex-wrap: wrap;
    margin-top: 4rem;
    padding: 2rem;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 120px;
  }

  .stat-number {
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1;
    background: linear-gradient(45deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .stat-label {
    font-size: 0.875rem;
    opacity: 0.8;
    margin-top: 0.5rem;
  }
}

/* 通用区块样式 */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  position: relative;
  display: inline-block;
  color: #1e293b;

  .title-decoration {
    display: inline-block;
    width: 30px;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    vertical-align: middle;
    margin: 0 1rem;
    border-radius: 1.5px;
  }
}

.section-description {
  font-size: 1.125rem;
  color: #64748b;
  max-width: 700px;
  margin: 0 auto;
}

.view-more-container {
  text-align: center;
  margin-top: 3rem;
}

/* 民族文化区块样式 */
.culture-section {
  padding: 6rem 0;
  background-color: #f8fafc;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100px;
    background: linear-gradient(to bottom, #0f172a, transparent);
    opacity: 0.1;
  }

  .culture-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
  }
}

/* 地区风情区块样式 */
.region-section {
  padding: 6rem 0;
  background-color: #ffffff;
  position: relative;

  .region-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
  }
}

/* 文化展示区块样式 */
.showcase-section {
  padding: 6rem 0;
  background-color: #0f172a;
  color: white;

  .section-title {
    color: white;
  }

  .section-description {
    color: #94a3b8;
  }

  .showcase-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
  }

  .showcase-card {
    border-radius: 0.75rem;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.05);
    transition: transform 0.3s ease, background-color 0.3s ease;
    cursor: pointer;

    &:hover {
      transform: translateY(-5px);
      background: rgba(255, 255, 255, 0.1);
    }
  }

  .showcase-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }

  .showcase-content {
    padding: 1.5rem;
  }

  .showcase-title {
    font-size: 1.25rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
  }

  .showcase-category {
    font-size: 0.875rem;
    color: #94a3b8;
    margin: 0;
  }
}

/* 联系我们区块样式 */
.contact-section {
  padding: 6rem 0;
  background-color: #f8fafc;

  .contact-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
    align-items: start;
  }

  .contact-info {
    background-color: white;
    padding: 2.5rem;
    border-radius: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }

  .contact-title {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 1rem;
    color: #1e293b;
  }

  .contact-description {
    font-size: 1.125rem;
    color: #64748b;
    margin-bottom: 2rem;
  }

  .contact-details {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .contact-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    color: #334155;
  }

  .contact-form {
    background-color: white;
    padding: 2.5rem;
    border-radius: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  }

  .form-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    color: #1e293b;
  }

  .form-group {
    margin-bottom: 1.5rem;
  }

  .form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #334155;
  }

  .form-group input,
  .form-group textarea {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    font-size: 1rem;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;

    &:focus {
      outline: none;
      border-color: #3b82f6;
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
  }

  .form-group textarea {
    resize: vertical;
    min-height: 100px;
  }
}

/* 动画效果 */
@keyframes float {
  0% {
    transform: translateY(0) translateX(0);
  }
  25% {
    transform: translateY(-20px) translateX(10px);
  }
  50% {
    transform: translateY(0) translateX(20px);
  }
  75% {
    transform: translateY(20px) translateX(10px);
  }
  100% {
    transform: translateY(0) translateX(0);
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

.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
}

.animate-fade-in-up-delay {
  animation: fadeInUp 0.6s ease-out 0.2s forwards;
  opacity: 0;
}

.animate-fade-in-up-delay-2 {
  animation: fadeInUp 0.6s ease-out 0.4s forwards;
  opacity: 0;
}

.animate-fade-in-up-delay-3 {
  animation: fadeInUp 0.6s ease-out 0.6s forwards;
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .hero-title {
    font-size: 2.75rem;
  }

  .stats-container {
    gap: 2rem;
  }

  .stat-item {
    min-width: 100px;
  }

  .stat-number {
    font-size: 2rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .contact-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero-section {
    height: auto;
    min-height: 100vh;
    padding: 8rem 0;
  }

  .hero-title {
    font-size: 2.25rem;
  }

  .hero-subtitle {
    font-size: 1.125rem;
  }

  .button-group {
    flex-direction: column;
    align-items: center;
  }

  .stats-container {
    flex-direction: column;
    gap: 1.5rem;
    padding: 1.5rem;
  }

  .stat-item {
    min-width: auto;
  }

  .section-header {
    margin-bottom: 3rem;
  }

  .section-title {
    font-size: 1.75rem;
  }

  .section-title .title-decoration {
    display: none;
  }

  .section-description {
    font-size: 1rem;
  }

  .culture-section,
  .region-section,
  .showcase-section,
  .contact-section {
    padding: 4rem 0;
  }

  .culture-grid,
  .region-grid,
  .showcase-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .contact-info,
  .contact-form {
    padding: 1.5rem;
  }

  .contact-title {
    font-size: 1.75rem;
  }

  .form-title {
    font-size: 1.25rem;
  }
}

@media (max-width: 480px) {
  .hero-content {
    padding: 0 1rem;
  }

  .hero-title {
    font-size: 1.75rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .container {
    padding: 0 1rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .contact-details {
    gap: 1rem;
  }

  .contact-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}

/* 深色模式适配 */
@media (prefers-color-scheme: dark) {
  .home-view {
    color: #f8fafc;
  }

  .culture-section,
  .contact-section {
    background-color: #0f172a;
  }

  .region-section {
    background-color: #1e293b;
  }

  .section-title {
    color: #f8fafc;
  }

  .section-description {
    color: #94a3b8;
  }

  .contact-info,
  .contact-form {
    background-color: #1e293b;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
  }

  .contact-title,
  .form-title {
    color: #f8fafc;
  }

  .contact-description {
    color: #94a3b8;
  }

  .contact-item {
    color: #cbd5e1;
  }

  .form-group label {
    color: #cbd5e1;
  }

  .form-group input,
  .form-group textarea {
    background-color: #0f172a;
    border-color: #334155;
    color: #f8fafc;

    &:focus {
      border-color: #60a5fa;
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
    }
  }
}
</style>