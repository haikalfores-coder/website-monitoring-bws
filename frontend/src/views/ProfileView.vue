<template>
  <div class="admin-wrapper relative bg-gray-50/50 min-h-screen">

    <!-- SIDEBAR -->
    <aside
      class="sidebar print:hidden"
      :class="{ active: isSidebarOpen }"
    >
      <div class="sidebar-brand">
        <img src="/logo-pu.png" alt="Logo PU" class="sidebar-logo">

        <div class="sidebar-brand-text">
          <strong>BWS SUMATERA III</strong>
          <span>PEKANBARU</span>
        </div>
      </div>

      <nav class="sidebar-menu">

        <div class="menu-title">
          MENU UTAMA
        </div>

        <router-link
          to="/admin"
          class="menu-item text-gray-500 hover:bg-gray-100"
        >
          <i class="fa-solid fa-house"></i>
          <span>Dashboard & Data</span>
        </router-link>

        <div class="menu-title">
          SISTEM
        </div>

        <router-link
          to="/profil"
          class="menu-item active"
        >
          <i class="fa-solid fa-user"></i>
          <span>Profil Saya</span>
        </router-link>

      </nav>

      <!-- LOGOUT -->
      <div class="sidebar-bottom">
        <a
          href="#"
          @click.prevent="handleLogout"
          class="menu-item logout"
        >
          <i class="fa-solid fa-right-from-bracket"></i>
          <span>Logout</span>
        </a>
      </div>
    </aside>


    <!-- MAIN CONTENT -->
    <main class="main-content">

      <!-- TOPBAR -->
      <header
        class="topbar relative z-40 print:hidden bg-white shadow-sm"
      >

        <div class="topbar-left">

          <button
            class="sidebar-toggle"
            @click="isSidebarOpen = !isSidebarOpen"
          >
            <i class="fa-solid fa-bars"></i>
          </button>

          <div class="page-title">
            <h1>Profil Pengguna</h1>

            <p>
              Informasi profil administrator
            </p>
          </div>

        </div>


        <!-- PROFIL DI TOPBAR -->
        <div class="topbar-right flex items-center gap-4 relative">

          <div
            class="relative"
            id="profile-menu"
          >

            <div
              @click="toggleProfile"
              class="admin-profile cursor-pointer hover:bg-gray-50 p-2 rounded-xl transition flex items-center gap-3"
            >

              <div
                class="admin-avatar bg-blue-100 text-blue-600 w-10 h-10 flex items-center justify-center rounded-full"
              >
                <i class="fa-solid fa-user"></i>
              </div>

              <div class="admin-info hidden sm:block">

                <strong class="block text-sm text-gray-800">
                  {{ authStore.username }}
                </strong>

                <span class="block text-xs text-gray-500">
                  Admin Sektor {{ mySector }}
                </span>

              </div>

              <i
                class="fa-solid fa-chevron-down profile-arrow text-gray-400 text-xs transition-transform duration-300"
                :class="{
                  'rotate-180': isProfileMenuOpen
                }"
              ></i>

            </div>


            <!-- DROPDOWN PROFIL -->
            <transition name="fade-slide">

              <div
                v-if="isProfileMenuOpen"
                class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-2"
              >

                <router-link
                  to="/profil"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition"
                >
                  <i class="fas fa-user-circle mr-2 w-4 text-center"></i>
                  Profil Saya
                </router-link>

                <div class="border-t border-gray-100 my-1"></div>

                <a
                  href="#"
                  @click.prevent="handleLogout"
                  class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition"
                >
                  <i class="fas fa-sign-out-alt mr-2 w-4 text-center"></i>
                  Keluar
                </a>

              </div>

            </transition>

          </div>

        </div>

      </header>


      <!-- CONTENT -->
      <section class="content z-10">

        <div
          class="dashboard-grid grid-cols-1 lg:grid-cols-3 gap-6"
        >

          <!-- KARTU INFORMASI PROFIL -->
          <div
            class="dashboard-card col-span-1 p-6 border-2 border-blue-50 bg-white flex flex-col items-center text-center rounded-2xl shadow-sm"
          >

            <!-- FOTO PROFIL -->
            <div class="relative mb-4">

              <div
                class="w-32 h-32 rounded-full bg-gradient-to-tr from-blue-100 to-blue-50 flex items-center justify-center border-4 border-white shadow-lg overflow-hidden"
              >

                <i
                  v-if="!profileImage"
                  class="fa-solid fa-user text-5xl text-blue-300"
                ></i>

                <img
                  v-else
                  :src="profileImage"
                  alt="Foto Profil"
                  class="w-full h-full object-cover"
                >

              </div>

            </div>


            <!-- NAMA -->
            <h3 class="font-bold text-xl text-gray-800">
              {{ authStore.username }}
            </h3>


            <!-- SEKTOR -->
            <p class="text-sm text-blue-600 font-medium mb-1">
              Admin Sektor {{ mySector }}
            </p>


            <!-- NIP -->
            <p
              class="text-xs text-gray-500 bg-gray-100 px-3 py-1 rounded-full mt-2"
            >
              <i class="fas fa-id-badge mr-1"></i>
              NIP: {{ profileData.nip }}
            </p>


            <hr class="w-full my-6 border-gray-100">


            <!-- INFORMASI -->
            <div class="w-full text-left space-y-3">

              <div
                class="flex items-center gap-3 text-sm text-gray-600"
              >

                <i
                  class="fas fa-envelope text-gray-400 w-5"
                ></i>

                <span>
                  {{ profileData.email }}
                </span>

              </div>


              <div
                class="flex items-center gap-3 text-sm text-gray-600"
              >

                <i
                  class="fas fa-briefcase text-gray-400 w-5"
                ></i>

                <span>
                  {{ profileData.unitKerja }}
                </span>

              </div>

            </div>

          </div>


          <!-- INFORMASI DATA ADMIN -->
          <div
            class="dashboard-card col-span-1 lg:col-span-2 p-6 border border-gray-100 bg-white rounded-2xl shadow-sm"
          >

            <div
              class="border-b border-gray-100 pb-4 mb-6"
            >

              <h3 class="font-bold text-lg text-gray-800">
                Informasi Administrator
              </h3>

              <p class="text-sm text-gray-500">
                Informasi pengguna yang sedang login pada sistem.
              </p>

            </div>


            <!-- DATA PROFIL -->
            <div class="space-y-5">

              <!-- NAMA -->
              <div>

                <label
                  class="block text-sm font-semibold text-gray-700 mb-1"
                >
                  Nama Lengkap
                </label>

                <div
                  class="w-full border border-gray-200 bg-gray-50 p-3 rounded-lg text-gray-700"
                >
                  {{ profileData.nama }}
                </div>

              </div>


              <!-- NIP -->
              <div>

                <label
                  class="block text-sm font-semibold text-gray-700 mb-1"
                >
                  NIP
                </label>

                <div
                  class="w-full border border-gray-200 bg-gray-50 p-3 rounded-lg text-gray-700"
                >
                  {{ profileData.nip }}
                </div>

              </div>


              <!-- EMAIL -->
              <div>

                <label
                  class="block text-sm font-semibold text-gray-700 mb-1"
                >
                  Alamat Email
                </label>

                <div
                  class="w-full border border-gray-200 bg-gray-50 p-3 rounded-lg text-gray-700"
                >
                  {{ profileData.email }}
                </div>

              </div>


              <!-- UNIT KERJA -->
              <div>

                <label
                  class="block text-sm font-semibold text-gray-700 mb-1"
                >
                  Unit Kerja / Jabatan
                </label>

                <div
                  class="w-full border border-gray-200 bg-gray-50 p-3 rounded-lg text-gray-700"
                >
                  {{ profileData.unitKerja }}
                </div>

              </div>


              <!-- SEKTOR -->
              <div>

                <label
                  class="block text-sm font-semibold text-gray-700 mb-1"
                >
                  Sektor
                </label>

                <div
                  class="w-full border border-gray-200 bg-gray-50 p-3 rounded-lg text-gray-700"
                >
                  Admin Sektor {{ mySector }}
                </div>

              </div>


              <!-- STATUS -->
              <div>

                <label
                  class="block text-sm font-semibold text-gray-700 mb-1"
                >
                  Status Akun
                </label>

                <div
                  class="inline-flex items-center gap-2 bg-green-50 text-green-700 px-4 py-2 rounded-lg text-sm font-medium"
                >

                  <span
                    class="w-2 h-2 bg-green-500 rounded-full"
                  ></span>

                  Aktif

                </div>

              </div>

            </div>

          </div>

        </div>

      </section>


      <!-- FOOTER -->
      <footer
        class="main-footer flex flex-wrap items-center justify-center gap-2 p-4 text-sm text-gray-500 mt-auto border-t bg-white relative z-10 print:hidden"
      >

        <span>
          © 2026 Balai Wilayah Sungai Sumatera III Pekanbaru
        </span>

        <span class="hidden sm:inline px-1">
          |
        </span>

        <span>
          Kementerian Pekerjaan Umum
        </span>

      </footer>

    </main>

  </div>
