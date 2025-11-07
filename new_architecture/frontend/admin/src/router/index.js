import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import CultureManagement from '../views/CultureManagement.vue'
import Settings from '../views/Settings.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/culture-management',
    name: 'CultureManagement',
    component: CultureManagement
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router