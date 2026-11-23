import { defineStore } from 'pinia'

const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/+$/, '')

export const useAuthStore = defineStore('auth', {
  // State awal dibaca dari localStorage agar sesi tetap ada saat halaman di-refresh
  state: () => ({
    username: localStorage.getItem('username') || null,
    role: localStorage.getItem('role') || null,
    token: localStorage.getItem('token') || null, // BARU: token JWT
    isAuthenticated: localStorage.getItem('isAuthenticated') === 'true'
  }),

  actions: {
    async login(username, password) {
      try {
        const response = await fetch(`${API_URL}/api/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password })
        })

        if (!response.ok) return false

        const data = await response.json()

        // Simpan ke state Pinia
        this.username = data.username
        this.role = data.role // 'admin' atau 'superuser'
        this.token = data.access_token // BARU
        this.isAuthenticated = true

        // Simpan ke localStorage
        localStorage.setItem('username', data.username)
        localStorage.setItem('role', data.role)
        localStorage.setItem('token', data.access_token) // BARU
        localStorage.setItem('isAuthenticated', 'true')

        return true
      } catch (error) {
        console.error('Terjadi kesalahan saat login:', error)
        return false
      }
    },

    logout() {
      this.username = null
      this.role = null
      this.token = null // BARU
      this.isAuthenticated = false

      localStorage.removeItem('username')
      localStorage.removeItem('role')
      localStorage.removeItem('token') // BARU
      localStorage.removeItem('isAuthenticated')
    }
  }
})