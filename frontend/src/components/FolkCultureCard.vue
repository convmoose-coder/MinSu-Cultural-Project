<template>
  <div 
    class="folk-culture-card" 
    v-motion-slide-visible-once-bottom
    :class="{ 'is-favorited': isFavorite, 'is-loading': isLoading }"
  >
    <div class="card-image">
      <img 
        :src="culture.image || defaultImages.culture" 
        :alt="culture.name || '文化图片'" 
        @error="handleImageError"
      />
      <div class="card-category">
        <el-tag type="primary" size="small">{{ culture.category || '未分类' }}</el-tag>
      </div>
    </div>
    
    <div class="card-content">
      <h3 class="card-title">{{ culture.name || '未知文化' }}</h3>
      
      <div class="card-meta">
        <div class="meta-item">
          <el-icon><Location /></el-icon>
          <span>{{ culture.region || '未知地区' }}</span>
        </div>
        <div class="meta-item" v-if="culture.date">
          <el-icon><Calendar /></el-icon>
          <span>{{ culture.date || '未知日期' }}</span>
        </div>
      </div>
      
      <p class="card-description">{{ truncatedDescription }}</p>
      
      <div class="card-actions">
        <div class="action-buttons">
          <CustomButton 
            :variant="isFavorite ? 'danger' : 'ghost'" 
            size="small"
            icon="StarFilled"
            circle
            @click="toggleFavorite"
          />
        </div>
        <CustomButton 
          variant="primary" 
          size="small"
          icon="ArrowRight"
          @click="navigateToDetail"
        >
          查看详情
        </CustomButton>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Location, 
  Calendar, 
  ArrowRight, 
  Star,
  StarFilled
} from '@element-plus/icons-vue'
import CustomButton from './CustomButton.vue'
import defaultImages from '@/assets/images/defaultImages.js'

const props = defineProps({
  culture: {
    type: Object,
    required: true
  }
})

const router = useRouter()
const isFavorite = ref(false)
const isLoading = ref(false)

// 截取描述文本
const truncatedDescription = computed(() => {
  if (!props.culture.description) return ''
  return props.culture.description.length > 100 
    ? props.culture.description.substring(0, 100) + '...' 
    : props.culture.description
})

// 查看详情
const navigateToDetail = () => {
  // 添加加载状态
  isLoading.value = true
  
  // 模拟加载延迟
  setTimeout(() => {
    isLoading.value = false
    router.push(`/culture/${props.culture.id}`)
  }, 500)
}

// 切换收藏状态
const toggleFavorite = () => {
  isFavorite.value = !isFavorite.value
  // 这里可以添加收藏API调用
  console.log(`收藏状态: ${isFavorite.value ? '已收藏' : '未收藏'}`)
}

// 处理图片加载错误
const handleImageError = (event) => {
  event.target.src = defaultImages.culture
}


</script>

<style lang="scss" scoped>
@use '@/assets/styles/global.scss' as *;

// 直接定义变量以确保可用
$transition-base: 0.3s ease;
$transition-slow: 0.5s ease;
$danger-color: #f56565;
$spacing-sm: 8px;
$spacing-md: 16px;
$spacing-lg: 24px;
$spacing-xs: 4px;
$font-size-xl: 1.25rem;
$font-size-lg: 1.125rem;
$font-size-base: 1rem;
$font-size-sm: 0.875rem;
$text-primary: #2d3748;
$text-secondary: #718096;
$line-height-tight: 1.25;
$line-height-relaxed: 1.625;
$font-family-chinese: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
$primary-color: #3182ce;
$primary-dark: #2c5282;
$warning-color: #ed8936;

// 定义text-ellipsis-multiline混合器
@mixin text-ellipsis-multiline($lines: 2) {
  display: -webkit-box;
  -webkit-line-clamp: $lines;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.culture-card {
  @include card;
  @include card-hover;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: all $transition-base;
  position: relative;
  
  // 添加卡片悬停动画
  &:hover {
    transform: translateY(-8px);
    
    // 图片缩放效果
    .card-image img {
      transform: scale(1.05);
    }
    
    // 显示更多操作按钮
    .card-actions {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  // 添加收藏动画
  &.is-favorited {
    .favorite-icon {
      color: $danger-color;
      animation: heartBeat 0.8s ease;
    }
  }
  
  // 添加加载动画
  &.is-loading {
    pointer-events: none;
    
    .card-image::after {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(255, 255, 255, 0.7);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1;
    }
  }
}

// 心跳动画
@keyframes heartBeat {
  0% {
    transform: scale(1);
  }
  14% {
    transform: scale(1.3);
  }
  28% {
    transform: scale(1);
  }
  42% {
    transform: scale(1.3);
  }
  70% {
    transform: scale(1);
  }
}

.card-image {
  position: relative;
  height: 200px;
  overflow: hidden;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform $transition-slow;
  }
  
  .image-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 60%, rgba(0, 0, 0, 0.7) 100%);
    opacity: 0;
    transition: opacity $transition-base;
  }
  
  .favorite-btn {
    position: absolute;
    top: $spacing-sm;
    right: $spacing-sm;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.9);
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: $transition-base;
    z-index: 2;
    
    &:hover {
      background-color: white;
      transform: scale(1.1);
    }
    
    &.is-favorite {
      color: $danger-color;
    }
  }
}

.card-content {
  padding: $spacing-lg;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-header {
  margin-bottom: $spacing-md;
}

.card-title {
  font-size: $font-size-xl;
  font-weight: 600;
  color: $text-primary;
  margin: 0 0 $spacing-sm 0;
  line-height: $line-height-tight;
  font-family: $font-family-chinese;
}

.card-meta {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  color: $text-secondary;
  font-size: $font-size-sm;
  
  .meta-item {
    display: flex;
    align-items: center;
    gap: $spacing-xs;
    
    .el-icon {
      font-size: $font-size-sm;
    }
  }
}

.card-description {
  color: $text-secondary;
  font-size: $font-size-base;
  line-height: $line-height-relaxed;
  margin-bottom: $spacing-lg;
  flex: 1;
  
  @include text-ellipsis-multiline(3);
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-xs;
  margin-bottom: $spacing-lg;
}

.card-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  opacity: 0.8;
  transform: translateY(4px);
  transition: $transition-base;
  
  .action-buttons {
    display: flex;
    gap: $spacing-xs;
  }
}

.card-link {
  display: inline-flex;
  align-items: center;
  gap: $spacing-xs;
  color: $primary-color;
  font-weight: 500;
  text-decoration: none;
  font-size: $font-size-sm;
  transition: $transition-base;
  
  &:hover {
    color: $primary-dark;
    gap: $spacing-sm;
  }
}

.card-rating {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  
  .rating-value {
    font-size: $font-size-sm;
    font-weight: 500;
    color: $text-secondary;
  }
  
  .el-icon {
    color: $warning-color;
    font-size: $font-size-sm;
  }
}

// 响应式设计
@include responsive(md) {
  .card-image {
    height: 160px;
  }
  
  .card-content {
    padding: $spacing-md;
  }
  
  .card-title {
    font-size: $font-size-lg;
  }
  
  .card-description {
    font-size: $font-size-sm;
  }
}

@include responsive(sm) {
  .card-image {
    height: 140px;
  }
  
  .card-content {
    padding: $spacing-sm;
  }
  
  .card-title {
    font-size: $font-size-base;
  }
  
  .card-description {
    font-size: $font-size-sm;
  }
}
</style>
