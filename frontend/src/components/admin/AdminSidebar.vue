<template>
  <div class="admin-sidebar" :class="{ 'collapsed': isCollapsed, 'dark': isDarkMode }">
    <!-- 品牌区域 -->
    <div class="sidebar-header">
      <div class="brand-logo">
        <span class="logo-icon">🏛️</span>
        <h3 v-if="!isCollapsed" class="brand-name">民族文化后台</h3>
      </div>
      <button @click="toggleCollapse" class="collapse-btn">
        {{ isCollapsed ? '▶️' : '◀️' }}
      </button>
    </div>

    <!-- 导航菜单 -->
    <nav class="sidebar-nav">
      <div
        v-for="group in navigationGroups"
        :key="group.title"
        class="nav-group"
      >
        <h4 v-if="!isCollapsed" class="group-title">{{ group.title }}</h4>
        <ul class="nav-list">
          <li
            v-for="item in group.items"
            :key="item.id"
            class="nav-item"
            :class="{
              'active': isActive(item),
              'has-submenu': item.submenu && item.submenu.length > 0
            }"
          >
            <router-link
              v-if="!item.submenu || item.submenu.length === 0"
              :to="item.path"
              class="nav-link"
              @click="$emit('link-clicked')"
            >
              <span class="nav-icon">{{ item.icon }}</span>
              <span v-if="!isCollapsed" class="nav-text">{{ item.title }}</span>
            </router-link>
            
            <div v-else class="nav-link with-submenu">
              <div
                @click="toggleSubmenu(item.id)"
                class="main-link"
                @click.stop
              >
                <span class="nav-icon">{{ item.icon }}</span>
                <span v-if="!isCollapsed" class="nav-text">{{ item.title }}</span>
                <span class="submenu-toggle">
                  {{ isSubmenuOpen(item.id) ? '▼' : '▶' }}
                </span>
              </div>
              
              <ul
                v-if="isSubmenuOpen(item.id)"
                class="submenu"
                :class="{ 'expanded': isSubmenuOpen(item.id) }"
              >
                <li
                  v-for="subItem in item.submenu"
                  :key="subItem.id"
                  class="submenu-item"
                  :class="{ 'active': isActive(subItem) }"
                >
                  <router-link
                    :to="subItem.path"
                    class="submenu-link"
                    @click="$emit('link-clicked')"
                  >
                    <span class="submenu-icon">{{ subItem.icon || '•' }}</span>
                    <span v-if="!isCollapsed" class="submenu-text">{{ subItem.title }}</span>
                  </router-link>
                </li>
              </ul>
            </div>
          </li>
        </ul>
      </div>
    </nav>

    <!-- 底部区域 -->
    <div class="sidebar-footer">
      <div class="user-info" v-if="!isCollapsed">
        <div class="user-avatar">{{ currentUser?.avatar || '👤' }}</div>
        <div class="user-details">
          <div class="user-name">{{ currentUser?.name || '管理员' }}</div>
          <div class="user-role">{{ currentUser?.role || '超级管理员' }}</div>
        </div>
      </div>
      
      <div class="footer-actions">
        <button
          @click="toggleDarkMode"
          class="theme-toggle"
          :title="isDarkMode ? '切换至亮色模式' : '切换至暗色模式'"
        >
          {{ isDarkMode ? '☀️' : '🌙' }}
        </button>
        
        <button
          v-if="!isCollapsed"
          @click="handleLogout"
          class="logout-btn"
        >
          <span class="logout-icon">🚪</span>
          <span class="logout-text">退出登录</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';

// 定义导航项接口
interface NavItem {
  id: string;
  title: string;
  path: string;
  icon: string;
  permission?: string;
  submenu?: NavItem[];
}

// 定义导航组接口
interface NavGroup {
  title: string;
  items: NavItem[];
}

// Emits定义
const emit = defineEmits<{
  'link-clicked': [];
  'logout': [];
  'theme-changed': [isDark: boolean];
}>();

// Props定义
interface Props {
  autoCollapse?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  autoCollapse: true
});

// 响应式数据
const isCollapsed = ref(false);
const isDarkMode = ref(false);
const expandedSubmenus = ref<Set<string>>(new Set());
const currentUser = ref<{name?: string; role?: string; avatar?: string} | null>({
  name: '管理员',
  role: '超级管理员',
  avatar: '👨‍💼'
});

const route = useRoute();

