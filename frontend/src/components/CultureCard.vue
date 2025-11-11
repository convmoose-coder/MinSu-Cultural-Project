<template>
  <div class="culture-card" :class="{ 'culture-card--expanded': expanded }" @mouseenter="onHover" @mouseleave="onLeave" @click="handleExplore">
    <div class="culture-card__image-container">
      <ModernImage
        :src="image"
        :alt="title"
        fit="cover"
        :default-src="'traditional.jpg'"
      />

      <div v-if="popularity" class="culture-card__popularity-badge">
        <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
        </svg>
        {{ popularity }}
      </div>
    </div>
    <div class="culture-card__content">
      <h3 class="culture-card__title">{{ title }}</h3>
      <p class="culture-card__subtitle">{{ subtitle }}</p>
      <div v-if="tags && tags.length > 0" class="culture-card__tags">
        <span v-for="tag in tags" :key="tag" class="culture-card__tag" :style="{ borderColor: tagColor, color: tagColor }">
          {{ tag }}
        </span>
      </div>
      <p class="culture-card__description" :class="{ 'culture-card__description--truncated': !expanded }">
        {{ description }}
      </p>

    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import ModernImage from './ModernImage.vue'
import ModernButton from './ModernButton.vue'

export default {
  name: 'CultureCard',
  components: {
    ModernImage,
    ModernButton
  },
  props: {
    id: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      required: true
    },
    image: {
      type: String,
      default: ''
    },
    category: {
      type: String,
      required: true
    },
    tags: {
      type: Array,
      default: () => []
    },
    tagColor: {
      type: String,
      default: '#3b82f6'
    },
    popularity: {
      type: Number,
      default: 0
    },
    author: {
      type: String,
      default: ''
    },
    region: {
      type: String,
      default: '未知地区'
    },
    views: {
      type: Number,
      default: 0
    },
    defaultImage: {
      type: String,
      default: 'traditional.jpg'
    }
  },
  emits: ['explore'],
  setup(props, { emit }) {
    const expanded = ref(false)
    const hoverEffect = ref({ scale: 1, boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' })

    const onHover = () => {
      hoverEffect.value = {
        scale: 1.02,
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
      }
    }

    const onLeave = () => {
      hoverEffect.value = {
        scale: 1,
        boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
      }
    }

    const handleExplore = () => {
      emit('explore', props.id)
    }
    
    // 点击卡片也触发探索
    const toggleExpanded = () => {
      expanded.value = !expanded.value
    }

    return {
      expanded,
      hoverEffect,
      onHover,
      onLeave,
      handleExplore,
      toggleExpanded
    }
  }
}
</script>

<style lang="scss" scoped>
.culture-card {
  background: white;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  }

  &--expanded .culture-card__description {
    display: block;
  }

  &__image-container {
    position: relative;
    width: 100%;
    height: 200px;
    overflow: hidden;
  }

  &__category-badge {
    position: absolute;
    top: 1rem;
    left: 1rem;
    background: rgba(255, 255, 255, 0.9);
    color: #374151;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    backdrop-filter: blur(4px);
  }
  
  &__popularity-badge {
    position: absolute;
    top: 1rem;
    right: 1rem;
    background: rgba(255, 193, 7, 0.9);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    display: flex;
    align-items: center;
    backdrop-filter: blur(4px);
    animation: pulse 2s infinite;
  }
  
  @keyframes pulse {
    0% {
      box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.7);
    }
    70% {
      box-shadow: 0 0 0 6px rgba(255, 193, 7, 0);
    }
    100% {
      box-shadow: 0 0 0 0 rgba(255, 193, 7, 0);
    }
  }

  &__content {
    padding: 1.5rem;
  }

  &__title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #111827;
    margin: 0 0 0.25rem 0;
    transition: color 0.2s ease;

    .culture-card:hover & {
      color: #3b82f6;
    }
  }

  .culture-card__subtitle {
    font-size: 0.875rem;
    color: #6b7280;
    margin: 0 0 0.75rem 0;
  }
  
  .culture-card__tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
  }
  
  .culture-card__tag {
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.25rem 0.5rem;
    border-radius: 9999px;
    border: 1px solid;
    background: transparent;
  }

  &__description {
    font-size: 0.875rem;
    color: #4b5563;
    line-height: 1.6;
    margin: 0 0 1.5rem 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;

    &--truncated {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  }

  &__footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__meta {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 0.75rem;
    color: #9ca3af;
  }

  &__divider {
    width: 1px;
    height: 12px;
    background-color: #e5e7eb;
  }

  &__region,
  &__author {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }

  &__views {
    display: flex;
    align-items: center;
    gap: 0.25rem;
  }
}

// 响应式调整
@media (max-width: 640px) {
  .culture-card {
    &__image-container {
      height: 160px;
    }

    &__content {
      padding: 1rem;
    }
    
    &__tags {
      gap: 0.25rem;
    }
    
    &__tag {
      font-size: 0.6875rem;
      padding: 0.125rem 0.375rem;
    }
  }
}
</style>