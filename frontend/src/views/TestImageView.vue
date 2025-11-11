<template>
  <div class="test-container">
    <h1>ModernImage组件测试</h1>
    
    <div class="test-section">
      <h2>1. 正常图片路径测试</h2>
      <div class="image-grid">
        <div class="test-item">
          <h3>绝对路径</h3>
          <ModernImage 
            src="/images/placeholder-culture.jpg" 
            alt="测试图片1"
            :default-src="'culture.jpg'"
            fit="cover"
          />
        </div>
        
        <div class="test-item">
          <h3>相对路径</h3>
          <ModernImage 
            src="placeholder-culture.jpg" 
            alt="测试图片2"
            :default-src="'culture.jpg'"
            fit="cover"
          />
        </div>
      </div>
    </div>
    
    <div class="test-section">
      <h2>2. 空路径测试（应显示默认图片）</h2>
      <div class="image-grid">
        <div class="test-item">
          <h3>空字符串</h3>
          <ModernImage 
            src="" 
            alt="测试图片3"
            :default-src="'culture.jpg'"
            fit="cover"
          />
        </div>
        
        <div class="test-item">
          <h3>null值</h3>
          <ModernImage 
            :src="null" 
            alt="测试图片4"
            :default-src="'culture.jpg'"
            fit="cover"
          />
        </div>
        
        <div class="test-item">
          <h3>undefined值</h3>
          <ModernImage 
            :src="undefined" 
            alt="测试图片5"
            :default-src="'culture.jpg'"
            fit="cover"
          />
        </div>
      </div>
    </div>
    
    <div class="test-section">
      <h2>3. 无效路径测试（应显示默认图片）</h2>
      <div class="image-grid">
        <div class="test-item">
          <h3>不存在的文件</h3>
          <ModernImage 
            src="/images/not-exist.jpg" 
            alt="测试图片6"
            :default-src="'culture.jpg'"
            fit="cover"
          />
        </div>
        
        <div class="test-item">
          <h3>无效URL</h3>
          <ModernImage 
            src="invalid-path" 
            alt="测试图片7"
            :default-src="'culture.jpg'"
            fit="cover"
          />
        </div>
      </div>
    </div>
    
    <div class="test-section">
      <h2>4. 不同默认图片测试</h2>
      <div class="image-grid">
        <div class="test-item">
          <h3>默认culture.jpg</h3>
          <ModernImage 
            src="" 
            alt="测试图片8"
            :default-src="'culture.jpg'"
            fit="cover"
          />
        </div>
        
        <div class="test-item">
          <h3>默认traditional.jpg</h3>
          <ModernImage 
            src="" 
            alt="测试图片9"
            :default-src="'traditional.jpg'"
            fit="cover"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ModernImage from '../components/ModernImage.vue'

export default {
  name: 'TestImageView',
  components: {
    ModernImage
  }
}
</script>

<style scoped>
.test-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.test-section {
  margin-bottom: 40px;
}

.test-section h2 {
  margin-bottom: 20px;
  color: #333;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.test-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  background-color: #f9f9f9;
}

.test-item h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 16px;
  color: #555;
}

.test-item .modern-image {
  height: 200px;
  border-radius: 4px;
}
</style>