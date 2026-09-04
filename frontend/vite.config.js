import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      // Memungkinkan Anda menggunakan '@' sebagai pengganti path relatif yang panjang (misal: '@/components/Navbar.vue')
      '@': path.resolve(import.meta.dirname, './src'),
    },
  },
  server: {
    port: 5173, // Port default Vite
    proxy: {
      // Mengarahkan otomatis semua request frontend berawalan '/api' ke backend FastAPI
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})