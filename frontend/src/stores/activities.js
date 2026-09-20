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
      // 1. Cek apakah data yang dikirim adalah FormData (ada file) atau Object biasa
      const isFormData = activityData instanceof FormData;
      
      const options = {
        method: 'POST',
        // Jika FormData, langsung jadikan body. Jika object biasa, jadikan JSON String
        body: isFormData ? activityData : JSON.stringify(activityData)
      };

      // 2. JANGAN atur Content-Type jika FormData (Browser akan mengaturnya otomatis)
      if (!isFormData) {
        options.headers = { 'Content-Type': 'application/json' };
      }

      const response = await fetch(`${API_URL}/api/kegiatan`, options);
      
      if (response.ok) {
        const newActivity = await response.json();
        this.activities.unshift(newActivity);
      } else {
        // Tangkap pesan error dari server dan lempar ke Vue Component
        const errorData = await response.json().catch(() => null);
        throw { response: { data: errorData } }; 
      }
    },

    async updateActivity(updatedData) {
      // 1. Cek tipe data
      const isFormData = updatedData instanceof FormData;
      
      // 2. Ambil ID dari FormData menggunakan .get('id'), atau dari object biasa menggunakan .id
      const activityId = isFormData ? updatedData.get('id') : updatedData.id;

      const options = {
        method: 'PUT',
        body: isFormData ? updatedData : JSON.stringify(updatedData)
      };

      if (!isFormData) {
        options.headers = { 'Content-Type': 'application/json' };
      }

      const response = await fetch(`${API_URL}/api/kegiatan/${activityId}`, options);
      
      if (response.ok) {
        // Ambil hasil response dari database agar data foto_url terupdate di tabel
        const updatedResult = await response.json(); 
        const index = this.activities.findIndex(a => a.id == activityId);
        if (index !== -1) {
          this.activities[index] = { ...this.activities[index], ...updatedResult };
        }
      } else {
        // Tangkap pesan error dari server dan lempar ke Vue Component
        const errorData = await response.json().catch(() => null);
        throw { response: { data: errorData } };
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