<template>
  <div class="admin-wrapper relative bg-gray-50/50 min-h-screen">

    <!-- ========================================== -->
    <!-- OVERLAY MOBILE -->
    <!-- ========================================== -->
    <div
      v-if="isSidebarOpen"
      @click="isSidebarOpen = false"
      class="fixed inset-0 bg-black/50 z-40 lg:hidden backdrop-blur-sm transition-opacity"
    ></div>


    <!-- ========================================== -->
    <!-- SIDEBAR -->
    <!-- ========================================== -->
    <aside
      class="sidebar print:hidden"
      :class="{ active: isSidebarOpen }"
    >

      <!-- BRAND -->
      <div class="sidebar-brand">

        <img
          src="/logo-pu.png"
          alt="Logo PU"
          class="sidebar-logo"
        />

        <div class="sidebar-brand-text">
          <strong>BWS SUMATERA III</strong>
          <span>PEKANBARU</span>
        </div>

      </div>


      <!-- MENU -->
      <nav class="sidebar-menu">

        <!-- MENU UTAMA -->
        <div class="menu-title">
          MENU UTAMA
        </div>


        <!-- DASHBOARD -->
        <router-link
          to="/superuser"
          class="menu-item"
          @click="isSidebarOpen = false"
        >
          <i class="fa-solid fa-house"></i>

          <span>
            Dashboard & Data
          </span>
        </router-link>


        <!-- SISTEM -->
        <div class="menu-title">
          SISTEM
        </div>


        <!-- PROFIL -->
        <a
          href="#"
          class="menu-item active"
          @click.prevent="isSidebarOpen = false"
        >
          <i class="fa-solid fa-user"></i>

          <span>
            Profil Saya
          </span>
        </a>

      </nav>


      <!-- LOGOUT -->
      <div class="sidebar-bottom">

        <a
          href="#"
          @click.prevent="handleLogout"
          class="menu-item logout"
        >
          <i class="fa-solid fa-right-from-bracket"></i>

          <span>
            Logout
          </span>
        </a>

      </div>

    </aside>


    <!-- ========================================== -->
    <!-- MAIN CONTENT -->
    <!-- ========================================== -->
    <main class="main-content">


      <!-- ========================================== -->
      <!-- TOPBAR -->
      <!-- ========================================== -->
      <header
        class="topbar relative z-40 print:hidden bg-white shadow-sm"
      >

        <div class="topbar-left">

          <!-- HAMBURGER -->
          <button
            class="sidebar-toggle"
            @click="isSidebarOpen = !isSidebarOpen"
          >
            <i class="fa-solid fa-bars"></i>
          </button>


          <!-- JUDUL -->
          <div class="page-title hidden sm:block">

            <h1 class="text-xl font-bold text-gray-800">
              Profil Pimpinan
            </h1>

            <p class="text-xs text-gray-500">
              Informasi dan pengaturan profil Pimpinan
            </p>

          </div>

        </div>


        <!-- ========================================== -->
        <!-- TOPBAR RIGHT -->
        <!-- ========================================== -->
        <div
          class="topbar-right flex items-center gap-4 relative"
        >


          <!-- ======================================== -->
          <!-- NOTIFIKASI -->
          <!-- ======================================== -->
          <div
            class="relative"
            id="notification-menu"
          >

            <button
              @click="toggleNotification"
              class="notification-button hover:bg-gray-100 p-2 rounded-full transition relative"
            >

              <i
                class="fa-regular fa-bell text-gray-600 text-xl"
              ></i>


              <!-- BADGE NOTIFIKASI -->
              <span
                v-if="unreadNotifications > 0"
                class="notification-badge bg-red-500 text-white text-xs font-bold w-5 h-5 flex items-center justify-center rounded-full absolute -top-1 -right-1 border-2 border-white"
              >
                {{ unreadNotifications }}
              </span>

            </button>


            <!-- DROPDOWN NOTIFIKASI -->
            <transition name="fade-slide">

              <div
                v-if="isNotificationOpen"
                class="absolute right-0 mt-3 w-80 bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden z-50"
              >

                <!-- HEADER -->
                <div
                  class="p-4 border-b border-gray-100 bg-gray-50 flex justify-between items-center"
                >

                  <h4
                    class="font-bold text-gray-700"
                  >
                    Notifikasi
                  </h4>


                  <button
                    @click="markAllAsRead"
                    class="text-xs text-blue-600 hover:underline"
                  >
                    Tandai dibaca
                  </button>

                </div>


                <!-- LIST NOTIFIKASI -->
                <div
                  class="max-h-72 overflow-y-auto"
                >

                  <!-- KOSONG -->
                  <div
                    v-if="notifications.length === 0"
                    class="p-6 text-center text-gray-500 text-sm"
                  >
                    Belum ada notifikasi baru.
                  </div>


                  <!-- NOTIFIKASI -->
                  <div
                    v-for="notification in notifications"
                    :key="notification.id"
                    class="p-4 border-b border-gray-100 text-sm text-gray-700"
                  >

                    <div
                      class="flex items-start gap-3"
                    >

                      <i
                        class="fa-solid fa-circle-info text-blue-500 mt-1"
                      ></i>

                      <span>
                        {{ notification.message }}
                      </span>

                    </div>

                  </div>

                </div>

              </div>

            </transition>

          </div>


          <!-- ======================================== -->
          <!-- PROFIL TOPBAR -->
          <!-- ======================================== -->
          <div
            class="relative"
            id="profile-menu"
          >

            <div
              @click="toggleProfile"
              class="admin-profile cursor-pointer hover:bg-gray-50 p-2 rounded-xl transition flex items-center gap-3"
            >

              <!-- AVATAR -->
              <div
                class="admin-avatar bg-blue-100 text-blue-600 w-10 h-10 flex items-center justify-center rounded-full"
              >

                <i class="fa-solid fa-user"></i>

              </div>


              <!-- NAMA -->
              <div
                class="admin-info hidden sm:block"
              >

                <strong
                  class="block text-sm text-gray-800"
                >
                  {{ profileData.nama }}
                </strong>


                <span
                  class="block text-xs text-gray-500"
                >
                  Pimpinan / Kepala Balai
                </span>

              </div>


              <!-- ARROW -->
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
                class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-2 z-50"
              >

                <!-- DASHBOARD -->
                <router-link
                  to="/superuser"
                  @click="isProfileMenuOpen = false"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition"
                >

                  <i
                    class="fas fa-house mr-2 w-4 text-center"
                  ></i>

                  Dashboard

                </router-link>


                <!-- GARIS -->
                <div
                  class="border-t border-gray-100 my-1"
                ></div>


                <!-- LOGOUT -->
                <a
                  href="#"
                  @click.prevent="handleLogout"
                  class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition"
                >

                  <i
                    class="fas fa-sign-out-alt mr-2 w-4 text-center"
                  ></i>

                  Keluar

                </a>

              </div>

            </transition>

          </div>

        </div>

      </header>


      <!-- ========================================== -->
      <!-- CONTENT -->
      <!-- ========================================== -->
      <section
        class="content z-10 print:hidden"
      >

        <div
          class="dashboard-grid grid-cols-1 lg:grid-cols-3 gap-6"
        >


          <!-- ====================================== -->
          <!-- KARTU PROFIL -->
          <!-- ====================================== -->
          <div
            class="dashboard-card col-span-1 p-6 rounded-2xl border-2 border-blue-50 bg-white shadow-sm flex flex-col items-center text-center"
          >

            <!-- FOTO PROFIL -->
            <div
              class="relative mb-4"
            >

              <div
                class="w-32 h-32 rounded-full bg-gradient-to-tr from-blue-100 to-blue-50 flex items-center justify-center border-4 border-white shadow-lg overflow-hidden"
              >

                <!-- DEFAULT ICON -->
                <i
                  v-if="!profileImage"
                  class="fa-solid fa-user text-5xl text-blue-300"
                ></i>


                <!-- IMAGE -->
                <img
                  v-else
                  :src="profileImage"
                  alt="Foto Profil"
                  class="w-full h-full object-cover"
                />

              </div>

            </div>


            <!-- NAMA -->
            <h3
              class="font-bold text-xl text-gray-800"
            >
              {{ profileData.nama }}
            </h3>


            <!-- JABATAN -->
            <p
              class="text-sm text-blue-600 font-medium mb-1"
            >
              Kepala Balai / Pimpinan
            </p>


            <!-- NIP -->
            <p
              class="text-xs text-gray-500 bg-gray-100 px-3 py-1 rounded-full mt-2"
            >

              <i
                class="fas fa-id-badge mr-1"
              ></i>

              NIP: {{ profileData.nip }}

            </p>


            <hr
              class="w-full my-6 border-gray-100"
            />


            <!-- EMAIL -->
            <div
              class="w-full text-left space-y-3"
            >

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


              <!-- UNIT KERJA -->
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


          <!-- ====================================== -->
          <!-- FORM EDIT PROFIL -->
          <!-- ====================================== -->
          <div
            class="dashboard-card col-span-1 lg:col-span-2 p-6 rounded-2xl border border-gray-100 bg-white shadow-sm"
          >

            <!-- HEADER -->
            <div
              class="border-b border-gray-100 pb-4 mb-6"
            >

              <h3
                class="font-bold text-lg text-gray-800"
              >
                Edit Profil
              </h3>

              <p
                class="text-sm text-gray-500"
              >
                Perbarui informasi profil Pimpinan.
              </p>

            </div>


            <!-- FORM -->
            <form
              @submit.prevent="saveProfile"
              class="space-y-5"
            >


              <!-- NAMA -->
              <div>

                <label
                  class="block text-sm font-semibold text-gray-700 mb-1"
                >
                  Nama Lengkap
                </label>


                <input
                  v-model="profileData.nama"
                  type="text"
                  class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition bg-gray-50 focus:bg-white"
                  required
                />

              </div>


              <!-- NIP -->
              <div>

                <label
                  class="block text-sm font-semibold text-gray-700 mb-1"
                >
                  NIP
                </label>


                <input
                  v-model="profileData.nip"
                  type="text"
                  class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition bg-gray-50 focus:bg-white"
                  required
                />

              </div>


              <!-- EMAIL -->
              <div>

                <label
                  class="block text-sm font-semibold text-gray-700 mb-1"
                >
                  Alamat Email
                </label>


                <input
                  v-model="profileData.email"
                  type="email"
                  class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition bg-gray-50 focus:bg-white"
                />

              </div>


              <!-- UNIT KERJA -->
              <div>

                <label
                  class="block text-sm font-semibold text-gray-700 mb-1"
                >
                  Unit Kerja / Jabatan
                </label>


                <input
                  v-model="profileData.unitKerja"
                  type="text"
                  class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none transition bg-gray-50 focus:bg-white"
                />

              </div>


              <!-- BUTTON SIMPAN -->
              <div
                class="flex justify-end pt-4"
              >

                <button
                  type="submit"
                  :disabled="isSaving"
                  class="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white px-6 py-2.5 rounded-lg font-bold shadow-md shadow-blue-500/30 transition flex items-center gap-2"
                >

                  <!-- LOADING -->
                  <span v-if="isSaving">

                    <i
                      class="fas fa-spinner fa-spin mr-2"
                    ></i>

                    Menyimpan...

                  </span>


                  <!-- NORMAL -->
                  <span v-else>

                    <i
                      class="fas fa-save mr-2"
                    ></i>

                    Simpan Perubahan

                  </span>

                </button>

              </div>

            </form>

          </div>

        </div>

      </section>


      <!-- ========================================== -->
      <!-- FOOTER -->
      <!-- ========================================== -->
      <footer
        class="main-footer flex flex-wrap items-center justify-center gap-2 p-4 text-sm text-gray-500 mt-auto border-t bg-white relative z-10 print:hidden"
      >

        <span>
          © 2026 Balai Wilayah Sungai Sumatera III Pekanbaru
        </span>

        <span
          class="hidden sm:inline px-1"
        >
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


