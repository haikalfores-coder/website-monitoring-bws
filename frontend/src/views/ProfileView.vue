<template>
  <div class="admin-wrapper relative">
    <!-- SIDEBAR -->
    <aside class="sidebar print:hidden" :class="{ 'active': isSidebarOpen }">
      <div class="sidebar-brand">
        <img src="@/assets/images/logo-pu.png" alt="Logo PU" class="sidebar-logo">
        <div class="sidebar-brand-text">
          <strong>BWS SUMATERA III</strong>
          <span>PEKANBARU</span>
        </div>
      </div>

      <nav class="sidebar-menu">
        <div class="menu-title">MENU UTAMA</div>
        <!-- Class 'active' dihapus, diganti menjadi link kembali ke dashboard -->
        <router-link to="/admin" class="menu-item">
          <i class="fa-solid fa-house"></i>
          <span>Dashboard</span>
        </router-link>

        <div class="menu-title">DATA</div>
        <router-link to="/admin" class="menu-item">
          <i class="fa-solid fa-clipboard-list"></i>
          <span>Data Kegiatan</span>
        </router-link>
        
        <!-- Menu Siapkan Laporan sudah dihapus -->

        <a href="#" @click.prevent="printLaporan" class="menu-item text-green-600 font-bold bg-green-50">
          <i class="fa-solid fa-file-pdf"></i>
          <span>Cetak PDF Laporan</span>
        </a>

        <div class="menu-title">SISTEM</div>
        <!-- Class 'active' dipindahkan ke sini -->
        <a href="#" class="menu-item active">
          <i class="fa-solid fa-user"></i>
          <span>Profil</span>
        </a>
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
      
      <!-- TOPBAR KONSISTEN DENGAN DASHBOARD -->
      <header class="topbar relative z-40">
        <div class="topbar-left">
          <div class="page-title">
            <h1>Profil Pengguna</h1>
            <p>Manajemen akun dan preferensi sistem</p>
          </div>
        </div>

        <div class="topbar-right flex items-center gap-4 relative">
          
          <!-- Notifikasi Interaktif -->
          <div class="relative" id="notification-menu">
            <button @click="toggleNotification" class="notification-button hover:bg-gray-100 p-2 rounded-full transition">
              <i class="fa-regular fa-bell text-gray-600 text-xl"></i>
              <span v-if="unreadNotifications > 0" class="notification-badge bg-red-500 text-white text-xs font-bold w-5 h-5 flex items-center justify-center rounded-full absolute -top-1 -right-1 border-2 border-white">
                {{ unreadNotifications }}
              </span>
            </button>

            <!-- Dropdown Notifikasi -->
            <transition name="fade-slide">
              <div v-if="isNotificationOpen" class="absolute right-0 mt-3 w-80 bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden">
                <div class="p-4 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
                  <h4 class="font-bold text-gray-700">Notifikasi</h4>
                  <button @click="markAllAsRead" class="text-xs text-blue-600 hover:underline">Tandai dibaca</button>
                </div>
                <div class="max-h-72 overflow-y-auto">
                  <div v-for="notif in notifications" :key="notif.id" class="p-4 border-b border-gray-50 hover:bg-blue-50/50 transition cursor-pointer flex gap-3" :class="{'opacity-60': notif.read}">
                    <div class="mt-1">
                      <i class="fas fa-info-circle text-blue-500" v-if="notif.type === 'info'"></i>
                      <i class="fas fa-check-circle text-green-500" v-else-if="notif.type === 'success'"></i>
                    </div>
                    <div>
                      <p class="text-sm text-gray-800 line-clamp-2">{{ notif.message }}</p>
                      <span class="text-xs text-gray-400">{{ notif.time }}</span>
                    </div>
                  </div>
                  <div v-if="notifications.length === 0" class="p-6 text-center text-gray-500 text-sm">
                    Belum ada notifikasi baru.
                  </div>
                </div>
              </div>
            </transition>
          </div>

          <!-- Profil Interaktif -->
          <div class="relative" id="profile-menu">
            <div @click="toggleProfile" class="admin-profile cursor-pointer hover:bg-gray-50 p-2 rounded-xl transition flex items-center gap-3">
              <div class="admin-avatar bg-blue-100 text-blue-600 w-10 h-10 flex items-center justify-center rounded-full">
                <i class="fa-solid fa-user"></i>
              </div>
              <div class="admin-info hidden sm:block">
                <strong class="block text-sm text-gray-800">{{ profileData.nama }}</strong>
                <span class="block text-xs text-gray-500">Administrator</span>
              </div>
              <i class="fa-solid fa-chevron-down profile-arrow text-gray-400 text-xs transition-transform duration-300" :class="{'rotate-180': isProfileMenuOpen}"></i>
            </div>

            <!-- Dropdown Profil -->
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

      <!-- CONTENT -->
      <section class="content z-10">
        <div class="dashboard-grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          <!-- KARTU FOTO PROFIL -->
          <div class="dashboard-card col-span-1 p-6 border-2 border-blue-50 bg-white flex flex-col items-center text-center">
            <div class="relative mb-4 group cursor-pointer">
              <div class="w-32 h-32 rounded-full bg-gradient-to-tr from-blue-100 to-blue-50 flex items-center justify-center border-4 border-white shadow-lg overflow-hidden">
                <i v-if="!profileImage" class="fa-solid fa-user text-5xl text-blue-300"></i>
                <img v-else :src="profileImage" class="w-full h-full object-cover">
              </div>
              <div class="absolute inset-0 bg-black/40 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition duration-300">
                <i class="fas fa-camera text-white text-xl"></i>
              </div>
            </div>
            <h3 class="font-bold text-xl text-gray-800">{{ profileData.nama }}</h3>
            <p class="text-sm text-blue-600 font-medium mb-1">Administrator Sistem</p>
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
          <div class="dashboard-card col-span-1 lg:col-span-2 p-6 border border-gray-100">
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

      <footer class="main-footer flex flex-wrap items-center justify-center gap-2 p-4 text-sm text-gray-500 mt-auto border-t bg-white relative z-10">
        <span>© 2026 Balai Wilayah Sungai Sumatera III Pekanbaru</span>
      </footer>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useActivityStore } from '@/stores/activities'
