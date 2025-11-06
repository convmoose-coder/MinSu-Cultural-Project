import { createRouter, createWebHistory } from 'vue-router'
import AdminLayout from '../../components/admin/AdminLayout.vue'
import DashboardView from '../../views/admin/Dashboard.vue'
import BatchUploadView from '../../views/admin/BatchUpload.vue'
import AdminLogin from '../../views/admin/AdminLogin.vue'
import AdminLogout from '../../views/admin/AdminLogout.vue'
import AdminRegister from '../../views/admin/Register.vue'

const adminRoutes = [
  // 登录页
  {
    path: '/admin/login',
    name: 'adminLogin',
    component: AdminLogin,
    meta: {
      title: '管理员登录',
      requiresAuth: false
    }
  },
  // 注册页
  {
    path: '/admin/register',
    name: 'adminRegister',
    component: AdminRegister,
    meta: {
      title: '管理员注册',
      requiresAuth: false
    }
  },
  // 注销页
  {
    path: '/admin/logout',
    name: 'adminLogout',
    component: AdminLogout,
    meta: {
      title: '管理员注销'
    }
  },
  // 主布局
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      // 控制面板
      {
        path: '',
        redirect: '/admin/dashboard'
      },
      {
        path: 'dashboard',
        name: 'adminDashboard',
        component: DashboardView,
        meta: {
          title: '控制面板概览',
          breadcrumb: ['控制面板', '概览']
        }
      },
      // 批量上传
      {
        path: 'batch-upload',
        name: 'adminBatchUpload',
        component: BatchUploadView,
        meta: {
          title: '数据批量上传',
          breadcrumb: ['数据管理', '批量上传']
        }
      },
      // 民俗文化管理
      {
        path: 'culture-management',
        name: 'adminCultureManagement',
        component: () => import('../../views/admin/CultureManagement.vue'),
        meta: {
          title: '民俗文化管理',
          breadcrumb: ['数据管理', '民俗文化']
        }
      },
      // 分类管理
      {
        path: 'category-management',
        name: 'adminCategoryManagement',
        component: () => import('../../views/admin/CategoryManagement.vue'),
        meta: {
          title: '分类管理',
          breadcrumb: ['数据管理', '分类管理']
        }
      },
      // 地区管理
      {
        path: 'region-management',
        name: 'adminRegionManagement',
        component: () => import('../../views/admin/RegionManagement.vue'),
        meta: {
          title: '地区管理',
          breadcrumb: ['数据管理', '地区管理']
        }
      }
    ]
  }
]

export default adminRoutes
