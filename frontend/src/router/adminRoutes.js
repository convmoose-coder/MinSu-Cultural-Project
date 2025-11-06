import AdminLogin from '../views/admin/AdminLogin.vue'
import AdminRegister from '../views/admin/Register.vue'
import AdminLogout from '../views/admin/AdminLogout.vue'
import AdminLayout from '../components/admin/AdminLayout.vue'

// 后台路由配置 - 专注于用户端配置功能
export const adminRoutes = [
  // 管理员登录相关路由（无需布局）
  {
    path: '/admin/login',
    name: 'adminLogin',
    component: AdminLogin,
    meta: {
      title: '管理员登录',
      requiresAuth: false
    }
  },
  {
    path: '/admin/register',
    name: 'adminRegister',
    component: AdminRegister,
    meta: {
      title: '管理员注册',
      requiresAuth: false
    }
  },
  {
    path: '/admin/logout',
    name: 'adminLogout',
    component: AdminLogout,
    meta: {
      title: '管理员注销'
    }
  },
  // 管理员后台主布局和页面
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      {
        path: '',
        redirect: '/admin/system-config'
      },
      {
        path: 'system-config',
        name: 'adminSystemConfig',
        component: () => import('@/views/admin/SystemConfig.vue'),
        meta: {
          title: '系统配置',
          breadcrumb: ['系统管理', '系统配置']
        }
      },
      {
        path: 'user-management',
        name: 'adminUserManagement',
        component: () => import('@/views/admin/UserManagement.vue'),
        meta: {
          title: '用户管理',
          breadcrumb: ['系统管理', '用户管理']
        }
      },
      {
        path: 'content-config',
        name: 'adminContentConfig',
        component: () => import('@/views/admin/ContentConfig.vue'),
        meta: {
          title: '内容配置',
          breadcrumb: ['内容管理', '内容配置']
        }
      },
      {
        path: 'data-config',
        name: 'adminDataConfig',
        component: () => import('@/views/admin/DataConfig.vue'),
        meta: {
          title: '数据配置',
          breadcrumb: ['数据管理', '数据配置']
        }
      }
    ]
  }
]