<template>
  <div class="app-container">
    <header class="app-header" :class="{ 'is-visible': headerVisible }">
      <div class="container">
        <div class="header-content">
          <div class="logo-container">
            <router-link to="/" class="logo">
              <span 
                ref="logoRef"
                class="logo-text animate-on-load"
              >
                乘灼
              </span>
            </router-link>
          </div>
          
          <nav class="main-nav">
            <ul class="nav-list">
              <li class="nav-item" v-for="(item, index) in navItems" :key="item.path">
                <router-link 
                  :to="item.path" 
                  class="nav-link" 
                  :style="{ animationDelay: `${0.1 + index * 0.05}s` }"
                >
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
            <p>邮箱：contact@chengzhuo.com</p>
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
const logoRef = ref(null)
const scrollPosition = ref(0)
const headerVisible = ref(false)

// 使用requestAnimationFrame优化滚动处理
let animationId = null;
let lastScrollY = 0;

// 监听页面加载完成后触发header动画
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  
  // 添加页面可见性检查，仅在页面可见时激活动画
  document.addEventListener('visibilitychange', handleVisibilityChange)
  
  // 初始延迟显示header以提高感知性能
  setTimeout(() => {
    headerVisible.value = true
  }, 100)
  
  // 预加载动画资源
  preloadAnimationResources()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.removeEventListener('visibilitychange', handleVisibilityChange)
  
  // 清理动画帧
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
})

// 处理页面可见性变化
const handleVisibilityChange = () => {
  const navLinks = document.querySelectorAll('.nav-link')
  
  if (document.hidden) {
    // 页面不可见时暂停所有动画
    navLinks.forEach(link => {
      link.style.animationPlayState = 'paused'
    })
    if (logoRef.value) {
      logoRef.value.style.animationPlayState = 'paused'
    }
  } else {
    // 页面可见时恢复动画
    navLinks.forEach(link => {
      link.style.animationPlayState = 'running'
    })
    if (logoRef.value) {
      logoRef.value.style.animationPlayState = 'running'
    }
  }
}

// 预加载动画资源
const preloadAnimationResources = () => {
  // 创建一个不可见的元素来预加载动画效果
  const preloader = document.createElement('div')
  preloader.style.position = 'absolute'
  preloader.style.width = '0'
  preloader.style.height = '0'
  preloader.style.overflow = 'hidden'
  document.body.appendChild(preloader)
  
  // 模拟动画资源加载
  setTimeout(() => {
    document.body.removeChild(preloader)
  }, 1000)
}

const handleScroll = () => {
  lastScrollY = window.scrollY;
  
  if (!animationId) {
    animationId = requestAnimationFrame(updateScrollEffects);
  }
}

