<template>
  <div class="region-card" :style="cardStyle" @click="handleClick">
    <ModernImage
      :src="image"
      :alt="name"
      fit="cover"
      :default-src="'traditional.jpg'"
    />
    <div class="region-card__gradient-overlay"></div>
    <div class="region-card__content">
      <span class="region-card__tag">{{ tag || '地区文化' }}</span>
      <h3 class="region-card__title">{{ name }}</h3>
      <p class="region-card__subtitle">{{ description }}</p>
      <div class="region-card__stats">
        <span class="region-card__stat-item">
          {{ cultureCount }} 项文化
        </span>
      </div>

    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import ModernImage from './ModernImage.vue'

export default {
  name: 'RegionCard',
  components: {
    ModernImage
  },
  props: {
    id: {
      type: [Number, String],
      required: true
    },
    name: {
      type: String,
      required: true
    },
    description: {
      type: String,
      default: '暂无描述'
    },
    cultureCount: {
      type: Number,
      default: 0
    },
    image: {
      type: String,
      default: ''
    },
    tag: {
      type: String,
      default: ''
    },
    gradientFrom: {
      type: String,
      default: 'from-black/70'
    },
    gradientTo: {
      type: String,
      default: 'to-transparent'
    },
    defaultImage: {
      type: String,
      default: 'traditional.jpg'
    }
  },
  emits: ['click'],
  setup(props, { emit }) {
    const cardStyle = computed(() => ({
      '--gradient-from': props.gradientFrom,
      '--gradient-to': props.gradientTo
    }))

    const handleClick = () => {
      emit('click', props.id)
    }

    return {
      cardStyle,
      handleClick
    }
  }
}
</script>

<style lang="scss" scoped>
.region-card {
  position: relative;
  border-radius: 1rem;
  overflow: hidden;
  height: 360px;
  cursor: pointer;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);

  &:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  }

  &__gradient-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, var(--gradient-from, from-black/70), var(--gradient-to, to-transparent));
    z-index: 1;
  }

  &__content {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 2rem;
    z-index: 2;
    transform: translateY(20px);
    opacity: 0;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);

    .region-card:hover & {
      transform: translateY(0);
      opacity: 1;
    }
  }

  &__tag {
    display: inline-block;
    background: rgba(255, 255, 255, 0.9);
    color: #374151;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    margin-bottom: 1rem;
    backdrop-filter: blur(4px);
  }

  &__title {
    font-size: 2rem;
    font-weight: 800;
    color: white;
    margin: 0 0 0.5rem 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  &__subtitle {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.9);
    margin: 0 0 1rem 0;
    max-width: 80%;
    line-height: 1.5;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
  }

  &__stats {
    margin-bottom: 1.5rem;
    
    &-item {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 0.875rem;
      color: rgba(255, 255, 255, 0.8);
      background: rgba(0, 0, 0, 0.3);
      padding: 0.25rem 0.75rem;
      border-radius: 9999px;
    }
  }

  &__action {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: white;
    font-weight: 500;
    font-size: 0.875rem;
    padding: 0.5rem 1rem;
    background: rgba(59, 130, 246, 0.9);
    border-radius: 0.5rem;
    transition: all 0.3s ease;

    .region-card:hover & {
      background: rgba(59, 130, 246, 1);
      transform: translateX(4px);
    }
  }

  &__arrow {
    transition: transform 0.3s ease;

    .region-card:hover & {
      transform: translateX(2px);
    }
  }
}

// 响应式调整
@media (max-width: 768px) {
  .region-card {
    height: 300px;

    &__content {
      padding: 1.5rem;
    }

    &__title {
      font-size: 1.5rem;
    }

    &__subtitle {
      font-size: 0.875rem;
      max-width: 90%;
    }
  }
}

@media (max-width: 640px) {
  .region-card {
    height: 250px;

    &__content {
      padding: 1.25rem;
    }

    &__title {
      font-size: 1.25rem;
    }

    &__subtitle {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  }
}
</style>