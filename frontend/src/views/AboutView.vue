<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useIntersectionObserver } from '@vueuse/core'

// 组件懒加载 - 延迟导入Heavy组件
const ModernButton = defineAsyncComponent(() => import('../components/ModernButton.vue'))

// 页面元素引用
const missionVisionRef = ref(null)
const featuresRef = ref(null)
const contactRef = ref(null)
const particlesRef = ref(null)
const heroRef = ref(null)
const headerContentRef = ref(null)

// 性能优化：减少不必要的DOM查询 - 缓存常用元素
let scrollElements = []
let headerContent = null
let aboutView = null

// 性能优化：计算属性缓存动画配置
const fadeInUpConfig = computed(() => ({
  opacity: 0,
  transform: 'translateY(30px)'
}))

// 性能优化：防抖函数
const debounce = (func, wait) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

// 性能优化：节流函数
const throttle = (func, limit) => {
  let inThrottle
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

// 处理联系按钮点击
const handleContact = () => {
  // 平滑滚动到联系部分
  if (contactRef.value) {
    contactRef.value.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

// 性能优化：使用IntersectionObserver替代滚动事件监听元素可见性
const setupIntersectionObservers = () => {
  const options = {
    root: null,
    rootMargin: '-100px',
    threshold: 0.1
  }
  
  // 为使命愿景部分设置观察者
  if (missionVisionRef.value) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const mission = entry.target.querySelector('.mission')
          const vision = entry.target.querySelector('.vision')
          if (mission) mission.classList.add('animate-in')
          if (vision) vision.classList.add('animate-in')
          observer.unobserve(entry.target) // 只执行一次
        }
      })
    }, options)
    observer.observe(missionVisionRef.value)
    
    // 存储观察者引用以便清理
    scrollElements.push({
      observer,
      element: missionVisionRef.value
    })
  }
  
  // 为特色部分设置观察者
  if (featuresRef.value) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const items = entry.target.querySelectorAll('.feature-item')
          items.forEach((item, index) => {
            // 错开动画延迟以提高性能
            setTimeout(() => {
              item.classList.add('animate-in')
            }, index * 100)
          })
          observer.unobserve(entry.target)
        }
      })
    }, options)
    observer.observe(featuresRef.value)
    
    scrollElements.push({
      observer,
      element: featuresRef.value
    })
  }
  
  // 为联系部分设置观察者
  if (contactRef.value) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in')
          observer.unobserve(entry.target)
        }
      })
    }, options)
    observer.observe(contactRef.value)
    
    scrollElements.push({
      observer,
      element: contactRef.value
    })
  }
}

// 优化的滚动处理 - 使用requestAnimationFrame和节流
let lastScrollY = 0
const handleScroll = throttle(() => {
  const currentScrollY = window.scrollY
  
  // 性能优化：使用requestAnimationFrame处理动画
  window.requestAnimationFrame(() => {
    // 滚动时的视差效果
    if (particlesRef.value) {
      // 使用transform属性触发GPU加速
      particlesRef.value.style.transform = `translateY(${currentScrollY * 0.1}px)`
    }
    
    // 标题栏滚动效果
    if (headerContentRef.value) {
      const opacity = Math.max(0, 1 - currentScrollY / 300)
      headerContentRef.value.style.opacity = opacity
      headerContentRef.value.style.transform = `translateY(${-currentScrollY * 0.2}px)`
    }
    
    // 滚动进度指示器
    if (aboutView && window.innerHeight > 0) {
      const scrollHeight = document.documentElement.scrollHeight
      const windowHeight = window.innerHeight
      const scrollTop = window.scrollY || window.pageYOffset
      const scrolled = (scrollTop / (scrollHeight - windowHeight)) * 100
      aboutView.style.setProperty('--scroll-progress', `${scrolled}%`)
    }
  })
  
  lastScrollY = currentScrollY
}, 16) // 约60fps

