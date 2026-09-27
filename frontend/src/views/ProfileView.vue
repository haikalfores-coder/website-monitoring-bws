<template>
  <div class="admin-wrapper relative bg-gray-50/50 min-h-screen">
    <!-- SIDEBAR (Disinkronkan dengan AdminDashboard) -->
    <aside class="sidebar print:hidden" :class="{ 'active': isSidebarOpen }">
      <div class="sidebar-brand">
        <!-- Path logo disamakan dengan dashboard -->
        <img src="/logo-pu.png" alt="Logo PU" class="sidebar-logo">
        <div class="sidebar-brand-text">
          <strong>BWS SUMATERA III</strong>
          <span>PEKANBARU</span>
        </div>
      </div>

      <nav class="sidebar-menu">
        <div class="menu-title">MENU UTAMA</div>
        <!-- Link untuk kembali ke halaman Admin Dashboard -->
        <router-link to="/admin" class="menu-item text-gray-500 hover:bg-gray-100">
          <i class="fa-solid fa-house"></i>
          <span>Dashboard & Data</span>
        </router-link>

        <div class="menu-title">SISTEM</div>
        <!-- Menu Profil Aktif -->
        <router-link to="/profil" class="menu-item active">
          <i class="fa-solid fa-user"></i>
          <span>Profil Saya</span>
        </router-link>
      </nav>

      <div class="sidebar-bottom">
        <a href="#" @click.prevent="handleLogout" class="menu-item logout">
          <i class="fa-solid fa-right-from-bracket"></i>
          <span>Logout</span>
        </a>
      </div>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="main-content">
      
      <!-- TOPBAR (Disinkronkan dengan AdminDashboard) -->
      <header class="topbar relative z-40 print:hidden bg-white shadow-sm">
        <div class="topbar-left">
          <button class="sidebar-toggle" @click="isSidebarOpen = !isSidebarOpen">
            <i class="fa-solid fa-bars"></i>
          </button>
          <div class="page-title">
            <h1>Profil Pengguna</h1>
            <p>Manajemen akun dan kredensial sistem</p>
          </div>
        </div>

        <div class="topbar-right flex items-center gap-4 relative">
          <!-- PROFIL INTERAKTIF -->
          <div class="relative" id="profile-menu">
            <div @click="toggleProfile" class="admin-profile cursor-pointer hover:bg-gray-50 p-2 rounded-xl transition flex items-center gap-3">
              <div class="admin-avatar bg-blue-100 text-blue-600 w-10 h-10 flex items-center justify-center rounded-full">
                <i class="fa-solid fa-user"></i>
              </div>
              <div class="admin-info hidden sm:block">
                <!-- Nama dan Jabatan Dinamis -->
                <strong class="block text-sm text-gray-800">@{{ authStore.username }}</strong>
                <span class="block text-xs text-gray-500">Admin Sektor {{ mySector }}</span>
              </div>
              <i class="fa-solid fa-chevron-down profile-arrow text-gray-400 text-xs transition-transform duration-300" :class="{'rotate-180': isProfileMenuOpen}"></i>
            </div>

            <!-- Dropdown Profil -->
            <transition name="fade-slide">
              <div v-if="isProfileMenuOpen" class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-2">
                <router-link to="/profil" class="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition">
                  <i class="fas fa-user-circle mr-2 w-4 text-center"></i> Profil Saya
                </router-link>
                <div class="border-t border-gray-100 my-1"></div>
                <a href="#" @click.prevent="handleLogout" class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition">
                  <i class="fas fa-sign-out-alt mr-2 w-4 text-center"></i> Keluar
                </a>
              </div>
            </transition>
          </div>
        </div>
      </header>

      <!-- CONTENT: FORM PENGATURAN MILIK ANDA -->
      <section class="content z-10 print:hidden">
        <div class="dashboard-grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          <!-- KARTU FOTO PROFIL -->
          <div class="dashboard-card col-span-1 p-6 border-2 border-blue-50 bg-white flex flex-col items-center text-center rounded-2xl shadow-sm">
            <div class="relative mb-4 group cursor-pointer">
              <div class="w-32 h-32 rounded-full bg-gradient-to-tr from-blue-100 to-blue-50 flex items-center justify-center border-4 border-white shadow-lg overflow-hidden">
                <i v-if="!profileImage" class="fa-solid fa-user text-5xl text-blue-300"></i>
                <img v-else :src="profileImage" class="w-full h-full object-cover">
              </div>
              <div class="absolute inset-0 bg-black/40 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition duration-300">
                <i class="fas fa-camera text-white text-xl"></i>
              </div>
            </div>
            
            <h3 class="font-bold text-xl text-gray-800">@{{ authStore.username }}</h3>
            <p class="text-sm text-blue-600 font-medium mb-1">Admin Sektor {{ mySector }}</p>
            <p class="text-xs text-gray-500 bg-gray-100 px-3 py-1 rounded-full mt-2">
              <i class="fas fa-id-badge mr-1"></i> NIP: {{ profileData.nip }}
            </p>
            
            <hr class="w-full my-6 border-gray-100">
            
            <div class="w-full text-left space-y-3">
              <div class="flex items-center gap-3 text-sm text-gray-600">
                <i class="fas fa-envelope text-gray-400 w-5"></i>
                <span>{{ profileData.email }}</span>
              </div>
              <div class="flex items-center gap-3 text-sm text-gray-600">
                <i class="fas fa-briefcase text-gray-400 w-5"></i>
                <span>{{ profileData.unitKerja }}</span>
              </div>
            </div>
          </div>

          <!-- FORM EDIT PROFIL -->
          <div class="dashboard-card col-span-1 lg:col-span-2 p-6 border border-gray-100 bg-white rounded-2xl shadow-sm">
            <div class="border-b border-gray-100 pb-4 mb-6">
              <h3 class="font-bold text-lg text-gray-800">Pengaturan Akun</h3>
              <p class="text-sm text-gray-500">Perbarui informasi dasar dan kredensial Anda.</p>
            </div>

            <form @submit.prevent="saveProfile" class="space-y-5">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-1">Nama Lengkap</label>
                  <input v-model="profileData.nama" type="text" class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition bg-gray-50 focus:bg-white" required>
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-1">NIP (Nomor Induk Pegawai)</label>
                  <input v-model="profileData.nip" type="text" class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition bg-gray-50 focus:bg-white" required>
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-1">Alamat Email</label>
                  <input v-model="profileData.email" type="email" class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition bg-gray-50 focus:bg-white">
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-1">Unit Kerja / Jabatan</label>
                  <input v-model="profileData.unitKerja" type="text" class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition bg-gray-50 focus:bg-white">
                </div>
              </div>

              <div class="border-t border-gray-100 pt-5 mt-2">
                <h4 class="font-semibold text-sm text-gray-800 mb-3"><i class="fas fa-lock mr-2 text-gray-400"></i>Ganti Password</h4>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                  <div>
                    <input type="password" placeholder="Password Baru" class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition bg-gray-50">
                  </div>
                  <div>
                    <input type="password" placeholder="Konfirmasi Password" class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition bg-gray-50">
                  </div>
                </div>
              </div>

              <div class="flex justify-end pt-4">
                <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-lg font-bold shadow-md shadow-blue-500/30 transition flex items-center gap-2" :disabled="isSaving">
                  <span v-if="isSaving"><i class="fas fa-spinner fa-spin mr-2"></i>Menyimpan...</span>
                  <span v-else><i class="fas fa-save mr-2"></i>Simpan Perubahan</span>
                </button>
              </div>
            </form>
          </div>

        </div>
      </section>

      <footer class="main-footer flex flex-wrap items-center justify-center gap-2 p-4 text-sm text-gray-500 mt-auto border-t bg-white relative z-10 print:hidden">
        <span>© 2026 Balai Wilayah Sungai Sumatera III Pekanbaru</span>
        <span class="hidden sm:inline px-1">|</span>
        <span>Kementerian Pekerjaan Umum</span>
      </footer>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import '@/assets/admin.css' 

