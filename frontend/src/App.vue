<template>
  <div class="app-container">
    <header class="app-header" v-motion-slide-visible-once-bottom>
      <div class="container">
        <div class="header-content">
          <div class="logo-container">
            <router-link to="/" class="logo">
              <span class="logo-text" v-motion-slide-visible-once-right>民俗文化</span>
            </router-link>
          </div>
          
          <nav class="main-nav">
            <ul class="nav-list">
              <li class="nav-item" v-for="item in navItems" :key="item.path">
                <router-link :to="item.path" class="nav-link" v-motion-slide-visible-once-bottom>
                  {{ item.name }}
                </router-link>
              </li>
            </ul>
          </nav>
          
          <div class="header-actions">
            <el-button type="primary" class="search-btn" v-motion-slide-visible-once-right>
              <el-icon><Search /></el-icon>
              搜索
            </el-button>
          </div>
        </div>
      </div>
      
      <div class="decorative-line"></div>
    </header>

    <main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <footer class="app-footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-section">
            <h3>关于我们</h3>
            <p>致力于传承和弘扬中华优秀传统文化，让民俗文化走进现代生活。</p>
          </div>
          
          <div class="footer-section">
            <h3>快速链接</h3>
            <ul class="footer-links">
              <li><router-link to="/">首页</router-link></li>
              <li><router-link to="/culture">民俗文化</router-link></li>
              <li><router-link to="/regions">地区浏览</router-link></li>
              <li><router-link to="/about">关于我们</router-link></li>
            </ul>
          </div>
          
          <div class="footer-section">
            <h3>联系我们</h3>
            <p>邮箱：contact@minsu.com</p>
            <p>电话：400-123-4567</p>
          </div>
        </div>
        
        <div class="footer-bottom">
          <p>&copy; {{ currentYear }} 民俗文化平台. 保留所有权利.</p>
        </div>
      </div>
    </footer>
    
    <!-- 回到顶部按钮 -->
    <Transition name="fade">
      <el-button 
        v-if="showBackToTop"
        type="primary"
        circle
        class="back-to-top"
        @click="scrollToTop"
      >
        <el-icon><ArrowUp /></el-icon>
      </el-button>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Menu, ArrowUp } from '@element-plus/icons-vue'

const router = useRouter()
const isScrolled = ref(false)
const showBackToTop = ref(false)
const isMenuOpen = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
  showBackToTop.value = window.scrollY > 300
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const navigateTo = (path) => {
  router.push(path)
  isMenuOpen.value = false
}

// 导航菜单项
const navItems = ref([
  { name: '首页', path: '/' },
  { name: '民俗文化', path: '/culture' },
  { name: '地区浏览', path: '/regions' },
  { name: '关于我们', path: '/about' }
])

// 当前年份
const currentYear = computed(() => new Date().getFullYear())

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style lang="scss" scoped>
// 导入主题变量
@import './assets/styles/variables.scss';
@import './assets/styles/theme.scss';

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: $bg-primary;
}

.app-header {
  background-color: $bg-primary;
  box-shadow: $shadow-sm;
  position: sticky;
  top: 0;
  z-index: $z-index-fixed;
  transition: all $transition-base;
  
  .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 80px;
    
    @media (max-width: 768px) {
      height: 60px;
      flex-wrap: wrap;
    }
  }
  
  .logo-container {
    .logo {
        display: flex;
        align-items: center;
        font-size: 24px;
        font-weight: bold;
        color: $primary-color;
        text-decoration: none;
      
      img {
        height: 40px;
        margin-right: 10px;
        
        @media (max-width: 768px) {
          height: 30px;
        }
      }
      
      .logo-text {
        font-family: 'STKaiti', 'KaiTi', serif;
        
        @media (max-width: 768px) {
          display: none;
        }
      }
    }
  }
  
  .main-nav {
    @media (max-width: 768px) {
      order: 3;
      width: 100%;
      margin-top: 10px;
    }
    
    .nav-list {
      display: flex;
      list-style: none;
      margin: 0;
      padding: 0;
      
      @media (max-width: 768px) {
        justify-content: center;
      }
      
      .nav-item {
        margin: 0 15px;
        
        @media (max-width: 768px) {
          margin: 0 10px;
        }
        
        .nav-link {
          color: $text-secondary;
          text-decoration: none;
          font-weight: 500;
          padding: 8px 0;
          border-bottom: 2px solid transparent;
          transition: $transition-base;
          
          &:hover, &.router-link-active {
            color: $primary-color;
            border-bottom-color: $primary-color;
          }
        }
      }
    }
  }
  
  .header-actions {
    .search-btn {
      border-radius: 20px;
      
      @media (max-width: 768px) {
        padding: 8px 12px;
        font-size: 14px;
      }
    }
  }
  
  .decorative-line {
    height: 4px;
    background: linear-gradient(90deg, 
      $primary-color 0%, 
      $success 50%, 
      $warning 100%);
  }
}

.app-main {
  flex: 1;
  padding: 20px 0;
}

.app-footer {
  background-color: $bg-secondary;
  color: $text-inverse;
  padding: 40px 0 20px;
  margin-top: auto;
  
  .footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
    margin-bottom: 30px;
    
    .footer-section {
    h3 {
        font-size: 18px;
        margin-bottom: 15px;
        color: $text-inverse;
        position: relative;
        padding-bottom: 8px;
        
        &::after {
          content: '';
          position: absolute;
          bottom: 0;
          left: 0;
          width: 30px;
          height: 2px;
          background-color: $primary-color;
        }
    }
      
      p {
          margin-bottom: 10px;
          line-height: $line-height-normal;
          color: rgba(255, 255, 255, 0.7);
        }
      
      .footer-links {
        list-style: none;
        padding: 0;
        
        li {
          margin-bottom: 8px;
          
          a {
            color: rgba(255, 255, 255, 0.7);
            text-decoration: none;
            transition: $transition-base;
            
            &:hover {
              color: $primary-color;
            }
          }
        }
      }
    }
  }
  
  .footer-bottom {
    text-align: center;
    padding-top: 20px;
    border-top: 1px solid $border-medium;
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
  }
}

// 页面过渡动画
.page-enter-active,
.page-leave-active {
  transition: opacity $transition-base, transform $transition-base;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

// 回到顶部按钮
.back-to-top {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: $z-index-fixed;
  box-shadow: 0 4px 12px rgba($primary-color, 0.3);
  transition: all $transition-base;
  
  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba($primary-color, 0.4);
  }
  
  @media (max-width: 768px) {
    bottom: 20px;
    right: 20px;
  }
}

// 淡入淡出过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity $transition-base;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>