const updateScrollEffects = () => {
  const currentScrollY = lastScrollY;
  scrollPosition.value = currentScrollY;
  
  // 更新滚动状态 - 使用节流逻辑
  if (Math.abs(currentScrollY - (isScrolled.value ? 100 : 0)) > 30) {
    isScrolled.value = currentScrollY > 50;
  }
  
  // 回到顶部按钮显示逻辑
  showBackToTop.value = currentScrollY > 300;
  
  // logo动态效果处理 - 使用CSS变量而非直接操作style
  if (logoRef.value) {
    // 计算视差效果值和透明度
    const scrollFactor = Math.min(currentScrollY * 0.03, 10);
    const opacityFactor = Math.max(0.8, 1 - currentScrollY * 0.001);
    
    // 使用CSS变量更新，避免频繁的样式属性更改
    logoRef.value.style.setProperty('--logo-transform-y', `-${scrollFactor}px`);
    logoRef.value.style.setProperty('--logo-opacity', opacityFactor.toString());
  }
  
  animationId = null;
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
    
    // 性能优化：提前告知浏览器将要变化的属性
    will-change: transform, background-color, box-shadow;
    
    // 更高效的过渡属性 - 避免使用'all'
    transition: transform 0.3s ease, 
                background-color 0.3s ease, 
                box-shadow 0.3s ease, 
                height 0.3s ease;
    
    // 默认不可见，用于入场动画
    opacity: 0;
    transform: translateY(-20px);
    
    // 可见状态的样式 - 使用类而非v-motion指令
    &.is-visible {
      opacity: 1;
      transform: translateY(0);
      animation: slideInUp 0.5s ease-out 0.1s both;
    }
    
    // 入场动画 - 更高效的关键帧
    @keyframes slideInUp {
      from {
        opacity: 0;
        transform: translateY(-20px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }
    
    // 滚动时的样式变化 - 优化性能
    &.is-scrolled {
      height: 60px;
      box-shadow: $shadow-md;
      background-color: rgba($bg-primary, 0.98);
      backdrop-filter: blur(8px);
      
      .logo-container .logo .logo-text {
        font-size: 1em;
        transition: font-size 0.3s ease;
      }
    }
  
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
        
        // 使用CSS变量存储动态值
        --logo-transform-y: 0;
        --logo-opacity: 1;
        
        // 基本动画设置 - 使用更高效的属性组合
        transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), 
                    letter-spacing 0.3s ease, 
                    text-shadow 0.3s ease;
        position: relative;
        display: inline-block;
        
        // 文字阴影增强视觉深度
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        
        // 应用滚动效果的CSS变量
        transform: translateY(var(--logo-transform-y));
        opacity: var(--logo-opacity);
        
        // 悬停效果 - 只修改GPU加速属性
        &:hover {
          // 轻微放大和提升 - 使用transform (GPU加速)
          transform: scale(1.1) translateY(-3px) translateY(var(--logo-transform-y));
          
          // 增强文字阴影
          text-shadow: 0 4px 8px rgba($primary-color, 0.25),
                       0 1px 3px rgba(0, 0, 0, 0.1);
          
          // 颜色渐变效果 - 使用伪元素代替直接操作background-clip
          &::after {
            content: '乘灼';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, $primary-color, $accent-color);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            z-index: -1;
            transition: opacity 0.3s ease;
            opacity: 1;
          }
          
          // 字母间距变化
          letter-spacing: 0.2em;
        }
        
        // 创建伪元素用于渐变效果
        &::after {
          content: '乘灼';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: linear-gradient(135deg, $primary-color, $accent-color);
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
          z-index: -1;
          opacity: 0;
          transition: opacity 0.3s ease;
        }
        
        // 激活状态
        &:active {
          transform: scale(1.05) translateY(var(--logo-transform-y));
          transition: transform 0.1s ease;
        }
        
        // 加载动画 - 优化关键帧以减少重排
        @keyframes pulseText {
          0%, 100% {
            transform: scale(1) translateY(var(--logo-transform-y));
          }
          50% {
            transform: scale(1.05) translateY(var(--logo-transform-y));
          }
        }
        
        // 初始化动画 - 仅在页面首次加载时触发
        &.animate-on-load {
          animation: pulseText 0.8s ease-out 0.2s both; // 添加延迟以提高感知性能
          animation-play-state: running;
        }
        
        // 优化滚动状态下的动画
        .app-header.is-scrolled & {
          animation-play-state: paused; // 滚动时暂停动画以提高性能
        }
        
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
        
        // 触摸设备优化
        @media (hover: none) and (pointer: coarse) {
          &:active {
            transform: scale(1.05) translateY(-2px);
            text-shadow: 0 2px 4px rgba($primary-color, 0.2);
          }
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
          position: relative;
          
          // 初始状态 - 用于动画
          opacity: 0;
          transform: translateY(10px);
          
          // 使用CSS动画代替v-motion指令
          animation: navLinkFadeIn 0.4s ease-out both;
          
          // 优化过渡效果，仅包含必要属性
          transition: color 0.2s ease, 
                      transform 0.2s ease;
          
          // 悬停效果 - 使用transform代替border-bottom变化
          &:hover, &.router-link-active {
            color: $primary-color;
            transform: translateY(-2px);
          }
          
          // 使用伪元素实现下划线效果，避免重排
          &:hover::after, &.router-link-active::after {
            width: 100%;
          }
          
          &::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 0;
            height: 2px;
            background-color: $primary-color;
            transition: width 0.3s ease;
          }
        }
        
        // 导航链接的入场动画
        @keyframes navLinkFadeIn {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
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
          // 实现水平方向从左到右排列
          display: flex;
          flex-direction: row;
          align-items: center;
          // 确保子元素之间有适当间距
          gap: 1rem;
          // 增强响应式布局能力
          flex-wrap: wrap;
          justify-content: flex-start;
          // 确保父容器宽度不会限制子元素水平排列
          width: 100%;
          // 移除可能的边距影响
          margin: 0;
          padding: 0;
          
          .slogan-line {
            display: inline-block;
            position: relative;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
            // 优化内边距，确保良好的触摸区域
            padding: 8px 12px;
            z-index: 1;
            overflow: hidden;
            // Adjust width for better horizontal display
            // width: 4ch; - 移除固定宽度限制，让内容自然流动
            min-width: 4ch; // 保持最小宽度
            // Ensure text is displayed from left to right
            text-align: left;
            direction: ltr;
            // 确保元素在不同屏幕尺寸下有良好表现
            flex-shrink: 0;
            
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
              padding: 8px 12px;
              z-index: -1;
              box-sizing: border-box;
            }
            
            // 为第二个slogan-line添加不同的动画方向
            &:nth-child(2):before {
              clip-path: inset(100% 0 0 0);
              padding: 8px 12px;
              box-sizing: border-box;
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