import '@/assets/admin.css' 

const router = useRouter()
const authStore = useAuthStore()
const activityStore = useActivityStore()

// --- LOGIKA TOPBAR (NOTIFIKASI & PROFIL) ---
const isNotificationOpen = ref(false)
const isProfileMenuOpen = ref(false)

// State Notifikasi Kosong
const notifications = ref([])

const unreadNotifications = computed(() => notifications.value.filter(n => !n.read).length)

const toggleNotification = () => {
  isNotificationOpen.value = !isNotificationOpen.value
  isProfileMenuOpen.value = false
}
const toggleProfile = () => {
  isProfileMenuOpen.value = !isProfileMenuOpen.value
  isNotificationOpen.value = false
}
const markAllAsRead = () => {
  notifications.value.forEach(n => n.read = true)
}

const closeDropdownsOnClickOutside = (e) => {
  if (!e.target.closest('#notification-menu')) isNotificationOpen.value = false
  if (!e.target.closest('#profile-menu')) isProfileMenuOpen.value = false
}

// --- LOGIKA PROFIL ---
const isSaving = ref(false)
const profileImage = ref('')

const profileData = reactive({
  nama: 'Admin',
  nip: '19850101 201012 1 001',
  email: 'admin@bws-sumatera3.go.id',
  unitKerja: 'BWS Sumatera III Pekanbaru'
})

onMounted(() => {
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

const prepareReport = async () => {
  await activityStore.prepareReport()
  alert('Laporan berhasil disiapkan! Superuser sekarang dapat mengunduhnya.')
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