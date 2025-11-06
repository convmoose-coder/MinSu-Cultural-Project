<template>
  <div class="admin-layout" :class="{ 'dark': isDarkMode }">
    <!-- 侧边栏 -->
    <AdminSidebar
      :auto-collapse="autoCollapse"
      @link-clicked="handleLinkClicked"
      @logout="handleLogout"
      @theme-changed="handleThemeChange"
    />

    <!-- 主内容区 -->
    <div class="main-content" :class="{ 'sidebar-collapsed': isSidebarCollapsed }">
      <!-- 顶部导航栏 -->
      <header class="main-header">
        <div class="header-left">
          <button @click="toggleSidebar" class="sidebar-toggle">
            🍔
          </button>
          <h1 class="page-title">{{ currentPageTitle }}</h1>
        </div>
        <div class="header-right">
          <!-- 搜索框 -->
          <div class="search-container">
            <input
              type="text"
              placeholder="搜索..."
              class="search-input"
              v-model="searchQuery"
              @input="handleSearch"
            />
            <span class="search-icon">🔍</span>
          </div>
          
          <!-- 通知图标 -->
          <div class="notification-container">
            <button class="notification-btn" @click="toggleNotifications">
              <span class="notification-icon">🔔</span>
              <span v-if="notifications.length > 0" class="notification-badge">{{ notifications.length }}</span>
            </button>
            
            <!-- 通知面板 -->
            <div v-if="showNotifications" class="notification-panel">
              <div class="notification-header">
                <h3>通知</h3>
                <button @click="clearNotifications" class="clear-btn">清除全部</button>
              </div>
              <div class="notification-list">
                <div
                  v-for="(notification, index) in notifications"
                  :key="index"
                  class="notification-item"
                  :class="{ 'unread': !notification.read }"
                  @click="markAsRead(index)"
                >
                  <span class="notification-type">{{ notification.type }}</span>
                  <span class="notification-message">{{ notification.message }}</span>
                  <span class="notification-time">{{ formatTime(notification.time) }}</span>
                </div>
                <div v-if="notifications.length === 0" class="no-notifications">
                  暂无通知
                </div>
              </div>
            </div>
          </div>
          
          <!-- 用户头像 -->
          <div class="user-menu">
            <button class="user-menu-btn" @click="toggleUserMenu">
              <div class="user-avatar-mini">👤</div>
            </button>
            
            <!-- 用户菜单面板 -->
            <div v-if="showUserMenu" class="user-menu-panel">
              <div class="user-info-mini">
                <div class="user-name-mini">管理员</div>
                <div class="user-role-mini">超级管理员</div>
              </div>
              <div class="menu-divider"></div>
              <ul class="user-menu-list">
                <li class="user-menu-item">
                  <router-link to="/admin/profile">
                    <span class="menu-icon-mini">👤</span>
                    <span class="menu-text-mini">个人资料</span>
                  </router-link>
                </li>
                <li class="user-menu-item">
                  <router-link to="/admin/settings">
                    <span class="menu-icon-mini">⚙️</span>
                    <span class="menu-text-mini">账号设置</span>
                  </router-link>
                </li>
                <li class="user-menu-item">
                  <a href="#" @click.prevent="handleLogout">
                    <span class="menu-icon-mini">🚪</span>
                    <span class="menu-text-mini">退出登录</span>
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </header>

      <!-- 页面内容 -->
      <main class="page-content">
        <slot></slot>
      </main>

      <!-- 页脚 -->
      <footer class="main-footer">
        <div class="footer-content">
          <p>© 2024 民族文化后台管理系统. 保留所有权利.</p>
          <div class="footer-links">
            <a href="#" class="footer-link">使用帮助</a>
            <span class="footer-divider">|</span>
            <a href="#" class="footer-link">关于系统</a>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import AdminSidebar from './AdminSidebar.vue';

// 定义通知接口
interface Notification {
  id: string;
  type: string;
  message: string;
  time: Date;
  read: boolean;
}

// Props定义
interface Props {
  autoCollapse?: boolean;
  showHeader?: boolean;
  showFooter?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  autoCollapse: true,
  showHeader: true,
  showFooter: true
});

// Emits定义
const emit = defineEmits<{
  'sidebar-toggle': [collapsed: boolean];
  'logout': [];
  'search': [query: string];
  'theme-changed': [isDark: boolean];
}>();

// 响应式数据
const isDarkMode = ref(false);
const isSidebarCollapsed = ref(false);
const searchQuery = ref('');
const showNotifications = ref(false);
const showUserMenu = ref(false);
const notifications = ref<Notification[]>([]);

const route = useRoute();
const router = useRouter();

