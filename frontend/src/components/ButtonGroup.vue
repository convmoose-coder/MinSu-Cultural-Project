<template>
  <div
    :class="[
      'button-group',
      `button-group--${size}`,
      `button-group--${variant}`,
      {
        'button-group--vertical': vertical,
        'button-group--block': block,
        'button-group--gap': gap
      }
    ]"
    v-motion-slide-visible-once-bottom
    :delay="delay"
  >
    <slot />
  </div>
</template>

<script setup>
import { provide, computed } from 'vue';

// 定义组件属性
const props = defineProps({
  // 按钮组尺寸
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  // 按钮组变体
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => [
      'primary', 'secondary', 'success', 'warning', 'danger', 'info', 'ghost', 'outline'
    ].includes(value)
  },
  // 是否垂直排列
  vertical: {
    type: Boolean,
    default: false
  },
  // 是否块级显示
  block: {
    type: Boolean,
    default: false
  },
  // 按钮之间是否有间隔
  gap: {
    type: Boolean,
    default: false
  },
  // 动画延迟
  delay: {
    type: Number,
    default: 0
  }
});

// 向子组件提供上下文
provide('buttonGroup', {
  size: computed(() => props.size),
  variant: computed(() => props.variant),
  vertical: computed(() => props.vertical),
  block: computed(() => props.block),
  gap: computed(() => props.gap)
});
</script>

<style lang="scss" scoped>
@use '@/assets/styles/variables.scss' as *;
@use '@/assets/styles/theme.scss' as *;

.button-group {
  display: inline-flex;
  
  // 水平排列
  &:not(.button-group--vertical) {
    flex-direction: row;
    
    // 无间隔时，按钮紧贴
    &:not(.button-group--gap) {
      :deep(.custom-button) {
        border-radius: 0;
        
        &:first-child {
          border-top-left-radius: $border-radius-md;
          border-bottom-left-radius: $border-radius-md;
        }
        
        &:last-child {
          border-top-right-radius: $border-radius-md;
          border-bottom-right-radius: $border-radius-md;
        }
      }
    }
    
    // 有间隔时，按钮之间有间距
    &.button-group--gap {
      gap: $spacing-sm;
    }
  }
  
  // 垂直排列
  &.button-group--vertical {
    flex-direction: column;
    
    // 无间隔时，按钮紧贴
    &:not(.button-group--gap) {
      :deep(.custom-button) {
        border-radius: 0;
        
        &:first-child {
          border-top-left-radius: $border-radius-md;
          border-top-right-radius: $border-radius-md;
        }
        
        &:last-child {
          border-bottom-left-radius: $border-radius-md;
          border-bottom-right-radius: $border-radius-md;
        }
      }
    }
    
    // 有间隔时，按钮之间有间距
    &.button-group--gap {
      gap: $spacing-sm;
    }
  }
  
  // 块级显示
  &.button-group--block {
    width: 100%;
    display: flex;
    
    :deep(.custom-button) {
      flex: 1;
    }
  }
  
  // 按钮组尺寸
  &--small {
    :deep(.custom-button) {
      padding: $spacing-xs $spacing-sm;
      font-size: $font-size-sm;
      min-height: 32px;
    }
  }
  
  &--medium {
    :deep(.custom-button) {
      padding: $spacing-sm $spacing-md;
      font-size: $font-size-base;
      min-height: 40px;
    }
  }
  
  &--large {
    :deep(.custom-button) {
      padding: $spacing-md $spacing-lg;
      font-size: $font-size-lg;
      min-height: 48px;
    }
  }
}
</style>