import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/culture',
      name: 'culture',
      component: () => import('../views/CultureListView.vue')
    },
    {
      path: '/culture/:id',
      name: 'cultureDetail',
      component: () => import('../views/CultureDetailView.vue')
    },
    {
      path: '/regions',
      name: 'regions',
      component: () => import('../views/RegionsView.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router