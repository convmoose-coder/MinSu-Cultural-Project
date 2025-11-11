<template>
  <div class="modern-image">
    <img
      :src="imageSrc"
      :alt="alt"
      class="modern-image__img"
      :style="{
        objectFit: fit,
        width: '100%',
        height: '100%',
        display: 'block'
      }"
      :loading="lazy ? 'lazy' : 'eager'"
      @error="handleError"
    >
  </div>
</template>

<script>
export default {
  name: 'ModernImage',
  props: {
    src: {
      type: String,
      default: ''
    },
    alt: {
      type: String,
      default: 'Image'
    },
    fit: {
      type: String,
      default: 'cover'
    },
    lazy: {
      type: Boolean,
      default: true
    },
    defaultSrc: {
      type: String,
      default: 'traditional.jpg'
    }
  },
  computed: {
    // 获取默认图片路径
    defaultImage() {
      if (this.defaultSrc) {
        return this.defaultSrc.startsWith('/') ? this.defaultSrc : '/images/' + this.defaultSrc
      }
      return '/images/traditional.jpg'
    },
    // 获取最终图片路径
    imageSrc() {
      // 优先使用传入的src
      if (this.src && this.src.trim() !== '') {
        // 确保路径格式正确
        if (this.src.startsWith('http://') || this.src.startsWith('https://') || this.src.startsWith('/')) {
          return this.src
        }
        // 添加正确的路径前缀
        return '/images/' + this.src
      }
      
      // 如果没有提供src，使用默认图片
      return this.defaultImage
    }
  },
  methods: {
    // 错误处理函数
    handleError(event) {
      console.log('图片加载失败，尝试默认图片:', this.src)
      // 直接在元素上修改src为默认图片
      event.target.src = this.defaultImage
    }
  }
}
</script>

<style scoped>
.modern-image {
  position: relative;
  overflow: hidden;
  background-color: #f3f4f6;
  width: 100%;
  height: 100%;
}

.modern-image__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  display: block;
  transition: transform 0.3s ease;
}

.modern-image:hover .modern-image__img {
  transform: scale(1.05);
}
</style>