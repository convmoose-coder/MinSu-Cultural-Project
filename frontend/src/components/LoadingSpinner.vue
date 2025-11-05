<template>
  <div class="loading-container" :class="{ 'full-screen': fullScreen }">
    <div class="loading-spinner"></div>
    <p v-if="message" class="loading-message">{{ message }}</p>
  </div>
</template>

<script setup>
// 组件属性
const props = defineProps({
  // 是否全屏显示加载状态
  fullScreen: {
    type: Boolean,
    default: false
  },
  // 加载提示信息
  message: {
    type: String,
    default: '加载中...'
  }
})
</script>

<style scoped>
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  gap: 1rem;
}

.loading-container.full-screen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.9);
  z-index: 9999;
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #f0e6d2;
  border-top: 4px solid #C8102E;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  position: relative;
}

.loading-message {
  color: #666;
  font-size: 1rem;
  margin: 0;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
