<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { createLogger } from '../utils/logger'

// 创建日志实例
const logger = createLogger('NotFoundView');
const router = useRouter();

// 动画控制
const isVisible = ref(false);

// 返回首页
const goToHome = () => {
  logger.info('用户点击返回首页按钮');
  router.push('/');
};

// 探索文化
const exploreCultures = () => {
  logger.info('用户点击探索文化按钮');
  router.push('/culture');
};

onMounted(() => {
  logger.info('NotFoundView组件已挂载');
  // 添加延迟以触发动画
  setTimeout(() => {
    isVisible.value = true;
  }, 100);
});
</script>

<template>
  <section class="not-found-view" :class="{ 'visible': isVisible }">
    <!-- 错误状态展示 -->
    <div class="not-found-container">
      <!-- 错误图标 -->
      <div class="error-icon">
        <svg width="120" height="120" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="12" cy="12" r="10" stroke="var(--color-primary)" stroke-width="1.5" stroke-dasharray="1 1"/>
          <path d="M12 8V12L14 14" stroke="var(--color-primary)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="12" cy="12" r="1" fill="var(--color-primary)"/>
        </svg>
      </div>
      
      <!-- 错误信息 -->
      <h1 class="error-title">404</h1>
      <h2 class="error-subtitle">抱歉，页面未找到</h2>
      <p class="error-description">您访问的页面不存在或已被移除</p>
      
      <!-- 操作按钮 -->
      <div class="error-actions">
        <button class="btn-primary" @click="goToHome">返回首页</button>
        <button class="btn-secondary" @click="exploreCultures">探索文化</button>
      </div>
    </div>
  </section>
</template>

<style lang="scss" scoped>
.not-found-view {
  width: 100%;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-background);
  padding: var(--spacing-2xl) var(--spacing-padding);
  transition: all 0.6s ease;
  opacity: 0;
  transform: scale(0.9);
  
  &.visible {
    opacity: 1;
    transform: scale(1);
  }
  
  .not-found-container {
    max-width: 500px;
    width: 100%;
    text-align: center;
    padding: var(--spacing-3xl);
    background-color: var(--color-surface);
    border-radius: var(--border-radius-xl);
    box-shadow: var(--shadow-lg);
    transition: all 0.8s ease;
    animation: float 6s ease-in-out infinite;
  }
  
  .error-icon {
    margin-bottom: var(--spacing-xl);
    opacity: 0;
    transform: translateY(-20px);
    transition: all 0.8s ease 0.2s;
    
    .not-found-view.visible & {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .error-title {
    font-size: var(--font-size-6xl);
    font-weight: 800;
    color: var(--color-primary);
    margin: 0 0 var(--spacing-md) 0;
    opacity: 0;
    transform: translateY(-20px);
    transition: all 0.8s ease 0.4s;
    
    .not-found-view.visible & {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .error-subtitle {
    font-size: var(--font-size-2xl);
    font-weight: 600;
    color: var(--color-text-primary);
    margin: 0 0 var(--spacing-md) 0;
    opacity: 0;
    transform: translateY(-20px);
    transition: all 0.8s ease 0.6s;
    
    .not-found-view.visible & {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .error-description {
    font-size: var(--font-size-base);
    color: var(--color-text-secondary);
    margin: 0 0 var(--spacing-2xl) 0;
    line-height: 1.6;
    opacity: 0;
    transform: translateY(-20px);
    transition: all 0.8s ease 0.8s;
    
    .not-found-view.visible & {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .error-actions {
    display: flex;
    gap: var(--spacing-lg);
    justify-content: center;
    opacity: 0;
    transform: translateY(-20px);
    transition: all 0.8s ease 1s;
    
    .not-found-view.visible & {
      opacity: 1;
      transform: translateY(0);
    }
    
    button {
      padding: var(--spacing-md) var(--spacing-xl);
      border-radius: var(--border-radius-lg);
      font-size: var(--font-size-base);
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
      border: none;
      outline: none;
      min-width: 140px;
    }
    
    .btn-primary {
      background-color: var(--color-primary);
      color: white;
      
      &:hover {
        background-color: var(--color-primary-dark);
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
      }
    }
    
    .btn-secondary {
      background-color: var(--color-secondary);
      color: white;
      
      &:hover {
        background-color: var(--color-secondary-dark);
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
      }
    }
  }
}

// 浮动动画
@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
  100% {
    transform: translateY(0px);
  }
}

// 响应式设计
@media (max-width: 768px) {
  .not-found-view {
    padding: var(--spacing-xl) var(--spacing-padding);
    
    .not-found-container {
      padding: var(--spacing-2xl);
    }
    
    .error-icon svg {
      width: 100px;
      height: 100px;
    }
    
    .error-title {
      font-size: var(--font-size-5xl);
    }
    
    .error-subtitle {
      font-size: var(--font-size-xl);
    }
    
    .error-actions {
      flex-direction: column;
      align-items: center;
      
      button {
        width: 100%;
        min-width: auto;
      }
    }
  }
}

@media (max-width: 480px) {
  .not-found-view {
    .not-found-container {
      padding: var(--spacing-xl);
      border-radius: var(--border-radius-lg);
    }
    
    .error-icon svg {
      width: 80px;
      height: 80px;
    }
    
    .error-title {
      font-size: var(--font-size-4xl);
    }
  }
}
</style>
