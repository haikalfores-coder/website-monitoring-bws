<template>
  <nav class="glass-header sticky top-0 z-50 px-6 py-4 flex justify-between items-center no-print backdrop-blur-md bg-white/40 border-b border-white/60 shadow-sm">
    <!-- Bagian Kiri: Logo & Judul -->
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-sm">
        <i class="fas fa-water text-blue-500"></i>
      </div>
      <div>
        <h1 class="font-bold text-lg text-slate-800 leading-tight">Monitoring Kegiatan</h1>
        <p class="text-xs text-slate-500">BWS Sumatera III Pekanbaru</p>
      </div>
    </div>

    <!-- Bagian Kanan: Info User & Tombol Keluar -->
    <div class="flex items-center gap-4">
      <div class="text-right hidden sm:block">
        <p class="text-sm font-semibold text-slate-700">
          Halo, {{ authStore.role === 'admin' ? 'Admin' : 'Superuser' }}
        </p>
        <p class="text-xs text-slate-500">
          Hak Akses: {{ displayRole }}
        </p>
      </div>
      
      <button 
        @click="handleLogout" 
        class="px-4 py-2 bg-red-50 text-red-600 hover:bg-red-100 rounded-lg text-sm font-semibold transition"
      >
        <i class="fas fa-sign-out-alt mr-1"></i> Keluar
      </button>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Mengubah format teks role menjadi huruf kapital
const displayRole = computed(() => {
  return authStore.role ? authStore.role.toUpperCase() : ''
})

const handleLogout = () => {
  // Panggil fungsi logout di Pinia store
  authStore.logout()
  
  // Arahkan kembali ke halaman login
  router.push('/')
}
</script>