// 性能优化：预加载字体和关键资源
const preloadResources = () => {
  // 预加载字体（如果有自定义字体）
  if ('fonts' in document) {
    // 这里可以添加字体预加载逻辑
  }
  
  // 预加载关键图像
  const imageUrls = [] // 如果有背景图或其他关键图片可以添加
  imageUrls.forEach(url => {
    const link = document.createElement('link')
    link.rel = 'preload'
    link.as = 'image'
    link.href = url
    document.head.appendChild(link)
  })
}

// 清理观察者和事件监听器
const cleanupObservers = () => {
  // 清理IntersectionObservers
  scrollElements.forEach(({ observer, element }) => {
    if (observer && element) {
      observer.unobserve(element)
      observer.disconnect()
    }
  })
  scrollElements = []
  
  // 清理事件监听器
  window.removeEventListener('scroll', handleScroll)
}

// 页面挂载和卸载时的事件处理
onMounted(() => {
  // 缓存DOM元素引用
  headerContent = headerContentRef.value
  aboutView = document.querySelector('.about-view')
  
  // 设置CSS变量用于性能优化的滚动指示器
  if (aboutView) {
    aboutView.style.setProperty('--scroll-progress', '0%')
  }
  
  // 设置滚动事件监听器
  window.addEventListener('scroll', handleScroll, { passive: true })
  
  // 设置交叉观察器
  setupIntersectionObservers()
  
  // 预加载资源
  preloadResources()
  
  // 页面加载完成后添加淡入效果
  document.body.classList.add('page-loaded')
})

onUnmounted(() => {
  // 清理资源
  cleanupObservers()
})

// 优化的异步组件加载
function defineAsyncComponent(loader) {
  // 简单实现异步组件加载
  return {
    loader,
    loadingComponent: null,
    errorComponent: null,
    delay: 200,
    timeout: 3000
  }
}
</script>

