<script setup>
// 关于我们页面的逻辑
</script>

<template>
  <div class="about-view">
    <div class="about-header">
      <h1>关于我们</h1>
    </div>
    
    <div class="about-content">
      <section class="mission touch-feedback">
        <h2>我们的使命</h2>
        <p>乘灼致力于收集、整理和展示中华大地上丰富多彩的民族文化资源，让更多的人了解和传承中华优秀传统文化。我们希望通过数字技术，打破地域和时间的限制，让珍贵的民族文化得以保存和传播。</p>
      </section>
      
      <section class="vision touch-feedback">
        <h2>我们的愿景</h2>
        <p>乘灼数字平台，连接传统与现代，促进民族文化交流与传承，让民族文化在新时代焕发新的生机。</p>
      </section>
      
      <section class="features touch-feedback">
        <h2>网站特色</h2>
        <div class="feature-list">
          <div class="feature-item touch-feedback">
            <h3>丰富的内容资源</h3>
            <p>涵盖全国各地的民族文化，包括传统节日、民间艺术、饮食习惯、服饰文化等多个方面。</p>
          </div>
          
          <div class="feature-item touch-feedback">
            <h3>地区分类浏览</h3>
            <p>按地区查看不同地方的特色民俗，感受中国文化的多样性和丰富性。</p>
          </div>
          
          <div class="feature-item touch-feedback">
            <h3>深度文化解析</h3>
            <p>提供详尽的民族文化解析，帮助用户深入了解文化背后的历史和意义。</p>
          </div>
        </div>
      </section>
      
      <section class="contact touch-feedback">
        <h2>联系我们</h2>
        <p>如果您有任何问题、建议或合作意向，欢迎随时与我们联系。我们期待与您一起，为传承和弘扬中华优秀传统文化贡献力量。</p>
        <div class="contact-info">
          <p><strong>邮箱：</strong>contact@chengzhuo.com</p>
          <p><strong>电话：</strong>400-123-4567</p>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.about-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 0;
  /* 添加触摸滑动时的优化 */
  -webkit-overflow-scrolling: touch;
  overflow-x: hidden;
  /* 添加触摸反馈 */
  touch-action: manipulation;
}

.about-header {
  text-align: center;
  margin-bottom: 3rem;
  padding: 3rem 1rem;
  background-color: #8B4513;
  color: white;
  border-radius: 8px;
  margin: 0 1rem 3rem;
  /* 添加触摸反馈 */
  touch-action: manipulation;
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  transition: transform 0.1s ease;
  position: relative;
}

.about-header:active {
  transform: scale(0.98);
}

.about-header h1 {
  font-size: 2.8rem;
  margin: 0;
}

.about-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 1rem;
}

.about-content section {
  margin-bottom: 3rem;
  padding: 2.5rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative; /* 为伪元素提供定位上下文 */
}

.about-content section:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.about-content h2 {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #8B4513;
  border-bottom: 3px solid #8B4513;
  padding-bottom: 0.75rem;
}

.about-content p {
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: 1rem;
  color: #444;
}

.feature-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  /* 为整个网格添加触摸优化 */
  touch-action: manipulation;
}

.feature-item {
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #8B4513;
  position: relative; /* 为伪元素提供定位上下文 */
}

.feature-item h3 {
  color: #8B4513;
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.contact-info {
  margin-top: 2rem;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.contact-info p {
  margin: 0.75rem 0;
  font-weight: 500;
}

/* 触摸动画效果 */
.touch-feedback {
  /* 添加触摸反馈 */
  touch-action: manipulation;
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  -webkit-tap-highlight-color: transparent; /* 移除默认的高亮效果 */
  position: relative; /* 为伪元素提供定位上下文 */
}

.touch-feedback:active {
  transform: scale(0.97);
  transition: transform 0.1s ease;
}

/* 添加触摸时的高亮效果 */
.touch-feedback::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(139, 69, 19, 0.1);
  opacity: 0;
  transition: opacity 0.2s;
  border-radius: 8px;
  pointer-events: none;
}

.touch-feedback:active::before {
  opacity: 1;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .about-header {
    padding: 2rem 1rem;
  }
  
  .about-header h1 {
    font-size: 2rem;
  }
  
  .about-content section {
    padding: 1.5rem;
  }
  
  .about-content h2 {
    font-size: 1.6rem;
  }
  
  .feature-list {
    grid-template-columns: 1fr;
  }
}
</style>