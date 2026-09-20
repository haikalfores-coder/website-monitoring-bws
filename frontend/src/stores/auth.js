import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  // Membaca state awal dari localStorage agar sesi tetap terjaga saat halaman di-refresh
  state: () => ({
    username: localStorage.getItem('username') || null,
    role: localStorage.getItem('role') || null,
    isAuthenticated: localStorage.getItem('isAuthenticated') === 'true'
  }),
  
  actions: {
    async login(username, password) {
      try {
        // Mencegah error 308/405 dengan menghapus garis miring berlebih di akhir URL dari Vercel
        const cleanUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '');
        
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
          
          // Simpan ke state Pinia
          this.username = data.username
          this.role = data.role // 'admin' atau 'superuser'
          this.isAuthenticated = true

          // Simpan ke localStorage agar tidak hilang saat di-refresh
          localStorage.setItem('username', data.username)
          localStorage.setItem('role', data.role)
          localStorage.setItem('isAuthenticated', 'true')

          return true
        }

        // Jika respons server gagal (misal salah password), kembalikan false
        return false
      } catch (error) {
        console.error('Terjadi kesalahan saat login:', error)
        // Jika koneksi server putus, langsung kembalikan false
        return false
      }
    },

    logout() {
      // Hapus state saat pengguna keluar
      this.username = null
      this.role = null
      this.isAuthenticated = false

      // Hapus data dari localStorage
      localStorage.removeItem('username')
      localStorage.removeItem('role')
      localStorage.removeItem('isAuthenticated')
    }
  }
})