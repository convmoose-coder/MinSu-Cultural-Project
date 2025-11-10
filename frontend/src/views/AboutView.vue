<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { createLogger } from '../utils/logger'

// 创建日志实例
const logger = createLogger('AboutView');

// 动画控制
const sections = ref<HTMLElement[]>([])

onMounted(() => {
  logger.info('AboutView组件已挂载');
  
  // 初始化观察器以实现滚动动画
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
        }
      });
    },
    { threshold: 0.1 }
  );
  
  // 观察所有section元素
  sections.value = Array.from(document.querySelectorAll('.about-section'));
  sections.value.forEach(section => {
    observer.observe(section);
  });
  
  // 清理函数
  return () => {
    sections.value.forEach(section => {
      observer.unobserve(section);
    });
  };
});
</script>

<template>
  <section class="about-view">
    <!-- 页面头部 -->
    <div class="about-hero">
      <div class="about-hero-content">
        <h1 class="about-hero-title">关于我们</h1>
        <p class="about-hero-subtitle">传承中华优秀传统文化，连接传统与现代</p>
      </div>
    </div>
    
    <!-- 主要内容 -->
    <div class="about-content">
      <!-- 使命部分 -->
      <section class="about-section mission">
        <div class="section-icon">🎯</div>
        <h2 class="section-title">我们的使命</h2>
        <div class="section-content">
          <p>中国民俗文化网致力于收集、整理和展示中华大地上丰富多彩的民俗文化资源，让更多的人了解和传承中华优秀传统文化。我们希望通过数字技术，打破地域和时间的限制，让珍贵的民俗文化得以保存和传播。</p>
        </div>
      </section>
      <!-- 愿景部分 -->
      <section class="about-section vision">
        <div class="section-icon">🌟</div>
        <h2 class="section-title">我们的愿景</h2>
        <div class="section-content">
          <p>成为中国最具影响力的民俗文化数字平台，连接传统与现代，促进文化交流与传承，让民俗文化在新时代焕发新的生机。</p>
        </div>
      </section>
      <!-- 网站特色 -->
      <section class="about-section features">
        <div class="section-icon">✨</div>
        <h2 class="section-title">网站特色</h2>
        <div class="feature-grid">
          <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3 class="feature-title">丰富的内容资源</h3>
            <p class="feature-description">涵盖全国各地的民俗文化，包括传统节日、民间艺术、饮食习惯、服饰文化等多个方面。</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🗺️</div>
            <h3 class="feature-title">地区分类浏览</h3>
            <p class="feature-description">按地区查看不同地方的特色民俗，感受中国文化的多样性和丰富性。</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3 class="feature-title">深度文化解析</h3>
            <p class="feature-description">提供详尽的民俗文化解析，帮助用户深入了解文化背后的历史和意义。</p>
          </div>
        </div>
      </section>
      <!-- 团队介绍 -->
      <section class="about-section team">
        <div class="section-icon">👥</div>
        <h2 class="section-title">我们的团队</h2>
        <div class="section-content">
          <p>我们是一支热爱中国传统文化的专业团队，由文化学者、技术专家和设计师组成。我们致力于通过现代化的方式，让传统文化焕发新的生命力。</p>
        </div>
      </section>
      <!-- 联系我们 -->
      <section class="about-section contact">
        <div class="section-icon">📞</div>
        <h2 class="section-title">联系我们</h2>
        <div class="section-content">
          <p>如果您有任何问题、建议或合作意向，欢迎随时与我们联系。我们期待与您一起，为传承和弘扬中华优秀传统文化贡献力量。</p>
          <div class="contact-info">
            <a href="mailto:contact@minsu.com" class="contact-item">
              <span class="contact-icon">✉️</span>
              <span class="contact-text">contact@minsu.com</span>
            </a>
            <a href="tel:4001234567" class="contact-item">
              <span class="contact-icon">☎️</span>
              <span class="contact-text">400-123-4567</span>
            </a>
          </div>
          <button class="btn-primary mt-lg">发送合作请求</button>
        </div>
      </section>
    </div>
  </section>
</template>

<style lang="scss" scoped>
.about-view {
  width: 100%;
  overflow-x: hidden;
}

// 英雄区域
.about-hero {
  background: linear-gradient(135deg, var(--color-primary-dark) 0%, var(--color-primary) 100%);
  color: white;
  padding: var(--spacing-3xl) var(--spacing-padding);
  text-align: center;
  position: relative;
  overflow: hidden;
}

.about-hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M0,100 L100,0 L100,100 Z" fill="rgba(255,255,255,0.05)" /></svg>');
  background-size: cover;
  opacity: 0.6;
}

