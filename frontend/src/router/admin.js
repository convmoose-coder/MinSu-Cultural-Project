import { createRouter, createWebHistory } from 'vue-router';
import AdminLayout from '../components/layouts/AdminLayout.vue';
import Dashboard from '../views/admin/Dashboard.vue';
import Login from '../views/admin/Login.vue';
import Register from '../views/admin/Register.vue';
import BatchUpload from '../views/admin/BatchUpload.vue';

// 模拟认证检查
const checkAuth = (to, from, next) => {
  // 实际项目中应该使用真实的认证逻辑
  const isAuthenticated = localStorage.getItem('adminToken');
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'AdminLogin' });
    } else {
      next();
    }
  } else {
    next();
  }
};

const routes = [
  {
    path: '/admin',
    component: AdminLayout,
    beforeEnter: checkAuth,
    children: [
      {
        path: '',
        redirect: 'dashboard'
      },
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: Dashboard,
        meta: { requiresAuth: true }
      },
      {
        path: 'batch-upload',
        name: 'BatchUpload',
        component: BatchUpload,
        meta: { requiresAuth: true }
      }
    ]
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: Login
  },
  {
    path: '/admin/register',
    name: 'AdminRegister',
    component: Register
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;