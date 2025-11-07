<template>
  <div class="region-card">
    <div class="region-image">
      <img :src="image" :alt="name" @error="handleImageError" />
    </div>
    <div class="region-content">
      <h3 class="region-name">{{ name }}</h3>
      <p class="region-description">{{ description }}</p>
      <div class="region-stats">
        <span class="stat-item">
          <el-icon><Document /></el-icon>
          {{ cultureCount }} 项文化
        </span>
      </div>
    </div>
  </div>
</template>

<script>
import { Document } from '@element-plus/icons-vue'
import defaultImages from '@/assets/images/defaultImages.js'

export default {
  name: 'RegionCard',
  components: {
    Document
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
    }
  },
  methods: {
    handleImageError(event) {
      event.target.src = defaultImages.region
    }
  }
}
</script>

<style lang="scss" scoped>
.region-card {
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  }
  
  .region-image {
    height: 200px;
    overflow: hidden;
    
    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.5s ease;
    }
  }
  
  &:hover .region-image img {
    transform: scale(1.05);
  }
  
  .region-content {
    padding: 16px;
    
    .region-name {
      font-size: 20px;
      font-weight: 600;
      color: #2d3748;
      margin-bottom: 8px;
    }
    
    .region-description {
      color: #718096;
      margin-bottom: 16px;
      line-height: 1.75;
    }
    
    .region-stats {
      display: flex;
      align-items: center;
      gap: 8px;
      
      .stat-item {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 14px;
        color: #4a5568;
      }
    }
  }
}
</style>