// 计算属性
const currentPageTitle = computed(() => {
  // 根据路由路径返回对应的页面标题
  const titleMap: Record<string, string> = {
    '/admin/system-config': '系统配置',
    '/admin/user-management': '用户管理',
    '/admin/content-config': '内容配置',
    '/admin/data-config': '数据配置'
  };
  return titleMap[route.path] || '后台管理';
});

// 方法
const toggleSidebar = () => {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
  emit('sidebar-toggle', isSidebarCollapsed.value);
};

const handleLinkClicked = () => {
  // 在移动设备上，点击链接后自动收起侧边栏
  if (window.innerWidth < 768) {
    isSidebarCollapsed.value = true;
  }
};

const handleLogout = () => {
  if (confirm('确定要退出登录吗？')) {
    emit('logout');
    // 清除登录状态
    localStorage.removeItem('admin-token');
    // 跳转到登录页
    router.push('/login');
  }
};

const handleThemeChange = (isDark: boolean) => {
  isDarkMode.value = isDark;
  emit('theme-changed', isDark);
};

const handleSearch = () => {
  emit('search', searchQuery.value);
};

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value;
  showUserMenu.value = false; // 关闭其他菜单
};

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value;
  showNotifications.value = false; // 关闭其他菜单
};

const markAsRead = (index: number) => {
  notifications.value[index].read = true;
  // 这里可以调用API标记通知为已读
};

const clearNotifications = () => {
  notifications.value = [];
  // 这里可以调用API清除通知
};

const formatTime = (time: Date): string => {
  const now = new Date();
  const diff = now.getTime() - time.getTime();
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (minutes < 1) return '刚刚';
  if (minutes < 60) return `${minutes}分钟前`;
  if (hours < 24) return `${hours}小时前`;
  if (days < 7) return `${days}天前`;
  return time.toLocaleDateString();
};

// 点击外部关闭菜单
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement;
  if (
    !target.closest('.notification-container') &&
    !target.closest('.user-menu')
  ) {
    showNotifications.value = false;
    showUserMenu.value = false;
  }
};

// 生命周期
onMounted(() => {
  // 从本地存储恢复主题设置
  const savedDarkMode = localStorage.getItem('dark-mode');
  if (savedDarkMode !== null) {
    isDarkMode.value = savedDarkMode === 'true';
    document.documentElement.classList.toggle('dark', isDarkMode.value);
  }

  // 监听点击外部事件
  document.addEventListener('click', handleClickOutside);

  // 模拟获取通知数据
  notifications.value = [
    {
      id: '1',
      type: '📤',
      message: '批量上传任务已完成',
      time: new Date(Date.now() - 30 * 60000), // 30分钟前
      read: false
    },
    {
      id: '2',
      type: '⚠️',
      message: '有3条数据导入失败，请查看日志',
      time: new Date(Date.now() - 2 * 3600000), // 2小时前
      read: false
    },
    {
      id: '3',
      type: '👥',
      message: '管理员已登录系统',
      time: new Date(Date.now() - 24 * 3600000), // 1天前
      read: true
    }
  ];

  // 监听路由变化，关闭菜单
  watch(
    () => route.path,
    () => {
      showNotifications.value = false;
      showUserMenu.value = false;
    }
  );
});
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background-color: #f8fafc;
}

.admin-layout.dark {
  background-color: #0f172a;
  color: #f1f5f9;
}

/* 主内容区 */
.main-content {
  flex: 1;
  margin-left: 260px;
  transition: margin-left 0.3s ease;
  display: flex;
  flex-direction: column;
}

.main-content.sidebar-collapsed {
  margin-left: 70px;
}

/* 顶部导航栏 */
.main-header {
  height: 64px;
  background-color: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  flex-shrink: 0;
}

.dark .main-header {
  background-color: #1e293b;
  border-bottom-color: #334155;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.sidebar-toggle {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.sidebar-toggle:hover {
  background-color: #f1f5f9;
}

.dark .sidebar-toggle:hover {
  background-color: #334155;
}

.page-title {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
}

.dark .page-title {
  color: #f1f5f9;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* 搜索框 */
.search-container {
  position: relative;
}

.search-input {
  width: 240px;
  padding: 8px 12px 8px 36px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  background-color: #f8fafc;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  width: 280px;
}

.dark .search-input {
  background-color: #334155;
  border-color: #475569;
  color: #f1f5f9;
}

.dark .search-input:focus {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}

.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.9rem;
  color: #64748b;
}

.dark .search-icon {
  color: #94a3b8;
}

/* 通知部分 */
.notification-container {
  position: relative;
}

.notification-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 6px;
  position: relative;
  transition: background-color 0.2s;
}

.notification-btn:hover {
  background-color: #f1f5f9;
}

