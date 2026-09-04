<template>
  <!-- Komponen khusus router-view untuk merender halaman secara dinamis berdasarkan URL -->
  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<script setup>
// File ini berfungsi sebagai kerangka akar (root) aplikasi Vue.
// Halaman seperti LoginView atau AdminDashboard akan di-inject otomatis ke dalam <router-view>.
</script>

<style>
/* CSS khusus untuk animasi transisi perpindahan antar halaman (opsional) */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>