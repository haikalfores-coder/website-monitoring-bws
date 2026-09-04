import { createRouter, createWebHistory } from 'vue-router'

// Impor semua halaman
import LoginView from '../views/LoginView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import ProfileView from '../views/ProfileView.vue'
import SuperuserDashboard from '../views/SuperuserDashboard.vue'
import SuperuserProfile from '../views/SuperuserProfile.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboard
    },
    {
      path: '/profil',
      name: 'profil',
      component: ProfileView
    },
    {
      path: '/superuser',
      name: 'superuser',
      component: SuperuserDashboard
    },
    {
      // <-- INI ADALAH RUTE UNTUK PROFIL SUPERUSER
      path: '/superuser-profil',
      name: 'superuser-profil',
      component: SuperuserProfile 
    },
  ]
})

export default router