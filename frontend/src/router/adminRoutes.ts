import { createRouter, createWebHistory } from 'vue-router';

// 路由元信息类型
export interface RouteMeta {
  requiresAuth?: boolean;
  title?: string;
  icon?: string;
}

export const adminRoutes = [
  {
    path: '/admin',
    redirect: '/admin/dashboard',
    component: () => import('@/components/admin/AdminLayout.vue'),
    meta: { requiresAuth: true } as RouteMeta,
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: {
          requiresAuth: true,
          title: '仪表盘',
          icon: 'el-icon-data-line'
        } as RouteMeta
      },
      {
        path: 'folk-culture',
        name: 'AdminFolkCulture',
        component: () => import('@/views/admin/FolkCultureManage.vue'),
        meta: {
          requiresAuth: true,
          title: '民俗文化管理',
          icon: 'el-icon-document'
        } as RouteMeta
      },
      {
        path: 'batch-upload',
        name: 'AdminBatchUpload',
        component: () => import('@/views/admin/BatchUpload.vue'),
        meta: {
          requiresAuth: true,
          title: '批量上传',
          icon: 'el-icon-upload'
        } as RouteMeta
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/UserManage.vue'),
        meta: {
          requiresAuth: true,
          title: '用户管理',
          icon: 'el-icon-user'
        } as RouteMeta
      },
      {
        path: 'settings',
        name: 'AdminSettings',
        component: () => import('@/views/admin/Settings.vue'),
        meta: {
          requiresAuth: true,
          title: '系统设置',
          icon: 'el-icon-setting'
        } as RouteMeta
      }
    ]
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('@/views/admin/AdminLogin.vue'),
    meta: { requiresAuth: false, title: '管理员登录' } as RouteMeta
  },
  {
    path: '/admin/logout',
    name: 'AdminLogout',
    component: () => import('@/views/admin/AdminLogout.vue'),
    meta: { requiresAuth: true, title: '退出登录' } as RouteMeta
  }
];

// 创建管理员路由实例
const adminRouter = createRouter({
  history: createWebHistory('/admin'),
  routes: adminRoutes
});

// 路由守卫 - 验证登录状态
adminRouter.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 民俗文化管理系统`;
  }
  
  // 检查是否需要认证
  const requiresAuth = to.meta.requiresAuth !== false;
  const token = localStorage.getItem('adminToken');
  
  if (requiresAuth && !token) {
    // 需要认证但没有token，重定向到登录页
    next('/admin/login');
  } else if (to.path === '/admin/login' && token) {
    // 已登录用户访问登录页，重定向到仪表盘
    next('/admin/dashboard');
  } else {
    // 正常访问
    next();
  }
});

export default adminRouter;