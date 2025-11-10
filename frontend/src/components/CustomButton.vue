<template>
  <component
    :is="tag"
    :type="tag === 'button' ? type : null"
    :href="tag === 'a' ? href : null"
    :to="tag === 'router-link' ? to : null"
    :class="[
      'custom-button',
      `custom-button--${variant}`,
      `custom-button--${size}`,
      {
        'custom-button--block': block,
        'custom-button--loading': loading,
        'custom-button--disabled': disabled,
        'custom-button--icon-only': iconOnly,
        'custom-button--circle': circle,
        'btn-animation': !disabled && !loading,
        'traditional-ripple': !disabled && !loading && variant === 'primary'
      }
    ]"
    :disabled="disabled || loading"
    @click="handleClick"
    v-motion-slide-visible-once-bottom
    :delay="delay"
  >
    <!-- 加载状态 -->
    <span v-if="loading" class="custom-button__loading">
      <el-icon class="is-loading">
        <Loading />
      </el-icon>
    </span>
    
    <!-- 图标 -->
    <span v-if="icon && !loading" class="custom-button__icon">
      <el-icon>
        <component :is="icon" />
      </el-icon>
    </span>
    
    <!-- 按钮内容 -->
    <span v-if="$slots.default && !iconOnly" class="custom-button__content">
      <slot />
    </span>
    
    <!-- 后置图标 -->
    <span v-if="suffixIcon && !loading" class="custom-button__suffix-icon">
      <el-icon>
        <component :is="suffixIcon" />
      </el-icon>
    </span>
  </component>
</template>

<script setup>
import { computed } from 'vue';
import { Loading } from '@element-plus/icons-vue';

// 定义组件属性
const props = defineProps({
  // 按钮类型
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => [
      'primary', 'secondary', 'success', 'warning', 'danger', 'info', 'ghost', 'outline'
    ].includes(value)
  },
  // 按钮尺寸
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  // 是否禁用
  disabled: {
    type: Boolean,
    default: false
  },
  // 是否加载中
  loading: {
    type: Boolean,
    default: false
  },
  // 是否块级按钮
  block: {
    type: Boolean,
    default: false
  },
  // 按钮标签类型
  tag: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'a', 'router-link'].includes(value)
  },
  // 按钮原生type
  type: {
    type: String,
    default: 'button'
  },
  // 链接地址（tag为a时使用）
  href: {
    type: String,
    default: null
  },
  // 路由地址（tag为router-link时使用）
  to: {
    type: [String, Object],
    default: null
  },
  // 图标
  icon: {
    type: [String, Object],
    default: null
  },
  // 后置图标
  suffixIcon: {
    type: [String, Object],
    default: null
  },
  // 是否只显示图标
  iconOnly: {
    type: Boolean,
    default: false
  },
  // 是否圆形按钮
  circle: {
    type: Boolean,
    default: false
  },
  // 动画延迟
  delay: {
    type: Number,
    default: 0
  }
});

// 定义事件
const emit = defineEmits(['click']);

// 处理点击事件
const handleClick = (event) => {
  if (props.disabled || props.loading) return;
  emit('click', event);
};
</script>

<style lang="scss" scoped>
@use "sass:color";
@use '@/assets/styles/variables.scss' as *;
@use '@/assets/styles/theme.scss' as *;

