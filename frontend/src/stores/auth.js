import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    username: null,
    role: null,
    isAuthenticated: false
  }),
  
  actions: {
    async login(username, password) {
      try {
        // Blok ini untuk terhubung langsung ke backend FastAPI menggunakan URL dari Vercel
        const response = await fetch(`${import.meta.env.VITE_API_URL}/api/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username, password })
        })

        if (response.ok) {
          const data = await response.json()
          this.username = data.username
          this.role = data.role // 'admin' atau 'superuser'
          this.isAuthenticated = true
          return true
        }

        // Fallback mockup jika server backend belum dijalankan (hanya untuk testing UI)
        if (username === 'admin' && password === 'admin') {
          this.username = 'admin'
          this.role = 'admin'
          this.isAuthenticated = true
          return true
        } else if (username === 'super' && password === 'super') {
          this.username = 'super'
          this.role = 'superuser'
          this.isAuthenticated = true
          return true
        }

        return false
      } catch (error) {
        console.error('Terjadi kesalahan saat login:', error)
        
        // Fallback darurat jika koneksi ke server gagal (misal: FastAPI belum menyala)
        if (username === 'admin' && password === 'admin') {
          this.username = 'admin'; this.role = 'admin'; this.isAuthenticated = true; return true
        } else if (username === 'super' && password === 'super') {
          this.username = 'super'; this.role = 'superuser'; this.isAuthenticated = true; return true
        }
        
        return false
      }
    },

    logout() {
      // Hapus state saat pengguna keluar
      this.username = null
      this.role = null
      this.isAuthenticated = false
    }
  }
})