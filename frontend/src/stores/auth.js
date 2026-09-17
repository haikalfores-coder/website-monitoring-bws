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
        // Mencegah error 308/405 dengan menghapus garis miring berlebih di akhir URL dari Vercel
        const cleanUrl = import.meta.env.VITE_API_URL.replace(/\/+$/, '');
        
        // Terhubung langsung ke backend FastAPI menggunakan cleanUrl
        const response = await fetch(`${cleanUrl}/api/login`, {
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

        // Jika respons server gagal (misal salah password), kembalikan false
        return false
      } catch (error) {
        console.error('Terjadi kesalahan saat login:', error)
        // Jika koneksi server putus, langsung kembalikan false (tidak ada lagi auto-login)
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