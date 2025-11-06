<template>
  <div class="sidebar-container" :class="{ 'expanded': isExpanded, 'dark': darkMode }">
    <!-- 侧边栏头部 -->
    <div class="sidebar-header">
      <div class="logo-container" :class="{ 'compact': !isExpanded }">
        <div class="logo-icon">{{ logoIcon }}</div>
        <span v-if="isExpanded" class="logo-text">{{ brandName }}</span>
      </div>
      <button 
        class="toggle-btn" 
        @click="toggleSidebar"
        :title="isExpanded ? '收起侧边栏' : '展开侧边栏'"
      >
        {{ toggleIcon }}
      </button>
    </div>

    <!-- 侧边栏导航 -->
    <nav class="sidebar-nav">
      <div 
        v-for="(item, index) in navItems" 
        :key="index"
        class="nav-item"
        :class="{
          'has-children': item.children && item.children.length > 0,
          'active': isActive(item),
          'collapsed': !isExpanded && item.children && item.children.length > 0
        }"
      >
        <!-- 导航项 -->
        <div 
          class="nav-link" 
          @click="handleNavClick(item)"
          :title="item.label"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span v-if="isExpanded" class="nav-label">{{ item.label }}</span>
          <span 
            v-if="item.children && item.children.length > 0" 
            class="expand-icon"
            :class="{ 'rotated': isItemExpanded(item.id) }"
          >
            {{ expandIcon }}
          </span>
        </div>

        <!-- 子导航 -->
        <transition name="submenu">
          <div 
            v-if="isItemExpanded(item.id) && item.children && item.children.length > 0"
            class="sub-nav"
          >
            <div 
              v-for="(child, childIndex) in item.children" 
              :key="childIndex"
              class="sub-nav-item"
              :class="{ 'active': isActive(child) }"
              @click="handleNavClick(child)"
              :title="child.label"
            >
              <span v-if="isExpanded" class="sub-nav-label">{{ child.label }}</span>
              <span v-else class="sub-nav-tooltip">{{ child.label }}</span>
            </div>
          </div>
        </transition>
      </div>
    </nav>

    <!-- 侧边栏底部 -->
    <div class="sidebar-footer" v-if="showFooter">
      <div class="user-info" v-if="userInfo && isExpanded">
        <div class="user-avatar">{{ userInitial }}</div>
        <div class="user-details">
          <div class="user-name">{{ userInfo.name || '管理员' }}</div>
          <div class="user-role">{{ userInfo.role || '管理员' }}</div>
        </div>
      </div>
      <div class="footer-actions" :class="{ 'expanded': isExpanded }">
        <button 
          v-if="showSettings" 
          class="footer-btn settings-btn" 
          @click="handleSettingsClick"
          title="设置"
        >
          {{ settingsIcon }}
        </button>
        <button 
          v-if="showDarkModeToggle" 
          class="footer-btn dark-mode-btn" 
          @click="toggleDarkMode"
          title="切换主题"
        >
          {{ darkModeIcon }}
        </button>
        <button 
          v-if="showLogout" 
          class="footer-btn logout-btn" 
          @click="handleLogout"
          title="退出登录"
        >
          {{ logoutIcon }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

// 定义属性
interface Props {
  darkMode?: boolean;
  expanded?: boolean;
  brandName?: string;
  logoIcon?: string;
  showFooter?: boolean;
  showSettings?: boolean;
  showDarkModeToggle?: boolean;
  showLogout?: boolean;
  userInfo?: {
    name?: string;
    role?: string;
  };
  navItems?: NavItem[];
  minWidth?: number;
  maxWidth?: number;
  autoCollapse?: boolean;
  autoCollapseBreakpoint?: number;
}

// 导航项接口
interface NavItem {
  id?: string;
  label: string;
  icon: string;
  route?: string;
  href?: string;
  target?: string;
  children?: NavItem[];
  permission?: string;
  badge?: number | string;
  badgeColor?: string;
  disabled?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  darkMode: false,
  expanded: true,
  brandName: '民俗文化管理系统',
  logoIcon: '🏠',
  showFooter: true,
  showSettings: true,
  showDarkModeToggle: true,
  showLogout: true,
  userInfo: () => ({
    name: '管理员',
    role: '系统管理员'
  }),
  navItems: () => [
    {
      id: 'dashboard',
      label: '仪表盘',
      icon: '📊',
      route: '/admin'
    },
    {
      id: 'content',
      label: '内容管理',
      icon: '📝',
      children: [
        {
          label: '民俗文化列表',
          icon: '📚',
          route: '/admin/folk-culture'
        },
        {
          label: '批量上传',
          icon: '📤',
          route: '/admin/upload'
        },
        {
          label: '分类管理',
          icon: '🗂️',
          route: '/admin/categories'
        }
      ]
    },
    {
      id: 'media',
      label: '媒体管理',
      icon: '🖼️',
      route: '/admin/media'
    },
    {
      id: 'users',
      label: '用户管理',
      icon: '👥',
      route: '/admin/users'
    },
    {
      id: 'settings',
      label: '系统设置',
      icon: '⚙️',
      route: '/admin/settings'
    }
  ],
  minWidth: 60,
  maxWidth: 260,
  autoCollapse: true,
  autoCollapseBreakpoint: 768
});