const router = useRouter()
const authStore = useAuthStore()

// --- LOGIKA LAYOUT ---
const isSidebarOpen = ref(false)
const isProfileMenuOpen = ref(false)

// Pemetaan Sektor sesuai dengan AdminDashboard
const adminSectorMap = {
  'admin1': 'Siak',
  'admin2': 'Kampar',
  'admin3': 'Rokan',
  'admin4': 'Indragiri'
}
const mySector = computed(() => {
  return adminSectorMap[authStore.username] || 'Pusat'
})

const toggleProfile = () => {
  isProfileMenuOpen.value = !isProfileMenuOpen.value
}

const closeDropdownsOnClickOutside = (e) => {
  if (!e.target.closest('#profile-menu')) isProfileMenuOpen.value = false
}

// --- LOGIKA PROFIL MILIK ANDA ---
const isSaving = ref(false)
const profileImage = ref('')

const profileData = reactive({
  nama: 'Administrator Data',
  nip: '19850101 201012 1 001',
  email: 'admin@bws-sumatera3.go.id',
  unitKerja: 'BWS Sumatera III Pekanbaru'
})

onMounted(() => {
  if (!authStore.isAuthenticated || authStore.role !== 'admin') {
    router.push('/')
  }
  document.addEventListener('click', closeDropdownsOnClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', closeDropdownsOnClickOutside)
})

const saveProfile = () => {
  isSaving.value = true
  setTimeout(() => {
    isSaving.value = false
    alert('Profil berhasil diperbarui!')
  }, 800)
}

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.fade-slide-enter-active, .fade-slide-leave-active {
  transition: all 0.2s ease;
}
.fade-slide-enter-from, .fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>