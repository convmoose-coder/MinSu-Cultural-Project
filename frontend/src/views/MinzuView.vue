<template>
  <div class="minzu-container">
    <header class="minzu-header">
      <h1>中国各民族文化展示</h1>
      <p>探索中华56个民族丰富多彩的文化遗产和传统</p>
    </header>
    
    <div class="minzu-content">
      <!-- 搜索和筛选区域 -->
      <div class="search-filter-section">
        <div class="search-bar">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="搜索民族文化..."
            class="search-input"
          />
          <button class="search-button">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
          </button>
        </div>
        

      </div>
      
      <!-- 民族文化卡片网格 -->
      <div class="minzu-grid">
        <div 
          v-for="ethnic in filteredEthnicGroups" 
          :key="ethnic.id"
          class="ethnic-card"
        >
          <div class="ethnic-image-container">
            <ModernImage 
              :src="ethnic.image" 
              :alt="ethnic.altText || ethnic.name"
              :default-src="'placeholder-culture.jpg'"
              fit="cover"
              :lazy="true"
            />
          </div>
          <div class="ethnic-info">
            <h3 class="ethnic-name">{{ ethnic.name }}</h3>
            <p class="ethnic-description">{{ ethnic.description }}</p>
            <div class="ethnic-tags">
              <span 
                v-for="tag in ethnic.tags" 
                :key="tag"
                class="ethnic-tag"
              >
                {{ tag }}
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 空状态提示 -->
      <div v-if="filteredEthnicGroups.length === 0" class="empty-state">
        <p>暂无符合条件的民族文化信息</p>
      </div>
    </div>
  </div>
</template>

<script>
import ModernImage from '../components/ModernImage.vue'

export default {
  name: 'MinzuView',
  components: {
    ModernImage
  },
  data() {
    return {
      searchQuery: '',
      ethnicGroups: [
        {
          id: 1,
          name: '汉族',
          description: '中华民族的主体民族，历史悠久，文化博大精深，对中华文化的发展做出了巨大贡献。',
          image: '/images/placeholder-culture.jpg',
          altText: '汉族文化代表',
          tags: ['农耕', '汉字', '诗词', '书法'],
          category: '农耕文化'
        },
        {
          id: 2,
          name: '蒙古族',
          description: '草原上的游牧民族，以其豪迈的性格和独特的草原文化著称。',
          image: '/images/folk-culture-bg.jpg',
          altText: '蒙古族草原文化',
          tags: ['游牧', '马头琴', '长调', '那达慕'],
          category: '草原文化'
        },
        {
          id: 3,
          name: '藏族',
          description: '高原上的民族，拥有独特的宗教文化和艺术传统。',
          image: '/images/culture-default-cover.jpg',
          altText: '藏族高原文化',
          tags: ['佛教', '唐卡', '藏戏', '酥油花'],
          category: '高原文化'
        },
        {
          id: 4,
          name: '维吾尔族',
          description: '新疆地区的主要民族，能歌善舞，有着丰富的音乐舞蹈文化。',
          image: '/images/placeholder-region.jpg',
          altText: '维吾尔族绿洲文化',
          tags: ['歌舞', '手鼓', '烤馕', '地毯'],
          category: '绿洲文化'
        },
        {
          id: 5,
          name: '彝族',
          description: '西南地区的古老民族，有着丰富多彩的节日和服饰文化。',
          image: '/images/traditional.jpg',
          altText: '彝族山地文化',
          tags: ['火把节', '漆器', '银饰', '阿诗玛'],
          category: '山地文化'
        },
        {
          id: 6,
          name: '壮族',
          description: '中国人口最多的少数民族，以壮族三月三歌圩节闻名。',
          image: '/images/placeholder-category.jpg',
          altText: '壮族水乡文化',
          tags: ['歌圩', '铜鼓', '壮锦', '刘三姐'],
          category: '水乡文化'
        },
        {
          id: 7,
          name: '回族',
          description: '分布广泛的少数民族，在饮食、宗教等方面有独特传统。',
          image: '/images/placeholder-culture.jpg',
          altText: '回族多元文化',
          tags: ['清真寺', '回族小吃', '伊斯兰文化'],
          category: '多元文化'
        },
        {
          id: 8,
          name: '满族',
          description: '中国历史上建立过清朝的少数民族，有着独特的旗人文化。',
          image: '/images/folk-culture-bg.jpg',
          altText: '满族东北文化',
          tags: ['旗袍', '满族舞蹈', '酸菜', '剪纸'],
          category: '东北文化'
        },
        {
          id: 9,
          name: '苗族',
          description: '以精美的银饰和丰富的民族节日著称的少数民族。',
          image: '/images/culture-default-cover.jpg',
          altText: '苗族山地文化',
          tags: ['银饰', '苗绣', '芦笙', '苗年'],
          category: '山地文化'
        },
        {
          id: 10,
          name: '土家族',
          description: '分布在湘鄂渝黔四省市的少数民族，有着独特的吊脚楼建筑。',
          image: '/images/placeholder-region.jpg',
          altText: '土家族山地文化',
          tags: ['吊脚楼', '摆手舞', '油茶', '织锦'],
          category: '山地文化'
        },
        {
          id: 11,
          name: '侗族',
          description: '擅长建筑艺术的少数民族，以鼓楼和风雨桥闻名。',
          image: '/images/traditional.jpg',
          altText: '侗族水乡文化',
          tags: ['鼓楼', '风雨桥', '大歌', '侗锦'],
          category: '水乡文化'
        },
        {
          id: 12,
          name: '瑶族',
          description: '分布广泛的少数民族，有着丰富的民间传说和习俗。',
          image: '/images/placeholder-category.jpg',
          altText: '瑶族山地文化',
          tags: ['盘王节', '长鼓舞', '刺绣', '油茶'],
          category: '山地文化'
        },
        {
          id: 13,
          name: '白族',
          description: '主要分布在云南大理的少数民族，以白族扎染和三道茶闻名。',
          image: '/images/placeholder-culture.jpg',
          altText: '白族高原文化',
          tags: ['扎染', '三道茶', '洱海', '白族民居'],
          category: '高原文化'
        },
        {
          id: 14,
          name: '哈尼族',
          description: '以梯田文化著称的少数民族，元阳梯田是其杰出代表。',
          image: '/images/folk-culture-bg.jpg',
          altText: '哈尼族山地文化',
          tags: ['梯田', '长街宴', '哈尼族服饰', '蘑菇房'],
          category: '山地文化'
        },
        {
          id: 15,
          name: '哈萨克族',
          description: '草原游牧民族，擅长骑马和冬不拉演奏。',
          image: '/images/culture-default-cover.jpg',
          altText: '哈萨克族草原文化',
          tags: ['游牧', '冬不拉', '阿肯弹唱', '叼羊'],
          category: '草原文化'
        }
      ]
    }
  },
  methods: {
    // ModernImage组件已有错误处理功能，无需单独处理
  },
  computed: {
    filteredEthnicGroups() {
      let result = this.ethnicGroups;
      
      // 按搜索词筛选
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(ethnic => 
          ethnic.name.toLowerCase().includes(query) ||
          ethnic.description.toLowerCase().includes(query) ||
          ethnic.tags.some(tag => tag.toLowerCase().includes(query))
        );
      }
      
      return result;
    }
  },
  mounted() {
    // 设置页面标题
    document.title = '乘灼文化';
  }
}
</script>