// 定义事件
const emit = defineEmits<{
  'update:darkMode': [value: boolean];
  'update:expanded': [value: boolean];
  'settings-click': [];
  'logout': [];
  'navigate': [route: string];
}>();

// 响应式数据
const route = useRoute();
const router = useRouter();
const isExpanded = ref(props.expanded);
const expandedItems = ref<string[]>([]);
const darkMode = ref(props.darkMode);

// 计算属性
const toggleIcon = computed(() => isExpanded.value ? '◀' : '▶');
const expandIcon = computed(() => isExpanded.value ? '▼' : '▶');
const darkModeIcon = computed(() => darkMode.value ? '☀️' : '🌙');
const settingsIcon = computed(() => '⚙️');
const logoutIcon = computed(() => '🚪');
const logoIcon = computed(() => props.logoIcon);

// 计算用户首字母
const userInitial = computed(() => {
  if (!props.userInfo?.name) return '管';
  const name = props.userInfo.name;
  // 获取汉字首字母或英文首字母
  return name.charAt(0).toUpperCase();
});

// 方法
const toggleSidebar = () => {
  isExpanded.value = !isExpanded.value;
  emit('update:expanded', isExpanded.value);
};

const toggleDarkMode = () => {
  darkMode.value = !darkMode.value;
  emit('update:darkMode', darkMode.value);
};

const handleSettingsClick = () => {
  emit('settings-click');
};

const handleLogout = () => {
  emit('logout');
};

const isActive = (item: NavItem): boolean => {
  if (!item) return false;
  
  // 检查当前项是否匹配路由
  if (item.route) {
    // 完全匹配或开头匹配
    return route.path === item.route || route.path.startsWith(item.route + '/');
  }
  
  // 检查子项是否有活动项
  if (item.children) {
    return item.children.some(child => isActive(child));
  }
  
  return false;
};

const isItemExpanded = (id?: string): boolean => {
  if (!id) return false;
  return expandedItems.value.includes(id);
};

const toggleItemExpand = (id?: string) => {
  if (!id) return;
  const index = expandedItems.value.indexOf(id);
  if (index > -1) {
    expandedItems.value.splice(index, 1);
  } else {
    expandedItems.value.push(id);
  }
};

const handleNavClick = (item: NavItem) => {
  // 禁用项不响应点击
  if (item.disabled) return;
  
  // 有子项的导航点击切换展开状态
  if (item.children && item.children.length > 0 && item.id) {
    toggleItemExpand(item.id);
    return;
  }
  
  // 处理路由跳转
  if (item.route) {
    router.push(item.route);
    emit('navigate', item.route);
  } 
  // 处理外部链接
  else if (item.href) {
    window.open(item.href, item.target || '_self');
  }
};

const handleResize = () => {
  if (!props.autoCollapse) return;
  
  const isMobile = window.innerWidth <= props.autoCollapseBreakpoint;
  if (isMobile && isExpanded.value) {
    isExpanded.value = false;
    emit('update:expanded', false);
  }
};

// 初始化活动项
const initializeExpandedItems = () => {
  const activeItems = findActiveParentItems(props.navItems || []);
  expandedItems.value = activeItems;
};

