<template>
  <!-- 现代导航栏组件 - 横向排列 -->
  <nav id="modern-navbar" class="navbar navbar-expand-lg fixed-top" :class="{ scrolled: isScrolled }">
    <div class="container">
      <!-- Logo和品牌名称 -->
      <router-link to="/" class="navbar-brand">
        <span class="brand-name">乘灼</span>
      </router-link>

      <!-- 桌面端导航菜单 -->
      <div class="nav-menu">
        <ul class="nav-list">
          <li class="nav-item">
            <router-link to="/" class="nav-link">首页</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/cultures" class="nav-link">文化底蕴</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/regions" class="nav-link">地区风情</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/about" class="nav-link">关于我们</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'ModernNavbar',
  data() {
    return {
      // 导航栏状态管理
      isScrolled: false
    }
  },
  mounted() {
    // 添加滚动事件监听，实现导航栏滚动效果
    window.addEventListener('scroll', this.handleScroll)
  },
  beforeUnmount() {
    // 清理事件监听器
    window.removeEventListener('scroll', this.handleScroll)
  },
  methods: {
    handleScroll() {
      // 检测滚动位置，更新导航栏样式
      this.isScrolled = window.scrollY > 20
    }
  }
}
</script>

<style scoped>
/* 导航栏基础样式 */
#modern-navbar {
  background: linear-gradient(135deg, #4a6fa5 0%, #166088 100%);
  color: white;
  transition: all 0.3s ease;
  padding: 1rem 0;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
}

/* 滚动时的导航栏样式 */
#modern-navbar.scrolled {
  padding: 0.75rem 0;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.15);
  background: linear-gradient(135deg, #3a5a8a 0%, #0f4c75 100%);
}

/* 容器样式 */
.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* 品牌名称样式 */
.brand-name {
  font-size: 1.75rem;
  font-weight: 700;
  color: white;
  letter-spacing: 1px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.brand-name:hover {
  transform: scale(1.05);
  color: #e0f7fa;
}

/* 导航菜单样式 */
.nav-menu {
  display: flex;
  align-items: center;
}

.nav-list {
  display: flex;
  list-style: none;
  gap: 2rem;
  margin: 0;
  padding: 0;
}

/* 导航项样式 */
.nav-item {
  position: relative;
}

/* 导航链接样式 */
.nav-link {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
  font-weight: 500;
  text-decoration: none;
  padding: 0.5rem 0;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: #4fc3f7;
  transition: width 0.3s ease;
}

.nav-link:hover {
  color: white;
}

.nav-link:hover::after {
  width: 100%;
}

/* 活动链接样式 */
.nav-link.router-link-active {
  color: white;
  font-weight: 600;
}

.nav-link.router-link-active::after {
  width: 100%;
  background-color: #4fc3f7;
}

/* 响应式设计 */
@media (max-width: 992px) {
  #modern-navbar {
    padding: 0.75rem 0;
  }
  
  .container {
    padding: 0 1rem;
  }
  
  .brand-name {
    font-size: 1.5rem;
  }
  
  .nav-list {
    gap: 1.5rem;
  }
  
  .nav-link {
    font-size: 0.95rem;
  }
}

@media (max-width: 768px) {
  .nav-list {
    gap: 1rem;
  }
  
  .brand-name {
    font-size: 1.35rem;
  }
  
  .nav-link {
    font-size: 0.9rem;
  }
}
</style>