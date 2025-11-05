<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <nav>
      <h1>传统文化</h1>
      <ul>
        <li><RouterLink to="/">首页</RouterLink></li>
        <li><RouterLink to="/culture">民俗文化</RouterLink></li>
        <li><RouterLink to="/regions">地区分类</RouterLink></li>
        <li><RouterLink to="/about">关于我们</RouterLink></li>
      </ul>
    </nav>
  </header>
  
  <main>
    <RouterView />
  </main>
  
  <footer>
    <p>&copy; 2025 传统文化网. 保留所有权利.</p>
  </footer>
</template>

<style>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 基础样式 - 中国风字体设置 */
body {
  font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'SimSun', serif;
  line-height: 1.6;
  color: #333;
  background-color: #faf7f0;
}

/* 头部导航 - 中国传统红色系 */
header {
  background-color: #C8102E;
  color: white;
  padding: 1.25rem 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 100;
}

/* 装饰性元素 - 中国传统花纹 */
header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background-image: linear-gradient(90deg, 
    transparent 0%, 
    rgba(255, 255, 255, 0.8) 20%, 
    rgba(255, 255, 255, 0.8) 80%, 
    transparent 100%);
}

/* 导航容器样式 */
nav {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 网站标题 - 中国风书法风格 */
nav h1 {
  font-size: 2rem;
  font-weight: bold;
  letter-spacing: 1px;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
  font-family: 'STZhongsong', 'FangSong', serif;
}

/* 导航列表 */
nav ul {
  display: flex;
  list-style: none;
  gap: 2rem;
}

/* 导航链接 - 中国传统设计 */
nav a {
  color: white;
  text-decoration: none;
  font-size: 1.1rem;
  transition: all 0.3s;
  position: relative;
  padding: 0.5rem 0;
  font-weight: 500;
}

/* 导航链接悬停效果 */
nav a:hover {
  color: #ffd700;
}

/* 导航链接下方装饰线 */
nav a::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: #ffd700;
  transition: width 0.3s ease;
}

/* 导航链接悬停时显示装饰线 */
nav a:hover::after {
  width: 100%;
}

/* 主内容区域 */
main {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
  min-height: 70vh;
}

/* 页脚 - 传统暗色系 */
footer {
  background-color: #2c1e1e;
  color: #e8d4b4;
  text-align: center;
  padding: 2rem 0;
  margin-top: 3rem;
  position: relative;
}

/* 页脚装饰元素 */
footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background-image: linear-gradient(90deg, 
    transparent 0%, 
    rgba(232, 212, 180, 0.5) 20%, 
    rgba(232, 212, 180, 0.5) 80%, 
    transparent 100%);
}

/* 响应式设计 */
@media (max-width: 768px) {
  header {
    padding: 1rem 0;
  }
  
  nav {
    flex-direction: column;
    gap: 1rem;
  }
  
  nav h1 {
    font-size: 1.6rem;
  }
  
  nav ul {
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
  }
  
  nav a {
    font-size: 1rem;
    padding: 0.3rem 0;
  }
}
</style>