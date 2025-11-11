<template>
  <button
    :class="[
      'modern-button',
      `modern-button--${variant}`,
      `modern-button--${size}`,
      { 'modern-button--block': block },
      { 'modern-button--disabled': disabled || loading }
    ]"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <span v-if="loading" class="modern-button__loading">
      <svg class="animate-spin -ml-1 mr-3 h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </span>
    <span v-if="iconLeft && !loading" class="modern-button__icon modern-button__icon--left">
      <slot name="icon-left"></slot>
    </span>
    <span class="modern-button__content">
      <slot></slot>
    </span>
    <span v-if="iconRight && !loading" class="modern-button__icon modern-button__icon--right">
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
  methods: {
    handleClick(event) {
      this.$emit('click', event)
    }
  }
}
</script>

<style lang="scss" scoped>
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
  transition: all 0.3s ease;
  cursor: pointer;
  outline: none;
  border: none;
  overflow: hidden;

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
    transition: width 0.6s, height 0.6s;
  }

  &:active::after {
    width: 300px;
    height: 300px;
  }

  &:focus-visible {
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.5);
  }

  &--primary {
    background: linear-gradient(135deg, #3b82f6, #60a5fa);
    color: white;

    &:hover:not(:disabled) {
      background: linear-gradient(135deg, #2563eb, #3b82f6);
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
  }

  &--secondary {
    background: linear-gradient(135deg, #10b981, #34d399);
    color: white;

    &:hover:not(:disabled) {
      background: linear-gradient(135deg, #059669, #10b981);
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }
  }

  &--outline {
    background: transparent;
    border: 2px solid #3b82f6;
    color: #3b82f6;

    &:hover:not(:disabled) {
      background: rgba(59, 130, 246, 0.1);
      transform: translateY(-1px);
    }
  }

  &--ghost {
    background: transparent;
    color: inherit;

    &:hover:not(:disabled) {
      background: rgba(0, 0, 0, 0.05);
      transform: translateY(-1px);
    }
  }

  &--link {
    background: transparent;
    color: #3b82f6;
    text-decoration: underline;
    padding: 0;

    &:hover:not(:disabled) {
      color: #2563eb;
      transform: none;
      box-shadow: none;
    }
  }

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
    transition: transform 0.2s ease;

    &--left {
      margin-right: 0.25rem;
    }

    &--right {
      margin-left: 0.25rem;

      .modern-button:hover & {
        transform: translateX(2px);
      }
    }
  }

  &__loading {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>