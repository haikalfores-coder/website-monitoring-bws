<template>
  <div class="overflow-x-auto rounded-xl border border-white/50 bg-white/40">
    <table class="w-full text-left border-collapse">
      <thead>
        <tr class="bg-white/60 text-slate-700">
          <th class="p-4 border-b border-white/50 text-sm font-bold">No</th>
          <th class="p-4 border-b border-white/50 text-sm font-bold">Nama Kegiatan</th>
          <th class="p-4 border-b border-white/50 text-sm font-bold">Item Kegiatan</th>
          <th class="p-4 border-b border-white/50 text-sm font-bold">Progres</th>
          <th class="p-4 border-b border-white/50 text-sm font-bold">Status Laporan</th>
          <th class="p-4 border-b border-white/50 text-sm font-bold no-print" v-if="authStore.role === 'admin'">Aksi</th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="(keg, index) in activityStore.activities" 
          :key="keg.id" 
          class="border-b border-white/30 hover:bg-white/50 transition"
        >
          <td class="p-4 text-sm">{{ index + 1 }}</td>
          <td class="p-4 text-sm font-semibold text-slate-800">
            {{ keg.nama_kegiatan }}
            <div class="text-xs font-normal text-slate-500 mt-1">
              <i class="fas fa-image mr-1"></i>{{ keg.foto_url }}
            </div>
          </td>
          <td class="p-4 text-sm">{{ keg.item_kegiatan }}</td>
          <td class="p-4 text-sm w-48">
            <div class="flex items-center gap-2">
              <div class="w-full bg-slate-200 rounded-full h-2.5 shadow-inner">
                <div 
                  class="bg-blue-500 h-2.5 rounded-full transition-all duration-500" 
                  :style="{ width: keg.progress + '%' }"
                ></div>
              </div>
              <span class="text-xs font-bold">{{ keg.progress }}%</span>
            </div>
          </td>
          <td class="p-4 text-sm">
            <span v-if="keg.laporan_ready" class="px-2 py-1 bg-emerald-100 text-emerald-700 rounded text-xs font-bold shadow-sm">
              <i class="fas fa-check-circle mr-1"></i>Siap
            </span>
            <span v-else class="px-2 py-1 bg-amber-100 text-amber-700 rounded text-xs font-bold shadow-sm">
              <i class="fas fa-clock mr-1"></i>Pending
            </span>
          </td>
          <!-- Kolom Aksi Hanya Muncul Untuk Admin -->
          <td class="p-4 text-sm no-print" v-if="authStore.role === 'admin'">
            <button 
              @click="handleDelete(keg.id)" 
              class="text-red-500 hover:text-red-700 transition transform hover:scale-110" 
              title="Hapus Kegiatan"
            >
              <i class="fas fa-trash-alt"></i>
            </button>
          </td>
        </tr>
        
        <!-- State Jika Data Kosong -->
        <tr v-if="activityStore.activities.length === 0">
          <td :colspan="authStore.role === 'admin' ? 6 : 5" class="p-8 text-center text-slate-500">
            Belum ada data kegiatan yang diinput.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useActivityStore } from '@/stores/activities'
import { useAuthStore } from '@/stores/auth'

const activityStore = useActivityStore()
const authStore = useAuthStore()

const handleDelete = async (id) => {
  if (confirm('Yakin ingin menghapus data kegiatan ini?')) {
    await activityStore.deleteActivity(id)
  }
}
</script>