<script setup lang="ts">
import { computed } from 'vue'

// Props
interface Props {
  size?: 'small' | 'medium' | 'large'
  color?: string
  message?: string
  fullScreen?: boolean
  overlay?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'medium',
  color: 'var(--color-primary)',
  message: '',
  fullScreen: false,
  overlay: true
})

// 计算属性
const spinnerSize = computed(() => {
  switch (props.size) {
    case 'small': return '32px'
    case 'large': return '64px'
    default: return '48px'
  }
})

const iconSize = computed(() => {
  switch (props.size) {
    case 'small': return '16px'
    case 'large': return '32px'
    default: return '24px'
  }
})

const messageSize = computed(() => {
  switch (props.size) {
    case 'small': return 'var(--font-size-sm)'
    case 'large': return 'var(--font-size-lg)'
    default: return 'var(--font-size-base)'
  }
})
const containerClasses = computed(() => [
  'loading-spinner-container',
  {
    'full-screen': props.fullScreen,
    'with-overlay': props.overlay && props.fullScreen
  }
])
</script>

<template>
  <div :class="containerClasses">
    <div class="loading-spinner"
         :style="{
           width: spinnerSize,
           height: spinnerSize
         }">
      <!-- 双层旋转动画 -->
      <div class="spinner-outer"
           :style="{
             borderColor: `${color}20`,
             borderTopColor: color
           }"></div>
      <div class="spinner-inner"
           :style="{
             borderColor: `${color}30`,
             borderBottomColor: color,
             width: iconSize,
             height: iconSize
           }"></div>
    </div>
    
    <!-- 加载提示文本 -->
    <div v-if="message"
         class="loading-message"
         :style="{
           fontSize: messageSize,
           color: color
         }">
      {{ message }}
    </div>
  </div>
</template>

<style lang="scss" scoped>
.loading-spinner-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
  gap: var(--spacing-md);
  position: relative;
  z-index: 10;
  
  &.full-screen {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    background-color: transparent;
    padding: 0;
    z-index: 1000;
    
    &.with-overlay {
      background-color: rgba(255, 255, 255, 0.9);
      backdrop-filter: blur(2px);
    }
    
    // 暗色背景下的覆盖层颜色
    @media (prefers-color-scheme: dark) {
      &.with-overlay {
        background-color: rgba(0, 0, 0, 0.8);
      }
    }
  }
}

.loading-spinner {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

// 外层旋转环
.spinner-outer {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 4px solid;
  border-radius: 50%;
  animation: spin 1.5s linear infinite;
  box-sizing: border-box;
}

// 内层旋转环
.spinner-inner {
  position: relative;
  border: 3px solid;
  border-radius: 50%;
  animation: spin-reverse 1s linear infinite;
  box-sizing: border-box;
}

// 加载文本
.loading-message {
  font-weight: 500;
  text-align: center;
  white-space: nowrap;
  opacity: 0;
  animation: fadeIn 0.3s ease-in-out 0.5s forwards;
}

// 旋转动画
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes spin-reverse {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(-360deg);
  }
}

// 淡入动画
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

// 响应式调整
@media (max-width: 768px) {
  .loading-spinner-container {
    padding: var(--spacing-md);
  }
  
  .loading-spinner {
    
    .spinner-outer {
      border-width: 3px;
    }
    
    .spinner-inner {
      border-width: 2px;
    }
  }
}
</style>