.custom-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: $spacing-xs;
  border: none;
  border-radius: $border-radius-md;
  font-family: inherit;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  transition: $transition-base;
  white-space: nowrap;
  user-select: none;
  outline: none;
  overflow: hidden;
  
  // 添加涟漪效果
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.5);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
    z-index: 0;
  }
  
  &:active::before {
    width: 300px;
    height: 300px;
  }
  
  // 按钮尺寸
  &--small {
    padding: $spacing-xs $spacing-sm;
    font-size: $font-size-sm;
    min-height: 32px;
    
    &.custom-button--circle {
      width: 32px;
      height: 32px;
      padding: 0;
    }
  }
  
  &--medium {
    padding: $spacing-sm $spacing-md;
    font-size: $font-size-base;
    min-height: 40px;
    
    &.custom-button--circle {
      width: 40px;
      height: 40px;
      padding: 0;
    }
  }
  
  &--large {
    padding: $spacing-md $spacing-lg;
    font-size: $font-size-lg;
    min-height: 48px;
    
    &.custom-button--circle {
      width: 48px;
      height: 48px;
      padding: 0;
    }
  }
  
  // 按钮变体
  &--primary {
    @include button-theme("primary");
  }
  
  &--secondary {
    @include button-theme("secondary");
  }
  
  &--success {
    @include button-theme("success");
  }
  
  &--warning {
    @include button-theme("warning");
  }
  
  &--danger {
    @include button-theme("danger");
  }
  
  &--info {
    @include button-theme("info");
  }
  
  &--ghost {
    @include button-theme("ghost");
  }
  
  &--outline {
    @include button-theme("outline");
  }
  
  // 块级按钮
  &--block {
    width: 100%;
    display: flex;
  }
  
  // 禁用状态
  &--disabled {
    opacity: 0.6;
    cursor: not-allowed;
    pointer-events: none;
  }
  
  // 加载状态
  &--loading {
    pointer-events: none;
    
    .custom-button__content {
      opacity: 0.7;
    }
  }
  
  // 只显示图标
  &--icon-only {
    padding: $spacing-sm;
    min-width: auto;
    
    &.custom-button--small {
      width: 32px;
      height: 32px;
    }
    
    &.custom-button--medium {
      width: 40px;
      height: 40px;
    }
    
    &.custom-button--large {
      width: 48px;
      height: 48px;
    }
  }
  
  // 圆形按钮
  &--circle {
    border-radius: $border-radius-full;
  }
  
  // 子元素样式
  &__loading {
    display: flex;
    align-items: center;
    justify-content: center;
    animation: rotating 2s linear infinite;
  }
  
  &__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    
    .el-icon {
      font-size: 1em;
    }
  }
  
  &__content {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  &__suffix-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    
    .el-icon {
      font-size: 0.9em;
    }
  }
  
  // 悬停效果
  &:hover:not(.custom-button--disabled):not(.custom-button--loading) {
    transform: translateY(-2px);
    box-shadow: $shadow-lg;
    
    // 为不同变体添加悬停效果
    &.custom-button--primary {
      background-color: color.adjust($primary-color, $lightness: 5%);
    }
    
    &.custom-button--secondary {
      background-color: color.adjust($secondary-color, $lightness: 5%);
    }
    
    &.custom-button--success {
      background-color: color.adjust($success, $lightness: 5%);
    }
    
    &.custom-button--warning {
      background-color: color.adjust($warning, $lightness: 5%);
    }
    
    &.custom-button--danger {
      background-color: color.adjust($danger, $lightness: 5%);
    }
    
    &.custom-button--info {
      background-color: color.adjust($info, $lightness: 5%);
    }
    
    &.custom-button--outline {
      color: $primary-color;
      background-color: rgba($primary-color, 0.1);
    }
    
    &.custom-button--ghost {
      color: $primary-color;
      background-color: rgba($primary-color, 0.05);
    }
  }
  
  // 活跃状态 - 增强点击反馈
  &:active:not(.custom-button--disabled):not(.custom-button--loading) {
    transform: translateY(0) scale(0.98);
    box-shadow: $shadow-sm;
    transition: all $transition-fast;
  }
  
  // 焦点状态增强
  &:focus-visible {
    outline: 2px solid $primary-color;
    outline-offset: 2px;
    box-shadow: 0 0 0 3px rgba($primary-color, 0.1);
  }
  
  // 传统风格按钮变体
  &--primary {
    position: relative;
    overflow: hidden;
    
    &::after {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(45deg, transparent 48%, rgba(255,255,255,0.3) 48%, rgba(255,255,255,0.3) 52%, transparent 52%);
      background-size: 10px 10px;
      opacity: 0;
      transition: opacity $transition-base;
    }
    
    &:hover::after {
      opacity: 0.6;
    }
  }
  
  // 焦点状态
  &:focus-visible {
    outline: 2px solid $primary-color;
    outline-offset: 2px;
  }
  

}

// 旋转动画
@keyframes rotating {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>