// 导航菜单配置 - 专注于用户端配置功能
const navigationGroups: NavGroup[] = [
  // 第一组：系统配置（最顶部）
  {
    title: '系统配置',
    items: [
      {
        id: 'system-config',
        title: '系统设置',
        path: '/admin/system-config',
        icon: '⚙️'
      },
      {
        id: 'user-management',
        title: '用户管理',
        path: '/admin/user-management',
        icon: '👥'
      }
    ]
  },
  // 第二组：内容配置
  {
    title: '内容配置',
    items: [
      {
        id: 'content-config',
        title: '内容管理',
        path: '/admin/content-config',
        icon: '📝'
      },
      {
        id: 'data-config',
        title: '数据配置',
        path: '/admin/data-config',
        icon: '💾'
      }
    ]
  }
];

// 计算属性
const isActive = (item: NavItem): boolean => {
  return route.path === item.path;
};

const isSubmenuOpen = (menuId: string): boolean => {
  return expandedSubmenus.value.has(menuId);
};

// 方法
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
  localStorage.setItem('sidebar-collapsed', String(isCollapsed.value));
};

const toggleSubmenu = (menuId: string) => {
  if (expandedSubmenus.value.has(menuId)) {
    expandedSubmenus.value.delete(menuId);
  } else {
    expandedSubmenus.value.add(menuId);
  }
};

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
  document.documentElement.classList.toggle('dark', isDarkMode.value);
  localStorage.setItem('dark-mode', String(isDarkMode.value));
  emit('theme-changed', isDarkMode.value);
};

const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    // 这里可以添加清除token等逻辑
    emit('logout');
    // 跳转到登录页
    window.location.href = '/login';
  }
};

// 响应窗口大小变化
const handleResize = () => {
  if (props.autoCollapse) {
    const isMobile = window.innerWidth < 768;
    isCollapsed.value = isMobile;
  }
};

// 生命周期
onMounted(() => {
  // 从本地存储恢复状态
  const savedCollapsed = localStorage.getItem('sidebar-collapsed');
  if (savedCollapsed !== null) {
    isCollapsed.value = savedCollapsed === 'true';
  }

  const savedDarkMode = localStorage.getItem('dark-mode');
  if (savedDarkMode !== null) {
    isDarkMode.value = savedDarkMode === 'true';
    document.documentElement.classList.toggle('dark', isDarkMode.value);
  }

  // 监听窗口大小变化
  window.addEventListener('resize', handleResize);
  handleResize(); // 初始化时执行一次

  // 自动展开当前路径的父菜单
  const currentPath = route.path;
  navigationGroups.forEach(group => {
    group.items.forEach(item => {
      if (item.submenu) {
        const isActiveSubmenu = item.submenu.some(subItem => subItem.path === currentPath);
        if (isActiveSubmenu) {
          expandedSubmenus.value.add(item.id);
        }
      }
    });
  });
});

// 监听路由变化，自动展开相应的子菜单
watch(
  () => route.path,
  (newPath) => {
    navigationGroups.forEach(group => {
      group.items.forEach(item => {
        if (item.submenu) {
          const isActiveSubmenu = item.submenu.some(subItem => subItem.path === newPath);
          if (isActiveSubmenu) {
            expandedSubmenus.value.add(item.id);
          } else if (item.path !== newPath) {
            // 关闭非当前路径的子菜单
            // expandedSubmenus.value.delete(item.id);
          }
        }
      });
    });
  }
);
</script>

<style scoped>
.admin-sidebar {
  width: 260px;
  height: 100vh;
  background-color: #ffffff;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.admin-sidebar.collapsed {
  width: 70px;
}

.admin-sidebar.dark {
  background-color: #1e293b;
  border-right-color: #334155;
  color: #f1f5f9;
}

/* 侧边栏头部 */
.sidebar-header {
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.sidebar-header.dark {
  border-bottom-color: #334155;
}

.brand-logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-icon {
  font-size: 1.5rem;
}

.brand-name {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
}

.dark .brand-name {
  color: #f1f5f9;
}

.collapse-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.collapse-btn:hover {
  background-color: #f1f5f9;
}

.dark .collapse-btn:hover {
  background-color: #334155;
}

/* 导航菜单 */
.sidebar-nav {
  flex: 1;
  padding: 20px 0;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
}

.nav-group {
  margin-bottom: 24px;
  display: flex;
  flex-direction: column;
}

.group-title {
  margin: 0 0 8px 20px;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748b;
  font-weight: 600;
}

.dark .group-title {
  color: #94a3b8;
}

.nav-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
}

