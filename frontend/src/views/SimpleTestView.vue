<template>
  <div class="simple-test-container">
    <h1>简单默认图片测试</h1>
    
    <div class="test-item">
      <h2>空字符串测试</h2>
      <ModernImage 
        src="" 
        alt="空字符串测试"
        :default-src="'culture.jpg'"
        fit="cover"
        style="width: 300px; height: 200px; border: 1px solid #ccc;"
      />
    </div>
    
    <div class="test-item">
      <h2>null值测试</h2>
      <ModernImage 
        :src="null" 
        alt="null值测试"
        :default-src="'culture.jpg'"
        fit="cover"
        style="width: 300px; height: 200px; border: 1px solid #ccc;"
      />
    </div>
    
    <div class="test-item">
      <h2>直接使用默认图片</h2>
      <img 
        src="/images/placeholder-culture.jpg" 
        alt="直接使用默认图片"
        style="width: 300px; height: 200px; border: 1px solid #ccc;"
      />
    </div>
    
    <div class="test-item">
      <h2>ModernImage使用本地图片路径</h2>
      <ModernImage 
        src="traditional.jpg" 
        alt="ModernImage使用本地图片"
        fit="cover"
        style="width: 300px; height: 200px; border: 1px solid #ccc;"
      />
    </div>
  </div>
</template>

<script>
import ModernImage from '../components/ModernImage.vue'

export default {
  name: 'SimpleTestView',
  components: {
    ModernImage
  }
}
</script>

<style scoped>
.simple-test-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.test-item {
  margin-bottom: 30px;
}

.test-item h2 {
  margin-bottom: 10px;
}
</style>