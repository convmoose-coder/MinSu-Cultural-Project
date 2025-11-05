<template>
  <div class="culture-card">
    <h3 class="card-title">{{ culture.title }}</h3>
    <div class="card-meta">
      <span class="region">{{ culture.region }}</span>
      <span class="category">{{ culture.category }}</span>
    </div>
    <p class="card-description">{{ truncateDescription(culture.description, 100) }}</p>
    <router-link :to="`/culture/${culture.id}`" class="card-link">
      查看详情
    </router-link>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// 组件属性
const props = defineProps({
  culture: {
    type: Object,
    required: true,
    default: () => ({
      id: 0,
      title: '',
      description: '',
      region: '',
      category: ''
    })
  }
})

// 工具函数：截断描述文本
const truncateDescription = (text, maxLength) => {
  if (!text || text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}
</script>

<style scoped>
.culture-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.culture-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.card-title {
  font-size: 1.25rem;
  color: #333;
  margin: 0 0 0.75rem 0;
  line-height: 1.4;
}

.card-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.region {
  background-color: #f0f0f0;
  color: #666;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
}

.category {
  background-color: #C8102E;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-weight: 500;
}

.card-description {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  flex-grow: 1;
}

.card-link {
  display: inline-block;
  color: #C8102E;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  align-self: flex-start;
  position: relative;
  padding-right: 1.25rem;
}

.card-link::after {
  content: '→';
  position: absolute;
  right: 0;
  transition: transform 0.3s ease;
}

.card-link:hover {
  color: #a60c23;
}

.card-link:hover::after {
  transform: translateX(3px);
}
</style>
