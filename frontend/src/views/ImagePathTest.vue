<template>
  <div class="image-path-test">
    <h1>图片路径测试</h1>
    
    <!-- 直接使用绝对路径的原生img标签 -->
    <div class="test-case">
      <h3>1. 原生img绝对路径测试</h3>
      <img src="/images/traditional.jpg" alt="原生img绝对路径" style="width: 200px; height: 150px; border: 1px solid #ccc;" />
    </div>
    
    <!-- 使用相对路径的原生img标签 - 注意：在Vite项目中，public目录下的资源应该使用绝对路径 -->
    <div class="test-case">
      <h3>2. 原生img相对路径测试（不推荐）</h3>
      <img src="/images/traditional.jpg" alt="修正后的路径" style="width: 200px; height: 150px; border: 1px solid #ccc;" />
      <p class="path-info">正确路径: /images/traditional.jpg</p>
    </div>
    
    <!-- 额外的相对路径测试 -->
    <div class="test-case">
      <h3>2.1 相对路径示例（会失败）</h3>
      <img src="../public/images/traditional.jpg" alt="错误的相对路径" style="width: 200px; height: 150px; border: 1px solid #ccc;" />
      <p class="path-info">错误路径: ../public/images/traditional.jpg (Vite不支持这种访问方式)</p>
    </div>
    
    <!-- ModernImage使用文件名 -->
    <div class="test-case">
      <h3>3. ModernImage使用文件名</h3>
      <ModernImage src="traditional.jpg" alt="ModernImage文件名" style="width: 200px; height: 150px; border: 1px solid #ccc;" />
    </div>
    
    <!-- ModernImage使用绝对路径 -->
    <div class="test-case">
      <h3>4. ModernImage使用绝对路径</h3>
      <ModernImage src="/images/traditional.jpg" alt="ModernImage绝对路径" style="width: 200px; height: 150px; border: 1px solid #ccc;" />
    </div>
    
    <!-- ModernImage默认图片测试 -->
    <div class="test-case">
      <h3>5. ModernImage默认图片</h3>
      <ModernImage src="" alt="ModernImage默认图片" style="width: 200px; height: 150px; border: 1px solid #ccc;" />
    </div>
  </div>
</template>

<script>
import ModernImage from '../components/ModernImage.vue'

export default {
  name: 'ImagePathTest',
  components: {
    ModernImage
  }
}
</script>

<style scoped>
.image-path-test {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.test-case {
  margin-bottom: 30px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

h3 {
  margin-bottom: 10px;
  color: #333;
}

.path-info {
  font-size: 12px;
  color: #666;
  margin-top: 8px;
  background-color: #fff;
  padding: 5px;
  border-radius: 4px;
}
</style>