.dark .notification-btn:hover {
  background-color: #334155;
}

.notification-icon {
  font-size: 1.2rem;
}

.notification-badge {
  position: absolute;
  top: 0;
  right: 0;
  background-color: #ef4444;
  color: white;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 16px;
  text-align: center;
}

.notification-panel {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  width: 360px;
  max-height: 400px;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  z-index: 1000;
}

.dark .notification-panel {
  background-color: #1e293b;
  border-color: #334155;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.dark .notification-header {
  border-bottom-color: #334155;
}

.notification-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
}

.dark .notification-header h3 {
  color: #f1f5f9;
}

.clear-btn {
  background: none;
  border: none;
  color: #3b82f6;
  font-size: 0.8rem;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.clear-btn:hover {
  background-color: #f1f5f9;
}

.dark .clear-btn:hover {
  background-color: #334155;
}

.notification-list {
  max-height: 320px;
  overflow-y: auto;
}

.notification-item {
  padding: 12px 16px;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.notification-item:hover {
  background-color: #f8fafc;
}

.dark .notification-item {
  border-bottom-color: #334155;
}

.dark .notification-item:hover {
  background-color: #334155;
}

.notification-item.unread {
  background-color: #eff6ff;
}

.dark .notification-item.unread {
  background-color: #1e3a8a;
}

.notification-type {
  font-size: 1.1rem;
}

.notification-message {
  font-size: 0.9rem;
  color: #334155;
  font-weight: 500;
}

.dark .notification-message {
  color: #e2e8f0;
}

.notification-time {
  font-size: 0.75rem;
  color: #64748b;
}

.dark .notification-time {
  color: #94a3b8;
}

.no-notifications {
  padding: 24px;
  text-align: center;
  color: #64748b;
}

.dark .no-notifications {
  color: #94a3b8;
}

/* 用户菜单 */
.user-menu {
  position: relative;
}

.user-menu-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.user-menu-btn:hover {
  background-color: #f1f5f9;
}

.dark .user-menu-btn:hover {
  background-color: #334155;
}

.user-avatar-mini {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #3b82f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  color: white;
}

.user-menu-panel {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  width: 240px;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  z-index: 1000;
}

.dark .user-menu-panel {
  background-color: #1e293b;
  border-color: #334155;
}

.user-info-mini {
  padding: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.dark .user-info-mini {
  border-bottom-color: #334155;
}

.user-name-mini {
  font-weight: 600;
  font-size: 0.95rem;
  color: #1e293b;
  margin-bottom: 4px;
}

.dark .user-name-mini {
  color: #f1f5f9;
}

.user-role-mini {
  font-size: 0.8rem;
  color: #64748b;
}

.dark .user-role-mini {
  color: #94a3b8;
}

.menu-divider {
  height: 1px;
  background-color: #e2e8f0;
}

.dark .menu-divider {
  background-color: #334155;
}

.user-menu-list {
  list-style: none;
  margin: 0;
  padding: 8px 0;
}

.user-menu-item {
  padding: 0;
}

.user-menu-item a {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  color: #334155;
  text-decoration: none;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.user-menu-item a:hover {
  background-color: #f8fafc;
}

.dark .user-menu-item a {
  color: #cbd5e1;
}

.dark .user-menu-item a:hover {
  background-color: #334155;
}

.menu-icon-mini {
  font-size: 1rem;
}

.menu-text-mini {
  font-weight: 500;
}

/* 页面内容 */
.page-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
}

/* 页脚 */
.main-footer {
  height: 60px;
  background-color: #ffffff;
  border-top: 1px solid #e2e8f0;
  flex-shrink: 0;
}

.dark .main-footer {
  background-color: #1e293b;
  border-top-color: #334155;
}

.footer-content {
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  font-size: 0.85rem;
  color: #64748b;
}

.dark .footer-content {
  color: #94a3b8;
}

.footer-content p {
  margin: 0;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.footer-link {
  color: #64748b;
  text-decoration: none;
  transition: color 0.2s;
}

.footer-link:hover {
  color: #3b82f6;
}

.dark .footer-link {
  color: #94a3b8;
}

.footer-divider {
  color: #cbd5e1;
}

.dark .footer-divider {
  color: #475569;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
  }

  .main-content.sidebar-collapsed {
    margin-left: 0;
  }

  .header-right {
    gap: 8px;
  }

  .search-input {
    width: 160px;
  }

  .search-input:focus {
    width: 180px;
  }

  .notification-panel {
    width: 300px;
    right: -10px;
  }

  .user-menu-panel {
    right: -10px;
  }

  .page-content {
    padding: 16px;
  }

  .footer-content {
    flex-direction: column;
    gap: 8px;
    padding: 12px 16px;
  }
}
</style>