// 递归查找活动父项
const findActiveParentItems = (items: NavItem[]): string[] => {
  const result: string[] = [];
  
  for (const item of items) {
    if (item.children && item.children.length > 0) {
      // 检查子项是否有活动项
      const hasActiveChild = item.children.some(child => isActive(child));
      if (hasActiveChild && item.id) {
        result.push(item.id);
        // 递归查找子项的活动父项
        const childResults = findActiveParentItems(item.children);
        result.push(...childResults);
      }
    }
  }
  
  return result;
};

// 生命周期
onMounted(() => {
  isExpanded.value = props.expanded;
  darkMode.value = props.darkMode;
  initializeExpandedItems();
  
  if (props.autoCollapse) {
    window.addEventListener('resize', handleResize);
    // 初始检查
    handleResize();
  }
});

// 清理事件监听
const cleanup = () => {
  if (props.autoCollapse) {
    window.removeEventListener('resize', handleResize);
  }
};

// 监听属性变化
watch(() => props.expanded, (newVal) => {
  isExpanded.value = newVal;
});

watch(() => props.darkMode, (newVal) => {
  darkMode.value = newVal;
});

// 导出清理函数供组件卸载时使用
const unmounted = () => {
  cleanup();
};

defineExpose({
  toggleSidebar,
  toggleDarkMode,
  isExpanded,
  darkMode,
  unmounted
});
</script>

<style scoped>
.sidebar-container {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  background-color: #ffffff;
  border-right: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
}

/* 侧边栏展开状态 */
.sidebar-container.expanded {
  width: v-bind('props.maxWidth + "px"');
}

/* 侧边栏折叠状态 */
.sidebar-container:not(.expanded) {
  width: v-bind('props.minWidth + "px"');
}

/* 暗黑模式 */
.sidebar-container.dark {
  background-color: #1e293b;
  border-right-color: #334155;
  color: #f1f5f9;
}

/* 侧边栏头部 */
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  border-bottom: 1px solid #e2e8f0;
  min-height: 60px;
}

.sidebar-container.dark .sidebar-header {
  border-bottom-color: #334155;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.3s ease;
}

.logo-container.compact {
  gap: 0;
  justify-content: center;
  width: 100%;
}

.logo-icon {
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  white-space: nowrap;
}

.sidebar-container.dark .logo-text {
  color: #f1f5f9;
}

.toggle-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  padding: 8px;
  border-radius: 4px;
  color: #64748b;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.toggle-btn:hover {
  background-color: #f1f5f9;
  color: #334155;
}

.sidebar-container.dark .toggle-btn {
  color: #94a3b8;
}

.sidebar-container.dark .toggle-btn:hover {
  background-color: #334155;
  color: #cbd5e1;
}

/* 侧边栏导航 */
.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 8px 0;
}

/* 滚动条样式 */
.sidebar-nav::-webkit-scrollbar {
  width: 4px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 2px;
}

.sidebar-container.dark .sidebar-nav::-webkit-scrollbar-thumb {
  background-color: #475569;
}

.nav-item {
  position: relative;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #475569;
  position: relative;
  white-space: nowrap;
}

.sidebar-container.dark .nav-link {
  color: #cbd5e1;
}

.nav-link:hover {
  background-color: #f1f5f9;
}

.sidebar-container.dark .nav-link:hover {
  background-color: #334155;
}

.nav-link.active {
  background-color: #dbeafe;
  color: #2563eb;
  border-right: 3px solid #3b82f6;
}

.sidebar-container.dark .nav-link.active {
  background-color: #1e3a8a;
  color: #93c5fd;
  border-right-color: #60a5fa;
}

.nav-icon {
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  flex-shrink: 0;
}

.nav-label {
  font-weight: 500;
  flex: 1;
}

.expand-icon {
  font-size: 0.8rem;
  transition: transform 0.2s ease;
  flex-shrink: 0;
}

.expand-icon.rotated {
  transform: rotate(180deg);
}

/* 子导航 */
.sub-nav {
  background-color: #f8fafc;
  border-left: 2px solid #e2e8f0;
  transition: all 0.3s ease;
}

.sidebar-container.dark .sub-nav {
  background-color: #0f172a;
  border-left-color: #334155;
}

.sub-nav-item {
  padding: 10px 16px 10px 48px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #64748b;
  position: relative;
  white-space: nowrap;
}