.nav-item {
  margin-bottom: 2px;
  display: block;
  width: 100%;
}

.nav-item.active > .nav-link > .nav-icon,
.nav-item.active > .nav-link > .nav-text {
  color: #3b82f6;
  font-weight: 500;
}

.nav-item.has-submenu .main-link {
  width: 100%;
  display: flex;
  align-items: center;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.2s;
  text-decoration: none;
}

.nav-item.has-submenu .main-link:hover {
  background-color: #f1f5f9;
}

.dark .nav-item.has-submenu .main-link:hover {
  background-color: #334155;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  color: #334155;
  text-decoration: none;
  transition: background-color 0.2s;
}

.nav-link:hover {
  background-color: #f1f5f9;
}

.dark .nav-link {
  color: #cbd5e1;
}

.dark .nav-link:hover {
  background-color: #334155;
}

.nav-icon {
  font-size: 1.1rem;
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
}

.nav-text {
  font-size: 0.95rem;
  transition: opacity 0.2s;
}

.submenu-toggle {
  margin-left: auto;
  font-size: 0.7rem;
  transition: transform 0.2s;
}

.submenu {
  list-style: none;
  margin: 0;
  padding: 0;
  background-color: #f8fafc;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}

.dark .submenu {
  background-color: #273449;
}

.submenu.expanded {
  max-height: 500px;
}

.submenu-item {
  padding: 0;
}

.submenu-link {
  display: flex;
  align-items: center;
  padding: 8px 20px 8px 48px;
  color: #475569;
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.submenu-link:hover {
  background-color: #e2e8f0;
  padding-left: 52px;
}

.dark .submenu-link {
  color: #94a3b8;
}

.dark .submenu-link:hover {
  background-color: #334155;
}

.submenu-item.active .submenu-link {
  color: #3b82f6;
  background-color: #dbeafe;
  font-weight: 500;
}

.dark .submenu-item.active .submenu-link {
  background-color: #1e3a8a;
}

.submenu-icon {
  font-size: 0.6rem;
  margin-right: 8px;
  opacity: 0.7;
}

/* 侧边栏底部 */
.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid #e2e8f0;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.dark .sidebar-footer {
  border-top-color: #334155;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #3b82f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: white;
}

.user-details {
  flex: 1;
}

.user-name {
  font-weight: 500;
  font-size: 0.9rem;
  color: #1e293b;
}

.dark .user-name {
  color: #f1f5f9;
}

.user-role {
  font-size: 0.8rem;
  color: #64748b;
}

.dark .user-role {
  color: #94a3b8;
}

.footer-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.theme-toggle,
.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px 12px;
  background: none;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
  color: #475569;
}

.dark .theme-toggle,
.dark .logout-btn {
  border-color: #334155;
  color: #cbd5e1;
}

.theme-toggle:hover,
.logout-btn:hover {
  background-color: #f1f5f9;
  border-color: #cbd5e1;
}

.dark .theme-toggle:hover,
.dark .logout-btn:hover {
  background-color: #334155;
  border-color: #475569;
}

.logout-icon {
  font-size: 1rem;
}

/* 折叠状态的样式调整 */
.collapsed .brand-name,
.collapsed .group-title,
.collapsed .nav-text,
.collapsed .submenu-text,
.collapsed .user-details,
.collapsed .logout-text {
  display: none;
}

.collapsed .sidebar-header,
.collapsed .nav-link,
.collapsed .nav-item.has-submenu .main-link {
  padding-left: 15px;
  padding-right: 15px;
  justify-content: center;
}

.collapsed .nav-icon {
  margin-right: 0;
}

.collapsed .submenu-toggle {
  display: none;
}

.collapsed .user-info {
  justify-content: center;
}

.collapsed .footer-actions {
  align-items: center;
}

.collapsed .theme-toggle,
.collapsed .logout-btn {
  width: 40px;
  height: 40px;
  padding: 0;
}

/* 滚动条样式 */
.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.dark .sidebar-nav::-webkit-scrollbar-thumb {
  background: #475569;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .admin-sidebar {
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    transform: translateX(0);
  }

  .admin-sidebar.collapsed {
    transform: translateX(-100%);
  }
}
</style>