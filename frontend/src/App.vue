<template>
  <div class="app-container">
    <header class="app-header" v-motion-slide-visible-once-bottom>
      <div class="container">
        <div class="header-content">
          <div class="logo-container">
            <router-link to="/" class="logo">
              <span class="logo-text" v-motion-slide-visible-once-right>乘灼</span>
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
          
          <!-- 搜索按钮已移除 -->
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
            <p class="slogan-text">
              <span class="slogan-line" data-text="乘势向上">乘势向上</span>
              <span class="slogan-line" data-text="灼见真知">灼见真知</span>
            </p>
          </div>
          
          <div class="footer-section">
            <h3>快速链接</h3>
            <ul class="footer-links">
              <li><router-link to="/">首页</router-link></li>
              <li><router-link to="/minzu">民族文化</router-link></li>
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
          <p>&copy; {{ currentYear }} 乘灼文化. 保留所有权利.</p>
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
import { ArrowUp } from '@element-plus/icons-vue'

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
  { name: '民族文化', path: '/minzu' },
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

<style lang="scss">
// 导入行书字体（增强回退机制）
@font-face {
  font-family: 'XingShu';
  // 首选系统中文字体作为主要字体，确保在没有外部字体文件时也能正常显示
  src: local('STXingkai'), local('华文行楷'), local('STKaiti'), local('KaiTi');
  // 同时保留外部字体文件引用，当实际文件存在时会使用
  src: url('./assets/fonts/xingshu.woff2') format('woff2'),
       url('./assets/fonts/xingshu.woff') format('woff'),
       url('./assets/fonts/xingshu.ttf') format('truetype'),
       // 回退到系统字体
       local('STXingkai'), local('华文行楷'), local('STKaiti'), local('KaiTi');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}

// 全局字体变量 - 增强回退机制
:root {
  --xing-shu-font: 'XingShu', 'STXingkai', '华文行楷', 'STKaiti', 'KaiTi', 'SimSun', serif;
}
</style>

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
        font-family: var(--xing-shu-font);
        font-size: 1.2em; // 1.2倍于标准文本字体大小
        line-height: 1.5; // 行高为字体大小的1.5倍
        letter-spacing: 0.15em; // 字间距为0.15em
        
        // 确保字体渲染清晰
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-rendering: optimizeLegibility;
        
        // 响应式调整
        @media (max-width: 768px) {
          display: none;
        }
        
        @media (min-width: 769px) and (max-width: 1024px) {
          font-size: 1.1em;
          letter-spacing: 0.12em;
        }
        
        @media (min-width: 1025px) {
          font-size: 1.3em;
          letter-spacing: 0.18em;
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
  background-color: $gray-800;
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
          color: rgba(255, 255, 255, 0.85);
        }
        
        // 标语文字特殊动效
        .slogan-text {
          margin-top: 20px;
          font-family: var(--xing-shu-font);
          font-size: 1.5em;
          line-height: 1.8;
          text-align: left;
          
          .slogan-line {
            display: block;
            position: relative;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
            padding: 5px 0;
            z-index: 1;
            overflow: hidden;
            
            &:before {
              content: attr(data-text);
              position: absolute;
              top: 0;
              left: 0;
              width: 100%;
              height: 100%;
              color: $primary-color;
              clip-path: inset(0 0 100% 0);
              transition: clip-path 0.6s cubic-bezier(0.22, 1, 0.36, 1);
              padding: 5px 0;
              z-index: -1;
            }
            
            // 为第二个slogan-line添加不同的动画方向
            &:nth-child(2):before {
              clip-path: inset(100% 0 0 0);
            }
            
            &:hover {
              transform: translateX(10px) translateY(-2px) scale(1.03);
              color: rgba(255, 255, 255, 1);
              text-shadow: 0 2px 10px rgba($primary-color, 0.3);
              
              &:before {
                clip-path: inset(0 0 0 0);
              }
            }
          }
        }
      
      .footer-links {
        list-style: none;
        padding: 0;
        
        li {
          margin-bottom: 8px;
          
          a {
            color: rgba(255, 255, 255, 0.85);
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
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.85);
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