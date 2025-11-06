import { createApp } from 'vue'
import App from './AdminApp.vue'
import router from './router/adminRouter.js'
import { createPinia } from 'pinia'
import './assets/admin.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#admin-app')