<style scoped>
.minzu-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.minzu-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 60px 20px;
  text-align: center;
}

.minzu-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  font-weight: 700;
}

.minzu-header p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.minzu-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.search-filter-section {
  margin-bottom: 40px;
  background: white;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.search-bar {
  display: flex;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 12px 20px;
  font-size: 16px;
  border: 2px solid #e1e5e9;
  border-radius: 8px 0 0 8px;
  outline: none;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #667eea;
}

.search-button {
  background: #667eea;
  color: white;
  border: none;
  padding: 0 20px;
  border-radius: 0 8px 8px 0;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-button:hover {
  background: #5a5fc7;
}



.minzu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 30px;
}

.ethnic-card {
  background: white;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.ethnic-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.ethnic-image-container {
  width: 100%;
  height: 250px; /* 固定高度确保图片显示 */
  overflow: hidden;
  position: relative;
  background-color: #f0f2f5;
  display: block;
  /* 确保子元素能正确填充 */
  
  /* 响应式设计 */
  @media (max-width: 768px) {
    height: 200px;
  }
  
  @media (max-width: 480px) {
    height: 180px;
  }
}

/* 确保ModernImage组件正确填充容器 */
.ethnic-image-container > .modern-image {
  width: 100% !important;
  height: 100% !important;
}

/* 确保图片元素正确填充父容器 */
.ethnic-image-container img {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  object-position: center !important;
  display: block !important;
  transition: transform 0.3s ease;
}

/* 悬停效果 */
.ethnic-card:hover .ethnic-image-container img {
  transform: scale(1.05);
}

.ethnic-info {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.ethnic-name {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #333;
}

.ethnic-description {
  color: #666;
  margin-bottom: 15px;
  line-height: 1.6;
  height: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.ethnic-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.ethnic-tag {
  background: #f0f2f5;
  color: #666;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  .minzu-header {
    padding: 40px 20px;
  }
  
  .minzu-header h1 {
    font-size: 2rem;
  }
  
  .minzu-grid {
    grid-template-columns: 1fr;
  }
  
  .search-filter-section {
    padding: 20px;
  }
}
</style>