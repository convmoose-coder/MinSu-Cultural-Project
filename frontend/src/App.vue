<template>
  <div class="app">
    <!-- 导航栏组件 -->
    <Navbar />

    <!-- 主内容区域 -->
    <main class="main-content">
      <RouterView v-slot="{ Component }">
        <Transition name="fade" mode="out-in">
          <component :is="Component" />
        </Transition>
      </RouterView>
    </main>

    <!-- 页脚组件 -->
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Navbar from './components/common/Navbar.vue';
import Footer from './components/common/Footer.vue';
</script>

<style lang="scss">
// 全局样式在main.js中已导入

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--color-background);
  color: var(--color-text-primary);
  font-family: var(--font-family-base);
  line-height: var(--line-height-normal);
}

// 主内容样式
.main-content {
  flex: 1;
  padding-top: 4rem;
  /* 丰富的背景设计 - 中国传统元素与现代渐变结合 */
  background: linear-gradient(135deg, var(--color-background) 0%, #f5f0e6 100%);
  /* 传统纹样背景 - 半透明图案增强文化氛围 */
  background-image: 
    url('data:image/svg+xml;utf8,<svg width="120" height="120" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg"><path d="M60,0 L120,60 L60,120 L0,60 Z" fill="none" stroke="%23e8d4b4" stroke-width="1" opacity="0.2"/></svg>'),
    url('data:image/svg+xml;utf8,<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><circle cx="30" cy="30" r="5" fill="none" stroke="%23d4a76a" stroke-width="0.5" opacity="0.1"/></svg>');
  /* 添加微妙的质感 */
  background-blend-mode: overlay;
  position: relative;
  overflow: hidden;
}

/* 内容区域装饰性元素 */
.main-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  /* 顶部渐变过渡效果 */
  background: linear-gradient(to bottom, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 100px);
  pointer-events: none;
}

// 过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>