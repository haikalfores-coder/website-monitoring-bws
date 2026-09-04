<template>
  <div class="split-container">
    <!-- PANEL KIRI -->
    <div class="left-panel">
      <div class="left-content">
        <div class="brand-top">
          <!-- Menggunakan @/assets/ untuk memanggil gambar dari folder src -->
          <img src="@/assets/images/logo-pu.png" alt="Logo PU" class="logo-img">
          <div class="brand-text">
            <strong>BWS SUMATERA III<br>PEKANBARU</strong><br>
            <span>Kementerian Pekerjaan Umum</span>
          </div>
        </div>

        <div class="main-heading">
          <h4>SELAMAT DATANG DI</h4>
          <h1>Dashboard Monitoring<br>Data Kegiatan</h1>
          <hr class="yellow-line">
          <p>
            Sistem informasi untuk monitoring dan pengelolaan data kegiatan Balai Wilayah Sungai Sumatera III Pekanbaru secara efektif, akurat, dan real-time.
          </p>
        </div>

        <div class="features">
          <div class="feature-item">
            <div class="icon-circle"><i class="fa-solid fa-chart-column"></i></div>
            <h5>Monitoring</h5>
            <p>Pantau kegiatan secara real-time</p>
          </div>
          <div class="feature-item">
            <div class="icon-circle"><i class="fa-solid fa-file-lines"></i></div>
            <h5>Laporan</h5>
            <p>Data dan statistik kegiatan</p>
          </div>
          <div class="feature-item">
            <div class="icon-circle"><i class="fa-solid fa-water"></i></div>
            <h5>Wilayah Sungai</h5>
            <p>Informasi wilayah sungai</p>
          </div>
        </div>
      </div>

      <div class="left-footer">
        <div class="contact-info">
          <span><i class="fa-solid fa-location-dot"></i> Jl. Pepaya No.1, Labuh Baru Timur</span>
          <span><i class="fa-solid fa-phone"></i> (0761) 21383</span>
          <span><i class="fa-solid fa-envelope"></i> bws_sumatera3@pu.go.id</span>
        </div>
        <div class="copyright">
          © 2026 BWS Sumatera III Pekanbaru
        </div>
      </div>
    </div>

    <!-- PANEL KANAN -->
    <div class="right-panel">
      <div class="login-card">
        <div class="card-header">
          <img src="@/assets/images/logo-pu.png" alt="Logo PU" class="logo-img small">
          <div class="brand-text dark">
            <strong>BWS SUMATERA III<br>PEKANBARU</strong>
          </div>
        </div>

        <hr class="divider">

        <div class="welcome-text">
          <div class="lock-circle"><i class="fa-solid fa-lock"></i></div>
          <h2>Selamat Datang</h2>
          <p>Silakan masuk menggunakan ID dan password yang telah diberikan administrator.</p>
        </div>

        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="userid">ID Pengguna</label>
            <div class="input-wrapper">
              <i class="fa-regular fa-user input-icon"></i>
              <input 
                v-model="username" 
                type="text" 
                id="userid" 
                placeholder="Masukkan ID Pengguna" 
                required
              >
            </div>
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <div class="input-wrapper">
              <i class="fa-solid fa-lock input-icon"></i>
              <input 
                v-model="password" 
                :type="showPassword ? 'text' : 'password'" 
                id="password" 
                placeholder="Masukkan Password" 
                required
              >
              <i 
                :class="['toggle-password', showPassword ? 'fa-regular fa-eye-slash' : 'fa-regular fa-eye']" 
                @click="showPassword = !showPassword"
              ></i>
            </div>
          </div>

          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>

          <button type="submit" class="btn-login" :disabled="isLoading">
            <span v-if="isLoading"><i class="fas fa-spinner fa-spin mr-2"></i>Memproses...</span>
            <span v-else>MASUK KE SISTEM</span>
          </button>
        </form>

        <div class="security-notice">
          <i class="fa-solid fa-shield-halved"></i><br>
          Hanya dapat diakses oleh pegawai dan pengguna yang berwenang.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoading = ref(false)
const showPassword = ref(false)