<template>
  <div class="about-view">
    <!-- 页面头部，与其他页面保持一致的渐变背景 -->
    <div class="about-header" ref="heroRef">
      <!-- 粒子背景 -->
      <div class="particles-container" ref="particlesRef">
        <div class="particle" style="top: 20%; left: 15%; width: 60px; height: 60px; animation-delay: 0s;"></div>
        <div class="particle" style="top: 40%; left: 80%; width: 40px; height: 40px; animation-delay: 1s;"></div>
        <div class="particle" style="top: 60%; left: 30%; width: 50px; height: 50px; animation-delay: 2s;"></div>
        <div class="particle" style="top: 80%; left: 60%; width: 30px; height: 30px; animation-delay: 1.5s;"></div>
        <div class="particle" style="top: 30%; left: 50%; width: 70px; height: 70px; animation-delay: 0.5s;"></div>
      </div>
      <div class="gradient-overlay"></div>
      <div class="header-content">
        <h1 class="section-title">
          <span class="title-decoration"></span>
          关于我们
          <span class="title-decoration"></span>
        </h1>
      </div>
    </div>

    <!-- 主要内容区域，使用与其他页面一致的container结构 -->
    <div class="about-content">
      <div class="container">
        <!-- 使命愿景部分 -->
        <section class="mission-vision" ref="missionVisionRef">
          <div class="section-header">
            <h2 class="section-title">
              <span class="title-decoration"></span>
              我们的使命与愿景
              <span class="title-decoration"></span>
            </h2>
          </div>
          <div class="mission-vision-content">
        <div class="mission">
          <h3 class="mission-title">我们的使命</h3>
          <div class="content-text">
            <p class="mission-text">
              乘灼致力于收集、整理和展示中华大地上丰富多彩的民族文化资源，让更多的人了解和传承中华优秀传统文化。我们希望通过数字技术，打破地域和时间的限制，让珍贵的民族文化得以保存和传播。
            </p>
          </div>
        </div>
        
        <div class="vision">
          <h3 class="vision-title">我们的愿景</h3>
          <div class="content-text">
            <p class="vision-text">
              乘灼数字平台，连接传统与现代，促进民族文化交流与传承，让民族文化在新时代焕发新的生机。
            </p>
          </div>
        </div>
      </div>
        </section>

        <!-- 网站特色部分 -->
        <section class="features" ref="featuresRef">
          <div class="section-header">
            <h2 class="section-title">
              <span class="title-decoration"></span>
              网站特色
              <span class="title-decoration"></span>
            </h2>
            <p class="section-description">
              我们提供丰富多彩的文化内容和用户体验
            </p>
          </div>
          <div class="feature-list">
          <div class="feature-item touch-feedback">
            <div class="feature-icon">📚</div>
            <h3 class="feature-title">丰富的内容资源</h3>
            <p class="feature-description">
              涵盖全国各地的民族文化，包括传统节日、民间艺术、饮食习惯、服饰文化等多个方面。
            </p>
          </div>
          <div class="feature-item touch-feedback">
            <div class="feature-icon">🗺️</div>
            <h3 class="feature-title">地区分类浏览</h3>
            <p class="feature-description">
              按地区查看不同地方的特色民俗，感受中国文化的多样性和丰富性。
            </p>
          </div>
          <div class="feature-item touch-feedback">
            <div class="feature-icon">🔍</div>
            <h3 class="feature-title">深度文化解析</h3>
            <p class="feature-description">
              提供详尽的民族文化解析，帮助用户深入了解文化背后的历史和意义。
            </p>
          </div>
        </div>
        </section>

        <!-- 联系我们部分 -->
        <section class="contact" ref="contactRef">
          <div class="section-header">
            <h2 class="section-title">
              <span class="title-decoration"></span>
              联系我们
              <span class="title-decoration"></span>
            </h2>
          </div>
          <div class="contact-content">
            <p class="contact-text">
              如果您有任何问题、建议或合作意向，欢迎随时与我们联系。我们期待与您一起，为传承和弘扬中华优秀传统文化贡献力量。
            </p>
            <div class="contact-info">
              <div class="contact-item">
                <span class="contact-label">邮箱：</span>
                <span class="contact-value">contact@chengzhuo.com</span>
              </div>
              <div class="contact-item">
                <span class="contact-label">电话：</span>
                <span class="contact-value">400-123-4567</span>
              </div>
            </div>
            <div class="contact-button">
              <ModernButton 
                size="medium" 
                variant="primary"
                @click="handleContact"
              >
                立即联系
              </ModernButton>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 基础样式设置 */
.about-view {
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* 页面头部样式，与其他页面保持一致 */
.about-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
  z-index: 1;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 15px;
  color: #333;
  position: relative;
  display: inline-block;
  padding: 0 20px;
}

.about-header .section-title {
  color: white;
  margin-bottom: 20px;
}

.title-decoration {
  display: inline-block;
  width: 20px;
  height: 2px;
  background-color: #667eea;
  margin: 0 10px;
  vertical-align: middle;
}

.about-header .title-decoration {
  background-color: white;
}

.section-description {
  font-size: 1.2rem;
  color: #666;
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.6;
}

.about-header .section-description {
  color: rgba(255, 255, 255, 0.9);
}

/* 主要内容区域样式 */
.about-content {
  padding: 60px 20px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.about-content section {
  margin-bottom: 80px;
}

/* 章节标题样式 */
.section-header {
  text-align: center;
  margin-bottom: 40px;
}

/* 使命愿景部分样式 - 统一排版 */
.mission-vision-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
}

.mission, .vision {
  background-color: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s, box-shadow 0.3s;
}

.mission:hover, .vision:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.mission-title, .vision-title {
  color: #667eea;
  font-size: 1.5rem;
  margin-bottom: 20px;
  font-weight: 600;
  text-align: center;
}

