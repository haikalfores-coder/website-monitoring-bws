import { defineStore } from 'pinia'
import { apiFetch } from '@/utils/api' // sesuaikan path jika berbeda

// Catatan: apiFetch sudah menambahkan VITE_API_URL di depan path,
// jadi di sini cukup menulis '/api/kegiatan'.

export const useActivityStore = defineStore('activities', {
  state: () => ({
    activities: [] // Data asli diambil dari Backend (Database)
  }),

  actions: {
    async fetchActivities() {
      try {
        const response = await apiFetch('/api/kegiatan')
        if (response.ok) {
          this.activities = await response.json()
        } else {
          console.error('Gagal mengambil data dari server')
        }
      } catch (error) {
        console.error('Koneksi ke server backend gagal:', error)
      }
    },

    async addActivity(activityData) {
      // Cek apakah data yang dikirim adalah FormData (ada file) atau object biasa
      const isFormData = activityData instanceof FormData

      const options = {
        method: 'POST',
        body: isFormData ? activityData : JSON.stringify(activityData)
      }

      // Jangan atur Content-Type jika FormData (peramban mengaturnya otomatis)
      if (!isFormData) {
        options.headers = { 'Content-Type': 'application/json' }
      }

      const response = await apiFetch('/api/kegiatan', options)

      if (response.ok) {
        const newActivity = await response.json()
        this.activities.unshift(newActivity)
      } else {
        // Tangkap pesan error dari server dan lempar ke komponen Vue
        const errorData = await response.json().catch(() => null)
        throw { response: { data: errorData } }
      }
    },

    async updateActivity(updatedData) {
      const isFormData = updatedData instanceof FormData

      // Ambil ID dari FormData dengan .get('id'), atau dari object biasa dengan .id
      const activityId = isFormData ? updatedData.get('id') : updatedData.id

      const options = {
        method: 'PUT',
        body: isFormData ? updatedData : JSON.stringify(updatedData)
      }

      if (!isFormData) {
        options.headers = { 'Content-Type': 'application/json' }
      }

      const response = await apiFetch(`/api/kegiatan/${activityId}`, options)

      if (response.ok) {
        // Ambil hasil dari database agar data foto terbaru tampil di tabel
        const updatedResult = await response.json()
        const index = this.activities.findIndex(a => a.id == activityId)
        if (index !== -1) {
          this.activities[index] = { ...this.activities[index], ...updatedResult }
        }
      } else {
        const errorData = await response.json().catch(() => null)
        throw { response: { data: errorData } }
      }
    },

    async deleteActivity(id) {
      try {
        const response = await apiFetch(`/api/kegiatan/${id}`, { method: 'DELETE' })

        if (response.ok) {
          this.activities = this.activities.filter(a => a.id !== id)
        } else {
          alert('Gagal menghapus data dari database.')
        }
      } catch (error) {
        console.error('Gagal menghapus kegiatan:', error)
        alert('Gagal terhubung ke server backend.')
      }
    },

    async prepareReport() {
      try {
        const response = await apiFetch('/api/kegiatan/prepare-report', { method: 'PUT' })

        if (response.ok) {
          this.activities.forEach(a => { a.laporan_ready = true })
        } else {
          alert('Gagal menyiapkan laporan di server.')
        }
      } catch (error) {
        console.error('Gagal menyiapkan laporan:', error)
        alert('Gagal terhubung ke server backend.')
      }
    }
  }
})
