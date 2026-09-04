import { defineStore } from 'pinia'

// Mengambil URL Backend dari environment (VITE_API_URL) atau gunakan localhost sebagai fallback
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const useActivityStore = defineStore('activities', {
  state: () => ({
    activities: [] // Mulai dengan array kosong, data asli akan diambil dari Backend (Database)
  }),
  
  actions: {
    async fetchActivities() {
      try {
        const response = await fetch(`${API_URL}/api/kegiatan`)
        if (response.ok) {
          this.activities = await response.json()
        } else {
          console.error("Gagal mengambil data dari server")
        }
      } catch (error) {
        console.error('Koneksi ke server backend gagal:', error)
      }
    },

    async addActivity(activityData) {
      try {
        const response = await fetch(`${API_URL}/api/kegiatan`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(activityData)
        })
        
        if (response.ok) {
          const newActivity = await response.json()
          this.activities.unshift(newActivity)
        } else {
          alert('Gagal menyimpan data kegiatan ke database.')
        }
      } catch (error) {
        console.error('Gagal menambah kegiatan:', error)
        alert('Gagal terhubung ke server backend.')
      }
    },

    async updateActivity(updatedData) {
      try {
        const response = await fetch(`${API_URL}/api/kegiatan/${updatedData.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(updatedData)
        })
        
        if (response.ok) {
          const index = this.activities.findIndex(a => a.id === updatedData.id)
          if (index !== -1) this.activities[index] = { ...this.activities[index], ...updatedData }
        } else {
          alert('Gagal memperbarui data di database.')
        }
      } catch (error) {
        console.error('Gagal memperbarui kegiatan:', error)
        alert('Gagal terhubung ke server backend.')
      }
    },

    async deleteActivity(id) {
      try {
        const response = await fetch(`${API_URL}/api/kegiatan/${id}`, { method: 'DELETE' })
        
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
        const response = await fetch(`${API_URL}/api/kegiatan/prepare-report`, { method: 'PUT' })
        
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