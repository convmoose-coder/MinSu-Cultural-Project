<template>
  <div class="culture-list-view">
    <!-- 页面头部 -->
    <section class="page-header">
      <div class="container">
        <h1 class="page-title">乘灼列表</h1>
        <p class="page-description">探索中华民族多元文化，传承千年文明瑰宝</p>
      </div>
    </section>

    <!-- 筛选和搜索区域 -->
    <section class="filter-section">
      <div class="container">
        <div class="filter-content">
          <div class="search-box">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="搜索民族或文化内容..."
              class="search-input"
            >
            <button class="search-button" aria-label="搜索">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 21L16.65 16.65M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
            </button>
          </div>
          <div class="filter-group">
            <select v-model="selectedRegion" class="filter-select"
                      @change="resetPagination"
            >
              <option value="">全部地区</option>
              <option value="东北">东北地区</option>
              <option value="华北">华北地区</option>
              <option value="西北">西北地区</option>
              <option value="西南">西南地区</option>
              <option value="中南">中南地区</option>
              <option value="华东">华东地区</option>
              <option value="港澳台">港澳台地区</option>
            </select>
            <select v-model="selectedCategory" class="filter-select"
                      @change="resetPagination"
            >
              <option value="">全部类别</option>
              <option value="传统艺术">传统艺术</option>
              <option value="民俗节日">民俗节日</option>
              <option value="饮食习惯">饮食习惯</option>
              <option value="服饰文化">服饰文化</option>
              <option value="建筑特色">建筑特色</option>
              <option value="民间传说">民间传说</option>
            </select>
          </div>
        </div>
      </div>
    </section>

    <!-- 文化列表区域 -->
    <section class="culture-list-section">
      <div class="container">
        <div class="culture-grid">
          <div 
            v-for="culture in filteredCultures" 
            :key="culture.id"
            class="culture-card"
          >
            <router-link :to="`/cultures/${culture.id}`" class="culture-link">
              <div class="culture-image-container">
                <img :src="culture.imageUrl" :alt="culture.name" class="culture-image">
                <div class="culture-tag">{{ culture.region }}</div>
              </div>
              <div class="culture-content">
                <h3 class="culture-name">{{ culture.name }}</h3>
                <div class="culture-meta">
                  <span class="culture-category">{{ culture.category }}</span>
                  <span class="culture-time">{{ culture.updatedAt }}</span>
                </div>
                <p class="culture-description">{{ culture.description.substring(0, 120) }}...</p>
                <div class="culture-footer">
                  <span class="read-more">查看详情 ></span>
                  <div class="culture-stats">
                    <span class="stat-item">
                      <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 4.5C7 4.5 2.73 7.61 1 12C2.73 16.39 7 19.5 12 19.5C17 19.5 21.27 16.39 23 12C21.27 7.61 17 4.5 12 4.5ZM12 17C9.24 17 7 14.76 7 12C7 9.24 9.24 7 12 7C14.76 7 17 9.24 17 12C17 14.76 14.76 17 12 17ZM12 9.5C10.62 9.5 9.5 10.62 9.5 12C9.5 13.38 10.62 14.5 12 14.5C13.38 14.5 14.5 13.38 14.5 12C14.5 10.62 13.38 9.5 12 9.5Z" fill="currentColor" />
                      </svg>
                      {{ culture.views }}
                    </span>
                  </div>
                </div>
              </div>
            </router-link>
          </div>
        </div>

        <!-- 无数据提示 -->
        <div v-if="filteredCultures.length === 0" class="no-data">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 17V19M12 5V7M19 12H17M5 12H7M16.97 7.03L18.41 8.47M5.59 15.53L7.03 16.97M16.97 16.97L18.41 15.53M5.59 8.47L7.03 7.03M12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
          </svg>
          <p>暂无符合条件的文化内容</p>
        </div>

        <!-- 分页控制 -->
        <div v-if="filteredCultures.length > 0" class="pagination">
          <button 
            @click="currentPage--" 
            :disabled="currentPage === 1"
            class="pagination-button"
          >上一页</button>
          <span class="pagination-info">第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
          <button 
            @click="currentPage++" 
            :disabled="currentPage === totalPages"
            class="pagination-button"
          >下一页</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// 响应式数据
const searchQuery = ref('');
const selectedRegion = ref('');
const selectedCategory = ref('');
const currentPage = ref(1);
const itemsPerPage = 12;