</template>


<script setup>

import {
  ref,
  reactive,
  computed,
  onMounted,
  onUnmounted
} from 'vue'

import { useRouter } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

import '@/assets/admin.css'


// ===============================
// ROUTER & AUTH
// ===============================

const router = useRouter()

const authStore = useAuthStore()


// ===============================
// LAYOUT
// ===============================

const isSidebarOpen = ref(false)

const isProfileMenuOpen = ref(false)


// ===============================
// PEMETAAN SEKTOR ADMIN
// ===============================

const adminSectorMap = {

  admin1: 'Siak',

  admin2: 'Kampar',

  admin3: 'Rokan',

  admin4: 'Indragiri'

}


const mySector = computed(() => {

  return adminSectorMap[authStore.username] || 'Pusat'

})


// ===============================
// DROPDOWN PROFIL
// ===============================

const toggleProfile = () => {

  isProfileMenuOpen.value =
    !isProfileMenuOpen.value

}


const closeDropdownsOnClickOutside = (e) => {

  if (
    !e.target.closest('#profile-menu')
  ) {

    isProfileMenuOpen.value = false

  }

}


// ===============================
// DATA PROFIL
// ===============================

const profileImage = ref('')


const profileData = reactive({

  nama: 'Administrator Data',

  nip: '19850101 201012 1 001',

  email: 'admin@bws-sumatera3.go.id',

  unitKerja: 'BWS Sumatera III Pekanbaru'

})


// ===============================
// CEK AUTENTIKASI
// ===============================

onMounted(() => {

  if (
    !authStore.isAuthenticated ||
    authStore.role !== 'admin'
  ) {

    router.push('/')

    return

  }


  document.addEventListener(
    'click',
    closeDropdownsOnClickOutside
  )

})


onUnmounted(() => {

  document.removeEventListener(
    'click',
    closeDropdownsOnClickOutside
  )

})


// ===============================
// LOGOUT
// ===============================

const handleLogout = () => {

  authStore.logout()

  router.push('/')

}

</script>


<style scoped>

.fade-slide-enter-active,
.fade-slide-leave-active {

  transition: all 0.2s ease;

}


.fade-slide-enter-from,
.fade-slide-leave-to {

  opacity: 0;

  transform: translateY(-10px);

}

</style>