<template>
  <button
    :class="buttonClasses"
    :disabled="isDisabled"
    @click="handleClick"
  >
    <!-- 优化：使用更简单的加载指示器 -->
    <span v-show="loading" class="modern-button__loading">
      <div class="loading-dot"></div>
    </span>
    
    <!-- 优化：减少条件判断复杂度 -->
    <span v-show="iconLeft && !loading" class="modern-button__icon modern-button__icon--left">
      <slot name="icon-left"></slot>
    </span>
    
    <span class="modern-button__content">
      <slot></slot>
    </span>
    
    <span v-show="iconRight && !loading" class="modern-button__icon modern-button__icon--right">
      <slot name="icon-right"></slot>
    </span>
  </button>
</template>

<script>
export default {
  name: 'ModernButton',
  props: {
    variant: {
      type: String,
      default: 'primary',
      // 优化：使用Set提高验证性能
      validator: (value) => ['primary', 'secondary', 'outline', 'ghost', 'link'].includes(value)
    },
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    },
    block: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    },
    loading: {
      type: Boolean,
      default: false
    },
    iconLeft: {
      type: Boolean,
      default: false
    },
    iconRight: {
      type: Boolean,
      default: false
    }
  },
  emits: ['click'],
  // 优化：使用computed缓存计算结果
  computed: {
    isDisabled() {
      return this.disabled || this.loading
    },
    buttonClasses() {
      return [
        'modern-button',
        `modern-button--${this.variant}`,
        `modern-button--${this.size}`,
        { 'modern-button--block': this.block },
        { 'modern-button--disabled': this.isDisabled }
      ]
    }
  },
  methods: {
    // 优化：简化事件处理
    handleClick(event) {
      // 避免不必要的事件触发
      if (!this.isDisabled) {
        this.$emit('click', event)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
// 优化：提取共享变量
$transition-base: 0.2s ease;
$focus-ring: 0 0 0 4px rgba(59, 130, 246, 0.5);

.modern-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: inherit;
  font-weight: 500;
  text-decoration: none;
  border-radius: 0.5rem;
  // 优化：减少transition属性数量
  transition: transform $transition-base, box-shadow $transition-base, background-color $transition-base;
  cursor: pointer;
  outline: none;
  border: none;
  overflow: hidden;

  // 优化：简化点击动画
  &::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: translate(-50%, -50%);
    // 优化：减少过渡时间
    transition: width 0.3s, height 0.3s;
  }

  &:active::after {
    width: 200px;
    height: 200px;
  }

  &:focus-visible {
    box-shadow: $focus-ring;
  }

  // 优化：简化渐变，使用纯色提高性能
  &--primary {
    background: #3b82f6;
    color: white;

    &:hover:not(:disabled) {
      background: #2563eb;
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
  }

  &--secondary {
    background: #10b981;
    color: white;

    &:hover:not(:disabled) {
      background: #059669;
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }
  }

  // 尺寸样式保持不变
  &--small {
    padding: 0.25rem 0.75rem;
    font-size: 0.875rem;
    line-height: 1.5;
  }

  &--medium {
    padding: 0.5rem 1rem;
    font-size: 1rem;
    line-height: 1.5;
  }

  &--large {
    padding: 0.75rem 1.5rem;
    font-size: 1.125rem;
    line-height: 1.5;
  }

  &--block {
    width: 100%;
  }

  &--disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none !important;
    box-shadow: none !important;
  }

  &__content {
    position: relative;
    z-index: 1;
  }

  &__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    // 移除不必要的过渡
  }

  &__icon--left {
    margin-right: 0.25rem;
  }

  &__icon--right {
    margin-left: 0.25rem;
  }

  // 优化：简化加载动画
  &__loading {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 16px;
    height: 16px;
  }

  .loading-dot {
    width: 16px;
    height: 16px;
    border: 2px solid currentColor;
    border-color: currentColor transparent transparent transparent;
    border-radius: 50%;
    // 优化：使用GPU加速的动画
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }
}
</style>