.about-hero-content {
  position: relative;
  z-index: 1;
  max-width: var(--container-width);
  margin: 0 auto;
}

.about-hero-title {
  font-size: var(--font-size-3xl);
  margin: 0 0 var(--spacing-md) 0;
  font-weight: 800;
  letter-spacing: -0.5px;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.8s ease-out forwards;
}

.about-hero-subtitle {
  font-size: var(--font-size-lg);
  margin: 0;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.8s ease-out forwards 0.2s;
}

// 内容区域
.about-content {
  max-width: var(--container-width);
  margin: 0 auto;
  padding: var(--spacing-3xl) var(--spacing-padding);
}

// 通用section样式
.about-section {
  background-color: var(--color-surface);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-2xl);
  margin-bottom: var(--spacing-2xl);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border);
  transition: all 0.5s ease;
  opacity: 0;
  transform: translateY(30px);
  position: relative;
  overflow: hidden;
}

.about-section.visible {
  opacity: 1;
  transform: translateY(0);
}

.about-section::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(to bottom, var(--color-primary), var(--color-secondary));
}

.section-icon {
  font-size: 2.5rem;
  margin-bottom: var(--spacing-md);
  opacity: 0.8;
}

.section-title {
  font-size: var(--font-size-2xl);
  color: var(--color-primary-dark);
  margin: 0 0 var(--spacing-lg) 0;
  font-weight: 700;
  position: relative;
  display: inline-block;
}

.section-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 60px;
  height: 3px;
  background-color: var(--color-primary);
  border-radius: 3px;
}

.section-content p {
  font-size: var(--font-size-base);
  line-height: 1.8;
  color: var(--color-text-secondary);
  margin: 0;
}

// 特色卡片网格
.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-xl);
  margin-top: var(--spacing-lg);
}

.feature-card {
  background-color: var(--color-background);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-xl);
  text-align: center;
  transition: all 0.3s ease;
  border: 1px solid var(--color-border);
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(to right, var(--color-primary), var(--color-secondary));
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
  border-color: var(--color-primary);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
  opacity: 0.8;
}

.feature-title {
  font-size: var(--font-size-lg);
  color: var(--color-text-primary);
  margin: 0 0 var(--spacing-md) 0;
  font-weight: 600;
}

.feature-description {
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0;
}

// 联系信息
.contact-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
  padding: var(--spacing-lg);
  background-color: var(--color-background);
  border-radius: var(--border-radius-md);
  border: 1px solid var(--color-border);
}

.contact-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  color: var(--color-text-primary);
  text-decoration: none;
  transition: all 0.3s ease;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius-sm);
}

.contact-item:hover {
  background-color: var(--color-hover);
  color: var(--color-primary);
  transform: translateX(5px);
}

.contact-icon {
  font-size: 1.2rem;
  min-width: 24px;
  text-align: center;
}

.contact-text {
  font-size: var(--font-size-base);
  font-weight: 500;
}

// 按钮样式
.btn-primary {
  background-color: var(--color-primary);
  color: white;
  border: none;
  padding: var(--spacing-md) var(--spacing-xl);
  border-radius: var(--border-radius-full);
  font-size: var(--font-size-base);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  box-shadow: var(--shadow-sm);
}

.btn-primary:hover {
  background-color: var(--color-primary-dark);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

// 辅助类
.mt-lg {
  margin-top: var(--spacing-lg);
}

// 动画效果
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

// 响应式设计
@media (max-width: 1024px) {
  .feature-grid {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  }
}

@media (max-width: 768px) {
  .about-hero {
    padding: var(--spacing-2xl) var(--spacing-padding);
  }
  
  .about-hero-title {
    font-size: var(--font-size-2xl);
  }
  
  .about-hero-subtitle {
    font-size: var(--font-size-base);
  }
  
  .about-content {
    padding: var(--spacing-xl) var(--spacing-padding);
  }
  
  .about-section {
    padding: var(--spacing-xl);
    margin-bottom: var(--spacing-xl);
  }
  
  .section-title {
    font-size: var(--font-size-xl);
  }
  
  .feature-grid {
    grid-template-columns: 1fr;
  }
  
  .contact-info {
    padding: var(--spacing-md);
  }
  
  .contact-item {
    padding: var(--spacing-sm);
  }
}

@media (max-width: 480px) {
  .about-hero-title {
    font-size: var(--font-size-xl);
  }
  
  .about-section {
    padding: var(--spacing-lg);
  }
  
  .section-icon {
    font-size: 2rem;
  }
  
  .feature-icon {
    font-size: 2.5rem;
  }
}
</style>