/* 内容文本容器 - 统一缩进和间距 */
.content-text {
  margin-top: 16px;
}

.mission-text, .vision-text {
  color: #666;
  font-size: 1rem;
  line-height: 1.8;
  margin-bottom: 16px;
  text-align: justify;
}

.mission-text:last-child, .vision-text:last-child {
  margin-bottom: 0;
}

/* 特色列表样式 - 统一排版 */
.feature-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
}

.feature-item {
  background-color: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  border-top: 4px solid #667eea;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-height: 280px;
}

.feature-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.feature-item:hover::before {
  transform: scaleX(1);
}

/* 特色图标样式 */
.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: #667eea;
  opacity: 0.9;
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.feature-item:hover .feature-icon {
  transform: scale(1.1);
  opacity: 1;
}

.feature-title {
  color: #333;
  font-size: 1.3rem;
  margin-bottom: 16px;
  font-weight: 600;
}

.feature-description {
  color: #666;
  font-size: 1rem;
  line-height: 1.8;
  flex-grow: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: justify;
  padding: 0 8px;
}

/* 文本排版统一规范 */
p {
  margin-bottom: 16px;
  text-indent: 2em;
}

p:last-child {
  margin-bottom: 0;
}

/* 联系我们样式 */
.contact-content {
  background-color: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  text-align: center;
}

.contact-text {
  color: #666;
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: 30px;
}

.contact-info {
  margin-bottom: 30px;
}

.contact-item {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.contact-label {
  color: #333;
  font-weight: 600;
  margin-right: 10px;
}

.contact-value {
  color: #666;
}

.contact-button {
  margin-top: 20px;
}

/* 触摸反馈效果 */
.touch-feedback {
  transition: all 0.3s ease;
}

.touch-feedback:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

/* 进入视口动画 */
.mission, .vision, .feature-item {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.8s ease-out, transform 0.8s ease-out;
}

.mission.animate-in,
.vision.animate-in,
.feature-item.animate-in {
  opacity: 1;
  transform: translateY(0);
}

/* 错开动画延迟 */
.mission:nth-child(1) {
  transition-delay: 0.1s;
}

.vision:nth-child(2) {
  transition-delay: 0.2s;
}

.feature-item:nth-child(1) {
  transition-delay: 0.1s;
}

.feature-item:nth-child(2) {
  transition-delay: 0.2s;
}

.feature-item:nth-child(3) {
  transition-delay: 0.3s;
}

/* 粒子背景效果 */
.particles-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  overflow: hidden;
}

.particle {
  position: absolute;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.3);
  animation: float 8s infinite ease-in-out;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

/* 按钮交互效果增强 */
.contact-button .modern-button {
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.contact-button .modern-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
}

.contact-button .modern-button:active {
  transform: translateY(0);
}

/* 页面加载过渡效果 */
.page-loaded {
  transition: opacity 0.6s ease;
}

/* 性能优化：使用CSS变量和GPU加速 */
.about-view {
  /* CSS变量用于滚动进度 */
  --scroll-progress: 0%;
  will-change: transform;
}

/* 滚动进度指示器 - 使用CSS变量实现 */
.about-view::after {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  z-index: 1000;
  width: var(--scroll-progress);
  pointer-events: none;
  /* 性能优化：使用GPU加速 */
  transform: translateZ(0);
}

/* 性能优化：GPU加速关键元素 */
.particles-container,
.header-content,
.mission,
.vision,
.feature-item {
  /* 触发GPU加速，提高动画性能 */
  transform: translateZ(0);
  will-change: transform, opacity;
  backface-visibility: hidden;
}

/* 性能优化：简化动画关键帧 */
@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
  }
}

/* 性能优化：减少重排和重绘 */
.about-header {
  position: relative;
  overflow: hidden;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.9));
  pointer-events: none;
  /* 性能优化：GPU加速 */
  transform: translateZ(0);
}