// ==========================================
// ROUTER & AUTH
// ==========================================

const router = useRouter()

const authStore = useAuthStore()


// ==========================================
// SIDEBAR
// ==========================================

const isSidebarOpen = ref(false)


// ==========================================
// NOTIFIKASI
// ==========================================

const isNotificationOpen = ref(false)

const notifications = ref([])


const unreadNotifications = computed(() => {

  return notifications.value.filter(
    notification => !notification.read
  ).length

})


const toggleNotification = () => {

  isNotificationOpen.value =
    !isNotificationOpen.value

  isProfileMenuOpen.value = false

}


const markAllAsRead = () => {

  notifications.value.forEach(
    notification => {

      notification.read = true

    }
  )

}


// ==========================================
// PROFILE DROPDOWN
// ==========================================

const isProfileMenuOpen = ref(false)


const toggleProfile = () => {

  isProfileMenuOpen.value =
    !isProfileMenuOpen.value

  isNotificationOpen.value = false

}


// ==========================================
// CLOSE DROPDOWN
// ==========================================

const closeDropdownsOnClickOutside = (e) => {

  if (
    !e.target.closest('#notification-menu')
  ) {

    isNotificationOpen.value = false

  }


  if (
    !e.target.closest('#profile-menu')
  ) {

    isProfileMenuOpen.value = false

  }

}


// ==========================================
// DATA PROFIL
// ==========================================

const profileImage = ref('')


const profileData = reactive({

  nama: 'Superuser',

  nip: '19700101 199503 1 001',

  email: 'pimpinan@bws-sumatera3.go.id',

  unitKerja: 'Kepala BWS Sumatera III Pekanbaru'

})


// ==========================================
// STATUS SIMPAN
// ==========================================

const isSaving = ref(false)


// ==========================================
// SIMPAN PROFIL
// ==========================================

const saveProfile = () => {

  isSaving.value = true


  setTimeout(() => {

    isSaving.value = false

    alert(
      'Profil Pimpinan berhasil diperbarui!'
    )

  }, 800)

}


// ==========================================
// CEK AUTHENTICATION
// ==========================================

onMounted(() => {

  if (
    !authStore.isAuthenticated ||
    authStore.role !== 'superuser'
  ) {

    router.push('/')

    return

  }


  document.addEventListener(
    'click',
    closeDropdownsOnClickOutside
  )

})


// ==========================================
// CLEANUP
// ==========================================

onUnmounted(() => {

  document.removeEventListener(
    'click',
    closeDropdownsOnClickOutside
  )

})


// ==========================================
// LOGOUT
// ==========================================

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