.sidebar-container.dark .sub-nav-item {
  color: #94a3b8;
}

.sub-nav-item:hover {
  background-color: #f1f5f9;
  color: #334155;
}

.sidebar-container.dark .sub-nav-item:hover {
  background-color: #1e293b;
  color: #cbd5e1;
}

.sub-nav-item.active {
  background-color: #dbeafe;
  color: #2563eb;
  font-weight: 500;
}

.sidebar-container.dark .sub-nav-item.active {
  background-color: #1e3a8a;
  color: #93c5fd;
}

.sub-nav-label {
  display: block;
}

.sub-nav-tooltip {
  display: none;
  position: absolute;
  left: 100%;
  top: 50%;
  transform: translateY(-50%);
  background-color: #334155;
  color: white;
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.8rem;
  white-space: nowrap;
  margin-left: 8px;
  z-index: 1001;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.sub-nav-tooltip::before {
  content: '';
  position: absolute;
  right: 100%;
  top: 50%;
  transform: translateY(-50%);
  border-width: 4px;
  border-style: solid;
  border-color: transparent #334155 transparent transparent;
}

/* 折叠时显示工具提示 */
.sidebar-container:not(.expanded) .sub-nav-tooltip {
  display: block;
}

/* 子导航过渡动画 */
.submenu-enter-active,
.submenu-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.submenu-enter-from,
.submenu-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateX(-10px);
}

.submenu-enter-to,
.submenu-leave-from {
  max-height: 500px;
  opacity: 1;
  transform: translateX(0);
}

/* 侧边栏底部 */
.sidebar-footer {
  border-top: 1px solid #e2e8f0;
  padding: 16px;
  transition: all 0.3s ease;
}

.sidebar-container.dark .sidebar-footer {
  border-top-color: #334155;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #3b82f6;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
}

.sidebar-container.dark .user-avatar {
  background-color: #60a5fa;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.user-name {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.9rem;
}

.sidebar-container.dark .user-name {
  color: #f1f5f9;
}

.user-role {
  font-size: 0.8rem;
  color: #64748b;
}

.sidebar-container.dark .user-role {
  color: #94a3b8;
}

.footer-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
}

.footer-actions.expanded {
  flex-direction: row;
  justify-content: center;
}

.footer-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  padding: 8px;
  border-radius: 4px;
  color: #64748b;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.footer-btn:hover {
  background-color: #f1f5f9;
  color: #334155;
}

.sidebar-container.dark .footer-btn {
  color: #94a3b8;
}

.sidebar-container.dark .footer-btn:hover {
  background-color: #334155;
  color: #cbd5e1;
}

.settings-btn:hover {
  background-color: #fef3c7;
  color: #d97706;
}

.sidebar-container.dark .settings-btn:hover {
  background-color: #92400e;
  color: #fcd34d;
}

.dark-mode-btn:hover {
  background-color: #e0f2fe;
  color: #0284c7;
}

.sidebar-container.dark .dark-mode-btn:hover {
  background-color: #0c4a6e;
  color: #7dd3fc;
}

.logout-btn:hover {
  background-color: #fee2e2;
  color: #dc2626;
}

.sidebar-container.dark .logout-btn:hover {
  background-color: #7f1d1d;
  color: #fecaca;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar-container.expanded {
    width: v-bind('props.maxWidth + "px"');
  }
  
  .sidebar-container:not(.expanded) {
    width: v-bind('props.minWidth + "px"');
  }
  
  /* 在移动设备上点击外部区域关闭侧边栏 */
  .sidebar-container.expanded::after {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: -1;
  }
}

@media (max-width: 480px) {
  .sidebar-container.expanded {
    width: 100vw;
  }
  
  .footer-actions.expanded {
    flex-direction: column;
    gap: 8px;
  }
  
  .user-info {
    flex-direction: column;
    text-align: center;
  }
}

/* 导航徽章 */
.nav-badge {
  margin-left: auto;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  background-color: #3b82f6;
  color: white;
  min-width: 20px;
  text-align: center;
}

.nav-badge.success {
  background-color: #22c55e;
}

.nav-badge.warning {
  background-color: #eab308;
}

.nav-badge.error {
  background-color: #ef4444;
}

/* 禁用状态 */
.nav-link.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.nav-link.disabled:hover {
  background-color: transparent;
}
</style>