/* 性能优化：优化触摸反馈效果 */
.touch-feedback {
  transition: all 0.3s ease-out;
  /* 减少触摸延迟 */
  touch-action: manipulation;
  /* 优化点击事件 */
  cursor: pointer;
}

/* 性能优化：懒加载图片样式占位 */
.image-placeholder {
  background-color: #f0f0f0;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

/* 响应式设计优化 - 全面适配各种设备尺寸 */

/* 超大屏幕(1200px+) - 微调布局以适应大屏幕 */
@media (min-width: 1200px) {
  .container {
    max-width: 1140px;
    margin: 0 auto;
  }
  
  .mission-vision-content,
  .features-grid {
    max-width: 100%;
  }
}

/* 大屏幕(992px-1199px) */
@media (max-width: 1199px) {
  .container {
    max-width: 960px;
    margin: 0 auto;
  }
  
  .features-grid {
    gap: 1.5rem;
  }
}

/* 中等屏幕(768px-991px) */
@media (max-width: 991px) {
  .container {
    max-width: 720px;
    margin: 0 auto;
  }
  
  .mission-vision-content {
    flex-direction: column;
    gap: 2rem;
  }
  
  .mission,
  .vision {
    width: 100%;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .about-content section {
    margin-bottom: 60px;
  }
}

/* 小屏幕(576px-767px) */
@media (max-width: 767px) {
  .about-header {
    padding: 60px 15px;
  }
  
  .about-header .section-title {
    font-size: 2rem;
    padding: 0 10px;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .about-content {
    padding: 40px 15px;
  }
  
  .about-content section {
    margin-bottom: 50px;
  }
  
  .mission-vision-content {
    gap: 20px;
  }
  
  .mission, .vision {
    padding: 20px;
  }
  
  .feature-list {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .feature-item {
    padding: 20px;
  }
  
  .contact-content {
    padding: 25px;
  }
  
  .contact-item {
    flex-direction: column;
    text-align: center;
    margin-bottom: 15px;
  }
  
  .contact-label {
    margin-right: 0;
    margin-bottom: 5px;
  }
  
  /* 粒子背景在小屏幕上简化 */
  .particles-container {
    display: block;
  }
  
  .particle {
    transform: scale(0.7);
  }
}

/* 超小屏幕(<576px) - 手机竖屏优化 */
@media (max-width: 575px) {
  .about-header {
    padding: 40px 10px;
  }
  
  .about-header .section-title {
    font-size: 1.8rem;
  }
  
  .section-title {
    font-size: 1.8rem;
  }
  
  .section-description {
    font-size: 1rem;
  }
  
  /* 触摸目标优化 */
  .feature-item {
    padding: 1.5rem;
    border-radius: 12px;
  }
  
  .contact-button .modern-button {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    width: 100%;
    max-width: 200px;
  }
  
  /* 粒子背景在极小屏幕上进一步简化 */
  .particles-container {
    display: block;
  }
  
  .particle {
    transform: scale(0.5);
  }
}

/* 平板横屏优化 */
@media (min-width: 768px) and (max-width: 1024px) and (orientation: landscape) {
  .about-header {
    min-height: 60vh;
  }
}

/* 高DPI屏幕优化 */
@media (-webkit-device-pixel-ratio: 2), (resolution: 192dpi) {
  .gradient-overlay {
    background-image: linear-gradient(rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.9));
  }
  
  .title-decoration {
    background-image: linear-gradient(90deg, #667eea, #764ba2);
  }
}

/* 暗色模式支持 */
@media (prefers-color-scheme: dark) {
  .about-view {
    color-scheme: dark;
  }
  
  .mission,
  .vision,
  .feature-item,
  .contact-content {
    background-color: rgba(30, 30, 30, 0.7);
  }
  
  .mission:hover, .vision:hover,
  .feature-item:hover {
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  }
}
</style>