const handleLogin = async () => {
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    const success = await authStore.login(username.value, password.value)
    
    if (success) {
      if (authStore.role === 'admin') {
        router.push('/admin')
      } else if (authStore.role === 'superuser') {
        router.push('/superuser')
      }
    } else {
      errorMessage.value = 'ID Pengguna atau Password tidak sesuai.'
    }
  } catch (error) {
    errorMessage.value = 'Terjadi kesalahan pada server.'
    console.error(error)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.split-container {
  display: flex;
  width: 100%;
  height: 100vh;
  font-family: 'Inter', sans-serif;
  background: #f4f6f9;
}

/* =========================
   PANEL KIRI
========================= */
.left-panel {
  width: 60%;
  display: flex;
  flex-direction: column;
  /* Menggunakan @ untuk path CSS Vite */
  background: linear-gradient(rgba(0,51,102,.72), rgba(0,51,102,.45)), url('@/assets/images/background.jpg');
  background-size: cover;
  background-position: center;
  color: #fff;
}

.left-content {
  flex: 1;
  padding: 40px 50px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.brand-top {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 50px;
}

.logo-img {
  width: 60px;
  height: 60px;
  object-fit: contain;
}

.logo-img.small {
  width: 45px;
  height: 45px;
}

.brand-text {
  font-size: 14px;
  line-height: 1.4;
}

.brand-text span {
  font-size: 12px;
  opacity: .9;
}

.main-heading {
  max-width: 600px;
}

.main-heading h4 {
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 3px;
  margin-bottom: 12px;
}

.main-heading h1 {
  font-size: 52px;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 20px;
}

.yellow-line {
  width: 70px;
  height: 4px;
  border: none;
  border-radius: 50px;
  background: #FFD100;
  margin-bottom: 20px;
}

.main-heading p {
  max-width: 500px;
  font-size: 16px;
  line-height: 1.8;
}

.features {
  display: flex;
  gap: 25px;
  margin-top: 40px;
}

.feature-item {
  max-width: 180px;
}

.icon-circle {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: rgba(255,255,255,.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-bottom: 12px;
}

.feature-item h5 {
  font-size: 14px;
  margin-bottom: 6px;
}

.feature-item p {
  font-size: 13px;
  line-height: 1.5;
}

.left-footer {
  width: 100%;
  background: #003366;
  padding: 16px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.contact-info {
  display: flex;
  gap: 25px;
  font-size: 12px;
}

.contact-info i {
  color: #FFD100;
}

.copyright {
  font-size: 12px;
}

/* =========================
   PANEL KANAN
========================= */
.right-panel {
  width: 40%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #F8FAFC;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 390px;
  background: #fff;
  padding: 28px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,.08);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.brand-text.dark {
  color: #003366;
}

.divider {
  border: none;
  border-top: 1px solid #E2E8F0;
  margin: 18px 0;
}

.welcome-text {
  text-align: center;
  margin-bottom: 18px;
}

.lock-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #EEF3F9;
  color: #003366;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.welcome-text h2 {
  font-size: 26px;
  color: #003366;
  margin-bottom: 8px;
}

.welcome-text p {
  color: #64748B;
  font-size: 13px;
  line-height: 1.5;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #003366;
  font-size: 14px;
  font-weight: 600;
}

.input-wrapper {
  position: relative;
}

.input-wrapper input {
  width: 100%;
  height: 46px;
  border: 1px solid #D7DDE5;
  border-radius: 10px;
  padding: 0 42px;
  font-size: 14px;
}

.input-wrapper input:focus {
  outline: none;
  border-color: #005BAC;
}

.input-icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #94A3B8;
}

.toggle-password {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: #94A3B8;
  cursor: pointer;
}

.error-message {
  color: #DC2626;
  font-size: 13px;
  text-align: center;
  margin-bottom: 12px;
  background: #FEF2F2;
  padding: 8px;
  border-radius: 8px;
}

.btn-login {
  width: 100%;
  height: 46px;
  border: none;
  border-radius: 10px;
  background: #005BAC;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: .3s;
}

.btn-login:hover {
  background: #004B95;
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.security-notice {
  margin-top: 16px;
  text-align: center;
  color: #64748B;
  font-size: 11px;
  line-height: 1.5;
}

/* =========================
   RESPONSIF
========================= */
@media (max-width: 1100px) {
  .main-heading h1 { font-size: 42px; }
  .features { gap: 15px; }
  .login-card { max-width: 360px; }
}

@media (max-width: 768px) {
  .split-container {
    flex-direction: column;
    height: auto;
  }
  .left-panel, .right-panel { width: 100%; }
  .left-panel { min-height: 55vh; }
  .left-content { padding: 30px 25px; }
  .brand-top { margin-bottom: 25px; }
  .main-heading h1 { font-size: 34px; }
  .main-heading p { font-size: 14px; }
  .features {
    flex-direction: column;
    gap: 15px;
    margin-top: 25px;
  }
  .left-footer { display: none; }
  .right-panel { padding: 20px; }
  .login-card {
    max-width: 100%;
    padding: 24px;
  }
}
</style>