// 模拟数据 - 实际项目中应从API获取
const cultures = ref([
  {
    id: 1,
    name: '藏族锅庄舞',
    region: '西南',
    category: '传统艺术',
    description: '锅庄舞是藏族最具代表性的民间舞蹈之一，集歌、舞、乐于一体，节奏明快，动作刚健有力。每到节日庆典，人们身着盛装，围绕篝火载歌载舞，表达对生活的热爱和对未来的美好向往。',
    imageUrl: '/assets/images/tibetan-dance.jpg',
    views: 1245,
    updatedAt: '2024-01-15'
  },
  {
    id: 2,
    name: '蒙古族那达慕大会',
    region: '西北',
    category: '民俗节日',
    description: '那达慕大会是蒙古族传统的节日盛会，"那达慕"在蒙古语中意为"娱乐、游戏"。大会期间举行赛马、摔跤、射箭等传统体育比赛，还有精彩的歌舞表演和物资交流活动。',
    imageUrl: '/assets/images/mongolian-nadamu.jpg',
    views: 987,
    updatedAt: '2024-01-12'
  },
  {
    id: 3,
    name: '维吾尔族十二木卡姆',
    region: '西北',
    category: '传统艺术',
    description: '十二木卡姆是维吾尔族的大型传统音乐套曲，被誉为"东方音乐的瑰宝"。它集音乐、舞蹈、诗歌于一体，展现了维吾尔族人民的智慧和创造力，2005年被联合国教科文组织列入世界非物质文化遗产名录。',
    imageUrl: '/assets/images/uyghur-mukam.jpg',
    views: 1567,
    updatedAt: '2024-01-10'
  },
  {
    id: 4,
    name: '彝族火把节',
    region: '西南',
    category: '民俗节日',
    description: '火把节是彝族最隆重的传统节日，通常在农历六月二十四举行。这一天，人们点燃火把，载歌载舞，驱邪祈福。火把节还有斗牛、赛马、摔跤等传统活动，充满了浓厚的民族特色。',
    imageUrl: '/assets/images/yi-torch-festival.jpg',
    views: 2134,
    updatedAt: '2024-01-08'
  },
  {
    id: 5,
    name: '傣族泼水节',
    region: '西南',
    category: '民俗节日',
    description: '泼水节是傣族的新年节日，通常在公历4月中旬举行。节日期间，人们相互泼水祝福，象征着洗去过去一年的污垢和晦气，迎来新的一年。此外还有划龙舟、放高升、赶摆等丰富多彩的活动。',
    imageUrl: '/assets/images/dai-water-festival.jpg',
    views: 1876,
    updatedAt: '2024-01-05'
  },
  {
    id: 6,
    name: '汉族春节',
    region: '全国',
    category: '民俗节日',
    description: '春节是中华民族最重要的传统节日，象征着团圆、喜庆和新的开始。从腊月二十三的小年开始，到正月十五的元宵节结束，期间有贴春联、吃团圆饭、守岁、拜年等丰富多彩的民俗活动。',
    imageUrl: '/assets/images/spring-festival.jpg',
    views: 3421,
    updatedAt: '2024-01-01'
  },
  {
    id: 7,
    name: '朝鲜族跳板',
    region: '东北',
    category: '传统艺术',
    description: '跳板是朝鲜族传统的体育游戏，尤其受到朝鲜族妇女的喜爱。游戏时，两人分别站在跳板两端，轮流起跳，在空中做出各种优美的动作。跳板运动不仅展示了朝鲜族人民的勇敢和灵巧，也体现了他们对美好生活的追求。',
    imageUrl: '/assets/images/korean-board-jumping.jpg',
    views: 876,
    updatedAt: '2023-12-28'
  },
  {
    id: 8,
    name: '回族开斋节',
    region: '全国',
    category: '民俗节日',
    description: '开斋节是回族等穆斯林群众的重要节日，在伊斯兰教历十月一日举行。这一天，穆斯林们早早起床，沐浴更衣，前往清真寺参加会礼，然后走亲访友，互道祝福。开斋节期间，还会准备丰盛的美食，如油香、馓子等。',
    imageUrl: '/assets/images/eid-al-fitr.jpg',
    views: 1123,
    updatedAt: '2023-12-25'
  },
  {
    id: 9,
    name: '壮族三月三歌圩节',
    region: '中南',
    category: '民俗节日',
    description: '三月三歌圩节是壮族的传统节日，也被称为"歌仙节"。这一天，壮族人民会举行盛大的对歌活动，青年男女通过对歌来传情达意。此外还有抛绣球、碰彩蛋、抢花炮等特色活动，充满了浓厚的民族风情。',
    imageUrl: '/assets/images/zhuang-singing-festival.jpg',
    views: 987,
    updatedAt: '2023-12-22'
  },
  {
    id: 10,
    name: '侗族大歌',
    region: '中南',
    category: '传统艺术',
    description: '侗族大歌是侗族的多声部无伴奏合唱，被誉为"天籁之音"。它以其独特的和声结构和演唱方式闻名于世，2009年被列入联合国教科文组织人类非物质文化遗产代表作名录。侗族大歌内容丰富，涵盖了侗族人民的历史、生活和情感。',
    imageUrl: '/assets/images/dong-grand-chorus.jpg',
    views: 1456,
    updatedAt: '2023-12-20'
  },
  {
    id: 11,
    name: '满族旗袍',
    region: '东北',
    category: '服饰文化',
    description: '旗袍是满族的传统服饰，经过演变已经成为中华服饰文化的重要符号。旗袍以其修身的剪裁、精美的刺绣和独特的韵味而闻名，展现了东方女性的优雅和魅力。如今，旗袍已经成为中国传统服饰的代表，在各种重要场合广泛穿着。',
    imageUrl: '/assets/images/manchu-qipao.jpg',
    views: 2341,
    updatedAt: '2023-12-18'
  },
  {
    id: 12,
    name: '土家族摆手舞',
    region: '中南',
    category: '传统艺术',
    description: '摆手舞是土家族最有代表性的民间舞蹈，动作优美大方，节奏明快。舞蹈内容多反映土家族人民的生产生活和历史传说，表达了他们对自然的崇拜和对美好生活的向往。摆手舞通常在摆手堂或广场上表演，参与者众多，场面热烈。',
    imageUrl: '/assets/images/tujia-hand-dance.jpg',
    views: 765,
    updatedAt: '2023-12-15'
  },
  {
    id: 13,
    name: '哈萨克族阿肯弹唱',
    region: '西北',
    category: '传统艺术',
    description: '阿肯弹唱是哈萨克族的传统民间艺术形式，"阿肯"是哈萨克族对民间歌手的称呼。阿肯们怀抱冬不拉，即兴创作诗歌，歌颂英雄、赞美爱情、描绘草原风光。阿肯弹唱不仅是一种艺术表演，也是哈萨克族人民传承历史文化的重要方式。',
    imageUrl: '/assets/images/kazakh-akyn.jpg',
    views: 654,
    updatedAt: '2023-12-12'
  },
  {
    id: 14,
    name: '白族三月街',
    region: '西南',
    category: '民俗节日',
    description: '三月街是白族的传统节日，每年农历三月十五日至二十日在云南大理举行。这是一个集商贸、文化、娱乐于一体的盛会，有赛马、射箭、歌舞表演等活动，还有各种特色商品交易。三月街历史悠久，是白族人民交流感情、传承文化的重要平台。',
    imageUrl: '/assets/images/baizu-march-fair.jpg',
    views: 890,
    updatedAt: '2023-12-10'
  }
]);

