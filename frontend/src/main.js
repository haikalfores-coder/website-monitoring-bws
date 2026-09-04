import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router' // Memanggil router yang baru dibuat

// Impor CSS Tailwind
import './assets/style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router) // Mendaftarkan router ke aplikasi

app.mount('#app')