// 计算属性
const filteredCultures = computed(() => {
  let result = cultures.value.filter(culture => {
    const matchesSearch = culture.name.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                         culture.description.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesRegion = !selectedRegion.value || culture.region === selectedRegion.value || culture.region === '全国';
    const matchesCategory = !selectedCategory.value || culture.category === selectedCategory.value;
    
    return matchesSearch && matchesRegion && matchesCategory;
  });
  
  // 分页逻辑
  const startIndex = (currentPage.value - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  return result.slice(startIndex, endIndex);
});

const totalPages = computed(() => {
  let filtered = cultures.value.filter(culture => {
    const matchesSearch = culture.name.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                         culture.description.toLowerCase().includes(searchQuery.value.toLowerCase());
    const matchesRegion = !selectedRegion.value || culture.region === selectedRegion.value || culture.region === '全国';
    const matchesCategory = !selectedCategory.value || culture.category === selectedCategory.value;
    
    return matchesSearch && matchesRegion && matchesCategory;
  });
  
  return Math.ceil(filtered.length / itemsPerPage);
});

// 方法
function resetPagination() {
  currentPage.value = 1;
}

// 监听搜索查询变化
watch(searchQuery, () => {
  resetPagination();
});

// 页面挂载时重置分页
onMounted(() => {
  currentPage.value = 1;
});
</script>

<style lang="scss">
.culture-list-view {
  
  // 页面头部样式
  .page-header {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white;
    padding: 3rem 0;
    text-align: center;
    
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 1.5rem;
    }
    
    .page-title {
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: 1rem;
    }
    
    .page-description {
      font-size: 1.25rem;
      opacity: 0.9;
    }
    
    @media (max-width: 768px) {
      padding: 2rem 0;
      
      .page-title {
        font-size: 2rem;
      }
      
      .page-description {
        font-size: 1rem;
      }
    }
  }
  
  // 筛选区域样式
  .filter-section {
    background-color: #f8f9fa;
    padding: 2rem 0;
    
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 1.5rem;
    }
    
    .filter-content {
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
      
      @media (min-width: 768px) {
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
      }
    }
    
    .search-box {
      position: relative;
      max-width: 400px;
      width: 100%;
      
      .search-input {
        width: 100%;
        padding: 0.75rem 2.5rem 0.75rem 1rem;
        border: 1px solid var(--border-color);
        border-radius: 0.375rem;
        font-size: 1rem;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        
        &:focus {
          outline: none;
          border-color: var(--primary-color);
          box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.1);
        }
      }
      
      .search-button {
        position: absolute;
        right: 0.5rem;
        top: 50%;
        transform: translateY(-50%);
        background: none;
        border: none;
        color: var(--text-secondary);
        cursor: pointer;
        padding: 0.5rem;
        transition: color 0.3s ease;
        
        &:hover {
          color: var(--primary-color);
        }
        
        svg {
          width: 1.25rem;
          height: 1.25rem;
        }
      }
    }
    
    .filter-group {
      display: flex;
      gap: 1rem;
      flex-wrap: wrap;
      
      .filter-select {
        padding: 0.75rem 1rem;
        border: 1px solid var(--border-color);
        border-radius: 0.375rem;
        font-size: 1rem;
        background-color: white;
        cursor: pointer;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
        
        &:focus {
          outline: none;
          border-color: var(--primary-color);
          box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.1);
        }
      }
    }
  }
  
  // 文化列表区域样式
  .culture-list-section {
    padding: 3rem 0;
    
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 1.5rem;
    }
    
    .culture-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 2rem;
      margin-bottom: 2rem;
      
      @media (min-width: 640px) {
        grid-template-columns: repeat(2, 1fr);
      }
      
      @media (min-width: 992px) {
        grid-template-columns: repeat(3, 1fr);
      }
    }
    
    .culture-card {
      background-color: white;
      border-radius: 0.5rem;
      overflow: hidden;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      
      &:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
      }
      
      .culture-link {
        text-decoration: none;
        color: var(--text-primary);
        display: block;
      }
      
      .culture-image-container {
        position: relative;
        height: 200px;
        overflow: hidden;
        
        .culture-image {
          width: 100%;
          height: 100%;
          object-fit: cover;
          transition: transform 0.5s ease;
        }
        
        &:hover .culture-image {
          transform: scale(1.05);
        }
        
        .culture-tag {
          position: absolute;
          top: 1rem;
          left: 1rem;
          background-color: var(--primary-color);
          color: white;
          padding: 0.25rem 0.75rem;
          border-radius: 0.25rem;
          font-size: 0.75rem;
          font-weight: 600;
        }
      }
      
      .culture-content {
        padding: 1.5rem;
      }
      
      .culture-name {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        transition: color 0.3s ease;
        
        .culture-link:hover & {
          color: var(--primary-color);
        }
      }
      
      .culture-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        font-size: 0.875rem;
        color: var(--text-secondary);
      }
      
      .culture-description {
        color: var(--text-secondary);
        line-height: 1.6;
        margin-bottom: 1.5rem;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      
      .culture-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      
      .read-more {
        color: var(--primary-color);
        font-weight: 500;
        font-size: 0.875rem;
        transition: color 0.3s ease;
        
        .culture-link:hover & {
          color: var(--secondary-color);
        }
      }
      
      .culture-stats {
        display: flex;
        gap: 1rem;
        
        .stat-item {
          display: flex;
          align-items: center;
          gap: 0.25rem;
          color: var(--text-secondary);
          font-size: 0.875rem;
          
          svg {
            width: 1rem;
            height: 1rem;
          }
        }
      }
    }
    
    // 无数据提示
    .no-data {
      text-align: center;
      padding: 3rem 0;
      color: var(--text-secondary);
      
      svg {
        width: 3rem;
        height: 3rem;
        margin-bottom: 1rem;
        opacity: 0.5;
      }
      
      p {
        font-size: 1.125rem;
      }
    }
    
    // 分页控制
    .pagination {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 1.5rem;
      margin-top: 2rem;
      
      .pagination-button {
        padding: 0.5rem 1rem;
        background-color: white;
        border: 1px solid var(--border-color);
        border-radius: 0.25rem;
        color: var(--text-primary);
        cursor: pointer;
        transition: all 0.3s ease;
        
        &:hover:not(:disabled) {
          background-color: var(--primary-color);
          color: white;
          border-color: var(--primary-color);
        }
        
        &:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
      }
      
      .pagination-info {
        font-size: 0.875rem;
        color: var(--text-secondary);
      }
    }
  }
}
</style>