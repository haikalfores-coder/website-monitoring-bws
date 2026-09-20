<template>
  <div class="admin-wrapper relative bg-gray-50/50 min-h-screen flex overflow-hidden">
    
    <!-- OVERLAY UNTUK MOBILE (Klik di luar sidebar untuk menutup) -->
    <div v-if="isSidebarOpen" @click="isSidebarOpen = false" class="fixed inset-0 bg-black/50 z-40 lg:hidden backdrop-blur-sm transition-opacity"></div>

    <!-- SIDEBAR -->
    <!-- Ditambahkan class Tailwind fixed, z-50, transition-transform agar buka-tutup lancar di mobile -->
    <aside class="sidebar print:hidden fixed inset-y-0 left-0 z-50 w-64 h-screen bg-white shadow-lg transform transition-transform duration-300 lg:relative lg:translate-x-0" :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'">
      <div class="sidebar-brand">
        <img src="/logo-pu.png" alt="Logo PU" class="sidebar-logo">
        <div class="sidebar-brand-text">
          <strong>BWS SUMATERA III</strong>
          <span>PEKANBARU</span>
        </div>
      </div>

      <nav class="sidebar-menu">
        <div class="menu-title">MENU UTAMA</div>
        <a href="#" @click.prevent="activeMenu = 'dashboard'; scrollToTop(); isSidebarOpen = false" class="menu-item" :class="{ 'active': activeMenu === 'dashboard' }">
          <i class="fa-solid fa-house"></i>
          <span>Dashboard</span>
        </a>

        <div class="menu-title">DATA & LAPORAN</div>
        <a href="#tabel-data" @click="activeMenu = 'data'; isSidebarOpen = false" class="menu-item" :class="{ 'active': activeMenu === 'data' }">
          <i class="fa-solid fa-clipboard-list"></i>
          <span>Data Kegiatan</span>
        </a>

        <!-- Tombol Cetak di Sidebar -->
        <a href="#" @click.prevent="printLaporan" class="menu-item font-bold transition" :class="selectedToPrint.length > 0 ? 'text-green-600 bg-green-50 hover:bg-green-100' : 'text-gray-400 bg-gray-50 cursor-not-allowed'">
          <i class="fa-solid fa-file-pdf"></i>
          <span>Cetak PDF Laporan ({{ selectedToPrint.length }})</span>
        </a>

        <div class="menu-title">SISTEM</div>
        <router-link to="/profil" class="menu-item" @click="isSidebarOpen = false">
          <i class="fa-solid fa-user"></i>
          <span>Profil</span>
        </router-link>
      </nav>

      <div class="sidebar-bottom">
        <a href="#" @click.prevent="handleLogout" class="menu-item logout">
          <i class="fa-solid fa-right-from-bracket"></i>
          <span>Logout</span>
        </a>
      </div>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="main-content flex-1 h-screen overflow-y-auto w-full">
      <header class="topbar relative z-30 print:hidden bg-white shadow-sm flex justify-between items-center px-4 py-3">
        <div class="topbar-left flex items-center gap-4">
          <!-- Tombol Hamburger Toggle -->
          <button class="sidebar-toggle text-gray-600 hover:text-blue-600 focus:outline-none lg:hidden text-2xl" @click="isSidebarOpen = !isSidebarOpen">
            <i class="fa-solid fa-bars"></i>
          </button>
          <div class="page-title hidden sm:block">
            <h1 class="text-xl font-bold text-gray-800">Dashboard Administrator</h1>
            <p class="text-xs text-gray-500">Area Kerja Pribadi: @{{ authStore.username }}</p>
          </div>
        </div>

        <div class="topbar-right flex items-center gap-4 relative">
          <!-- PROFIL -->
          <div class="relative" id="profile-menu">
            <div @click="toggleProfile" class="admin-profile cursor-pointer hover:bg-gray-50 p-2 rounded-xl transition flex items-center gap-3">
              <div class="admin-avatar bg-blue-100 text-blue-600 w-10 h-10 flex items-center justify-center rounded-full">
                <i class="fa-solid fa-user"></i>
              </div>
              <div class="admin-info hidden sm:block">
                <strong class="block text-sm text-gray-800">@{{ authStore.username }}</strong>
                <span class="block text-xs text-gray-500">Administrator</span>
              </div>
              <i class="fa-solid fa-chevron-down profile-arrow text-gray-400 text-xs transition-transform duration-300" :class="{'rotate-180': isProfileMenuOpen}"></i>
            </div>

            <transition name="fade-slide">
              <div v-if="isProfileMenuOpen" class="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-2 z-50">
                <router-link to="/profil" class="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition">
                  <i class="fas fa-user-circle mr-2 w-4 text-center"></i> Profil Saya
                </router-link>
                <div class="border-t border-gray-100 my-1"></div>
                <a href="#" @click.prevent="handleLogout" class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition"><i class="fas fa-sign-out-alt mr-2 w-4 text-center"></i> Keluar</a>
              </div>
            </transition>
          </div>
        </div>
      </header>

      <section class="content z-10 print:hidden p-4 md:p-6">
        
        <!-- VISUALISASI DATA (GRAFIK & STATISTIK) -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <!-- Statistik Angka -->
          <div class="lg:col-span-1 flex flex-col gap-4">
            <div class="bg-blue-600 text-white p-5 rounded-2xl shadow-sm flex items-center justify-between">
              <div>
                <span class="block text-sm text-blue-100 font-medium mb-1">Kegiatan Saya</span>
                <strong class="text-3xl">{{ totalKegiatan }}</strong>
              </div>
              <i class="fa-solid fa-layer-group text-4xl opacity-30"></i>
            </div>
            
            <div class="grid grid-cols-2 gap-4 flex-1">
              <div class="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-center">
                <span class="text-xs text-gray-500 font-semibold mb-1 uppercase">Selesai</span>
                <div class="flex items-end gap-2"><strong class="text-2xl text-green-600">{{ countSelesai }}</strong></div>
              </div>
              <div class="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-center">
                <span class="text-xs text-gray-500 font-semibold mb-1 uppercase">Berjalan</span>
                <div class="flex items-end gap-2"><strong class="text-2xl text-blue-600">{{ countBerjalan }}</strong></div>
              </div>
              <div class="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-center">
                <span class="text-xs text-gray-500 font-semibold mb-1 uppercase">Menunggu</span>
                <div class="flex items-end gap-2"><strong class="text-2xl text-yellow-600">{{ countMenunggu }}</strong></div>
              </div>
              <div class="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex flex-col justify-center">
                <span class="text-xs text-gray-500 font-semibold mb-1 uppercase">Ditunda</span>
                <div class="flex items-end gap-2"><strong class="text-2xl text-red-600">{{ countDitunda }}</strong></div>
              </div>
            </div>
          </div>

          <!-- Grafik Cincin (Distribusi Status) -->
          <div class="lg:col-span-1 bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col">
            <h3 class="font-bold text-gray-800 mb-6 text-sm">Distribusi Status Data Milik Saya</h3>
            <div class="flex-1 flex flex-col items-center justify-center gap-6">
              <div class="w-32 h-32 rounded-full relative shadow-sm flex items-center justify-center transition-all duration-500"
                   :style="{ background: pieChartStyle }">
                <div class="w-20 h-20 bg-white rounded-full flex items-center justify-center shadow-inner">
                  <i class="fa-solid fa-chart-pie text-gray-300 text-2xl"></i>
                </div>
              </div>
              <div class="w-full grid grid-cols-2 gap-y-2 text-xs font-medium text-gray-600">
                <div class="flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-green-500 block"></span>Selesai ({{ countSelesai }})</div>
                <div class="flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-blue-500 block"></span>Berjalan ({{ countBerjalan }})</div>
                <div class="flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-yellow-500 block"></span>Menunggu ({{ countMenunggu }})</div>
                <div class="flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-red-500 block"></span>Ditunda ({{ countDitunda }})</div>
              </div>
            </div>
          </div>

          <!-- Grafik Batang (Progres Tertinggi) -->
          <div class="lg:col-span-1 bg-white p-5 rounded-2xl shadow-sm border border-gray-100 flex flex-col">
            <h3 class="font-bold text-gray-800 mb-4 text-sm">Progres Pekerjaan Aktif</h3>
            <div class="flex-1 overflow-y-auto pr-2 custom-scrollbar space-y-4">
              <div v-for="keg in activeActivitiesProgress" :key="keg.id">
                <div class="flex justify-between text-xs font-semibold text-gray-700 mb-1">
                  <span class="truncate w-3/4">{{ keg.nama_kegiatan }}</span>
                  <span class="text-blue-600">{{ keg.progress }}%</span>
                </div>
                <div class="w-full bg-gray-100 rounded-full h-2">
                  <div class="bg-blue-500 h-2 rounded-full transition-all duration-1000" :style="{ width: keg.progress + '%' }"></div>
                </div>
              </div>
              <div v-if="activeActivitiesProgress.length === 0" class="h-full flex flex-col items-center justify-center text-gray-400 text-sm">
                <i class="fa-solid fa-check-double text-2xl mb-2"></i>
                <p>Tidak ada kegiatan berjalan.</p>
              </div>
            </div>
          </div>
        </div>

        <!-- FORM INPUT KEGIATAN BARU -->
        <div v-if="showForm" class="bg-white rounded-2xl shadow-sm border border-gray-100 mb-8 overflow-hidden">
          <div class="bg-blue-50 border-b border-blue-100 p-4 flex justify-between items-center">
            <h3 class="font-bold text-blue-800"><i class="fas fa-plus-circle mr-2"></i>Tambah Data Baru</h3>
            <button @click="showForm = false" class="text-gray-500 hover:text-red-500 transition text-xl leading-none">&times;</button>
          </div>
          
          <form @submit.prevent="submitActivity" class="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="space-y-4 md:col-span-1">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Nama Kegiatan</label>
                <input v-model="formData.nama_kegiatan" type="text" placeholder="Contoh: Normalisasi Sungai / Perbaikan Jalan" class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none" required>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-1">Lokasi Detail (Bebas)</label>
                <input v-model="formData.item_kegiatan" type="text" placeholder="Contoh: Jl. Sudirman atau Sungai Kampar Kanan" class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none" required>
              </div>
              
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-1">Tanggal Mulai</label>
                  <input v-model="formData.tanggal_mulai" type="date" class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none">
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-1">Tanggal Selesai</label>
                  <input v-model="formData.tanggal_selesai" type="date" class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none">
                </div>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-1">Status Kegiatan</label>
                  <select v-model="formData.status" class="w-full border border-gray-300 p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none" required>
                    <option value="Menunggu">Menunggu</option>
                    <option value="Berjalan">Berjalan</option>
                    <option value="Ditunda">Ditunda</option>
                    <option value="Selesai">Selesai</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-semibold text-gray-700 mb-1">Progres (%)</label>
                  <div class="flex items-center gap-4 bg-gray-50 border border-gray-300 p-2.5 rounded-lg">
                    <input v-model="formData.progress" type="range" min="0" max="100" class="w-full accent-blue-600" @input="syncStatusWithProgress(formData)">
                    <span class="font-bold text-blue-700 w-12 text-right">{{ formData.progress }}%</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="flex flex-col md:col-span-1">
              <label class="block text-sm font-semibold text-gray-700 mb-1">Dokumentasi Foto</label>
              <div v-if="!imagePreview" class="flex-1 flex items-center justify-center w-full">
                <label for="dropzone-file" class="flex flex-col items-center justify-center w-full h-full min-h-[160px] border-2 border-dashed border-gray-300 rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 transition">
                  <div class="flex flex-col items-center justify-center pt-5 pb-6">
                    <i class="fa-solid fa-cloud-arrow-up text-3xl text-blue-500 mb-3"></i>
                    <p class="mb-1 text-sm text-gray-600"><span class="font-semibold">Klik untuk unggah foto</span></p>
                  </div>
                  <input id="dropzone-file" ref="fileInput" type="file" accept="image/*" class="hidden" @change="handleFileUpload" />
                </label>
              </div>
              <div v-else class="flex-1 relative w-full min-h-[160px] border rounded-lg bg-gray-100 p-2 flex justify-center items-center">
                <img :src="imagePreview" class="max-h-48 object-contain rounded shadow-sm">
                <button @click.prevent="removeImage" class="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 hover:bg-red-600 shadow-lg"><i class="fas fa-trash-alt text-xs"></i></button>
              </div>
            </div>

            <div class="md:col-span-2 flex justify-end mt-2 pt-4 border-t border-gray-100">
              <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-lg font-bold shadow-md transition"><i class="fas fa-save mr-2"></i>Simpan Kegiatan</button>
            </div>
          </form>
        </div>

        <!-- TABEL DATA, TABS & PENCARIAN -->
        <div id="tabel-data" class="bg-white rounded-2xl shadow-sm border border-gray-100 relative z-10 overflow-hidden">
          
          <div class="p-5 flex flex-col md:flex-row justify-between items-start md:items-end gap-4 border-b border-gray-100 bg-gray-50/50">
            <!-- TAB KATEGORI -->
            <div>
              <h3 class="mb-3 font-bold text-gray-800">Manajemen Data Pribadi</h3>
              <div class="flex gap-2 p-1 bg-gray-200/50 rounded-lg inline-flex">
                <button @click="activeTab = 'aktif'" class="px-5 py-1.5 text-sm rounded-md transition font-semibold" :class="activeTab === 'aktif' ? 'bg-white text-blue-700 shadow-sm' : 'text-gray-500 hover:text-gray-700'">
                  Sedang Dimonitoring
                </button>
                <button @click="activeTab = 'selesai'" class="px-5 py-1.5 text-sm rounded-md transition font-semibold" :class="activeTab === 'selesai' ? 'bg-white text-green-700 shadow-sm' : 'text-gray-500 hover:text-gray-700'">
                  Telah Selesai
                </button>
              </div>
            </div>
            
            <div class="flex flex-col sm:flex-row gap-3 w-full md:w-auto">
              <!-- FITUR PENCARIAN -->
              <div class="relative w-full sm:w-64">
                <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
                <input v-model="searchQuery" type="text" placeholder="Cari kegiatan/lokasi..." class="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none text-sm bg-white">
              </div>
              
              <button @click="openForm" v-if="!showForm" class="bg-blue-600 text-white px-4 py-2 rounded-lg whitespace-nowrap shadow-sm hover:bg-blue-700 transition font-medium">
                <i class="fa-solid fa-plus mr-1"></i> Tambah Data
              </button>
            </div>
          </div>

          <!-- KONTROL CETAK -->
          <div v-if="activeTab === 'selesai'" class="px-5 py-3 bg-green-50/50 border-b border-green-100 flex justify-between items-center">
            <span class="text-sm text-green-800 font-medium">
              <i class="fas fa-info-circle mr-1"></i> Pilih kegiatan yang ingin diserahkan / dicetak.
            </span>
            <button @click="printLaporan" :disabled="selectedToPrint.length === 0" class="px-4 py-1.5 text-sm font-bold rounded-lg transition shadow-sm" :class="selectedToPrint.length > 0 ? 'bg-green-600 text-white hover:bg-green-700' : 'bg-gray-200 text-gray-400 cursor-not-allowed'">
              Cetak Terpilih ({{ selectedToPrint.length }})
            </button>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse min-w-[600px]">
              <thead>
                <tr class="border-b bg-gray-50">
                  <th v-if="activeTab === 'selesai'" class="p-4 w-12 text-center">
                     <input type="checkbox" :checked="isAllSelesaiSelected" @change="toggleSelectAllSelesai" class="w-4 h-4 text-green-600 rounded cursor-pointer border-gray-300">
                  </th>
                  <th v-else class="p-4 w-12 text-center text-sm font-semibold text-gray-600">No</th>
                  
                  <th class="p-4 text-sm font-semibold text-gray-600">Nama Kegiatan & Lokasi</th>
                  <th class="p-4 text-sm font-semibold text-gray-600">Waktu Pelaksanaan</th>
                  <th class="p-4 text-sm font-semibold text-gray-600">Progres</th>
                  <th class="p-4 text-sm font-semibold text-center text-gray-600">Status</th>
                  <th class="p-4 text-sm font-semibold text-right text-gray-600">Aksi</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(keg, index) in displayedActivities" :key="keg.id" class="border-b hover:bg-blue-50/30 transition" :class="{'bg-green-50/30': selectedToPrint.includes(keg.id)}">
                  
                  <td v-if="activeTab === 'selesai'" class="p-4 text-center">
                    <input type="checkbox" :value="keg.id" v-model="selectedToPrint" class="w-4 h-4 text-green-600 rounded cursor-pointer border-gray-300">
                  </td>
                  <td v-else class="p-4 text-sm text-center text-gray-500">{{ index + 1 }}</td>

                  <td class="p-4 text-sm font-semibold text-gray-800">
                    {{ keg.nama_kegiatan }}
                    <span class="block text-xs font-normal text-gray-500 mt-1"><i class="fas fa-map-marker-alt mr-1"></i>{{ extractLokasi(keg.item_kegiatan) }}</span>
                    <div v-if="keg.foto_url" @click="openPhotoModal(keg)" class="text-xs font-normal text-blue-600 hover:text-blue-800 cursor-pointer mt-1 max-w-[150px] flex items-center">
                      <i class="fas fa-image mr-1"></i> Lihat Lampiran
                    </div>
                  </td>
                  
                  <td class="p-4 text-sm text-gray-600">
                    <div v-if="keg.tanggal_mulai && keg.tanggal_selesai" class="flex flex-col gap-1 text-xs whitespace-nowrap">
                      <span class="text-blue-700 font-medium"><i class="fas fa-calendar-plus text-gray-400 w-4"></i> {{ keg.tanggal_mulai }}</span>
                      <span class="text-orange-600 font-medium"><i class="fas fa-calendar-check text-gray-400 w-4"></i> {{ keg.tanggal_selesai }}</span>
                    </div>
                    <span v-else class="text-xs italic text-gray-400">Belum diatur</span>
                  </td>

                  <td class="p-4 min-w-[150px]">
                    <div class="flex items-center gap-3">
                      <div class="w-full bg-gray-200 rounded-full h-2">
                        <div class="bg-blue-500 h-2 rounded-full transition-all duration-500" :style="{ width: keg.progress + '%' }"></div>
                      </div>
                      <span class="text-xs font-bold text-gray-700 w-8">{{ keg.progress }}%</span>
                    </div>
                  </td>
                  <td class="p-4 text-center">
                    <span v-if="getDisplayStatus(keg) === 'Selesai'" class="px-2.5 py-1 rounded-md text-xs font-bold bg-green-100 text-green-700 border border-green-200">Selesai</span>
                    <span v-else-if="getDisplayStatus(keg) === 'Berjalan'" class="px-2.5 py-1 rounded-md text-xs font-bold bg-blue-100 text-blue-700 border border-blue-200">Berjalan</span>
                    <span v-else-if="getDisplayStatus(keg) === 'Ditunda'" class="px-2.5 py-1 rounded-md text-xs font-bold bg-red-100 text-red-700 border border-red-200">Ditunda</span>
                    <span v-else class="px-2.5 py-1 rounded-md text-xs font-bold bg-yellow-100 text-yellow-700 border border-yellow-200">Menunggu</span>
                  </td>
                  <td class="p-4 flex gap-2 justify-end">
                    <button @click="openEditModal(keg)" class="text-blue-600 bg-blue-50 hover:bg-blue-100 p-2 rounded-lg transition"><i class="fa-solid fa-pen"></i></button>
                    <button @click="handleDelete(keg.id)" class="text-red-600 bg-red-50 hover:bg-red-100 p-2 rounded-lg transition"><i class="fa-solid fa-trash"></i></button>
                  </td>
                </tr>
                <tr v-if="displayedActivities.length === 0">
                  <td :colspan="activeTab === 'selesai' ? 7 : 7" class="p-10 text-center text-gray-500">
                    <i class="fa-solid fa-inbox text-4xl mb-3 text-gray-300 block"></i>
                    <span v-if="searchQuery">Pencarian "{{ searchQuery }}" tidak ditemukan di area Anda.</span>
                    <span v-else-if="activeTab === 'selesai'">Belum ada kegiatan Anda yang berstatus selesai.</span>
                    <span v-else>Belum ada data kegiatan yang Anda input.</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <footer class="main-footer flex flex-wrap items-center justify-center gap-2 p-4 text-sm text-gray-500 mt-auto border-t bg-white relative z-10 print:hidden">
        <span>© 2026 Balai Wilayah Sungai Sumatera III Pekanbaru</span>
        <span class="hidden sm:inline px-1">|</span>
        <span>Kementerian Pekerjaan Umum</span>
      </footer>

      <!-- ================= TEMPLATE CETAK LAPORAN PDF ================= -->
      <div class="hidden print:block w-full bg-white text-black p-4">
        <div class="flex items-center border-b-4 border-black pb-4 mb-6">
          <img src="/logo-pu.png" alt="Logo PU" class="w-24 h-24 mr-6 object-contain">
          <div class="text-center w-full pr-12">
            <h2 class="text-xl font-bold uppercase tracking-wide">Kementerian Pekerjaan Umum dan Perumahan Rakyat</h2>
            <h3 class="text-lg font-bold uppercase tracking-wide">Direktorat Jenderal Sumber Daya Air</h3>
            <h1 class="text-2xl font-extrabold uppercase mt-1">Balai Wilayah Sungai Sumatera III Pekanbaru</h1>
            <p class="text-sm mt-2">Jl. Pepaya No.34-C, Jadirejo, Kec. Sukajadi, Kota Pekanbaru, Riau 28126</p>
          </div>
        </div>

        <div class="text-center mb-8">
          <h2 class="text-xl font-bold underline">LAPORAN PELAKSANAAN KEGIATAN (SELESAI)</h2>
        </div>

        <table class="w-full border-collapse border border-black text-sm text-left mb-12">
          <thead>
            <tr class="bg-gray-100">
              <th class="border border-black p-2 text-center w-10">No</th>
              <th class="border border-black p-2">Nama Kegiatan & Lokasi</th>
              <th class="border border-black p-2 text-center">Waktu Pelaksanaan</th>
              <th class="border border-black p-2 text-center w-24">Progres Fisik</th>
              <th class="border border-black p-2 text-center w-28">Status Verifikasi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(keg, index) in activitiesToPrint" :key="keg.id">
              <td class="border border-black p-2 text-center">{{ index + 1 }}</td>
              <td class="border border-black p-2">
                <strong class="block">{{ keg.nama_kegiatan }}</strong>
                <!-- Gunakan extractLokasi agar Tag tidak ikut tercetak -->
                <span class="text-xs text-gray-700">{{ extractLokasi(keg.item_kegiatan) }}</span>
              </td>
              <td class="border border-black p-2 text-center text-xs">
                {{ keg.tanggal_mulai || '-' }} <br> s.d <br> {{ keg.tanggal_selesai || '-' }}
              </td>
              <td class="border border-black p-2 text-center font-bold">{{ keg.progress }}%</td>
              <td class="border border-black p-2 text-center">Telah Selesai</td>
            </tr>
          </tbody>
        </table>

        <div class="flex justify-between px-10 pt-4">
          <div class="text-center">
            <p>Mengetahui,</p>
            <p class="font-bold mb-20">Kepala BWS Sumatera III</p>
            <p class="underline font-bold">(..........................................)</p>
            <p>NIP. </p>
          </div>
          <div class="text-center">
            <p>Pekanbaru, ...............................</p>
            <p>Dibuat Oleh,</p>
            <p class="font-bold mb-20 mt-2">Admin / Petugas</p>
            <p class="font-bold text-lg inline-block">(..........................................)</p>
            <p>NIP. </p>
          </div>
        </div>
      </div>
    </main>

    <!-- MODAL FOTO -->
    <div v-if="isPhotoModalOpen" class="fixed inset-0 bg-black/80 flex items-center justify-center z-[999] p-4 backdrop-blur-sm print:hidden">
      <div class="relative bg-white p-2 rounded-xl max-w-3xl w-full flex flex-col items-center">
        <button @click="isPhotoModalOpen = false" class="absolute -top-12 right-0 text-white text-4xl hover:text-gray-300">&times;</button>
        <img :src="currentPhoto" alt="Dokumentasi" class="max-h-[80vh] w-full object-contain rounded-lg">
      </div>
    </div>

    <!-- MODAL EDIT -->
    <div v-if="isEditModalOpen" class="fixed inset-0 bg-black/60 flex items-center justify-center z-[999] p-4 backdrop-blur-sm print:hidden">
      <div class="bg-white rounded-2xl w-full max-w-2xl overflow-hidden shadow-2xl">
        <div class="bg-blue-600 p-4 flex justify-between items-center text-white">
          <h3 class="font-bold text-lg"><i class="fas fa-pen-to-square mr-2"></i>Edit Data Kegiatan</h3>
          <button @click="closeEditModal" class="text-white hover:text-gray-200 text-2xl leading-none">&times;</button>
        </div>
        <form @submit.prevent="submitEdit" class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div><label class="block text-sm font-semibold text-gray-700 mb-1">Nama Kegiatan</label><input v-model="editFormData.nama_kegiatan" type="text" class="w-full border p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none" required></div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Lokasi Detail</label>
              <input v-model="editFormData.item_kegiatan" type="text" class="w-full border p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none" required>
            </div>
            <div><label class="block text-sm font-semibold text-gray-700 mb-1">Tanggal Mulai</label><input v-model="editFormData.tanggal_mulai" type="date" class="w-full border p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none"></div>
            <div><label class="block text-sm font-semibold text-gray-700 mb-1">Tanggal Selesai</label><input v-model="editFormData.tanggal_selesai" type="date" class="w-full border p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none"></div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Status</label>
              <select v-model="editFormData.status" class="w-full border p-2.5 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none" required>
                <option value="Menunggu">Menunggu</option><option value="Berjalan">Berjalan</option><option value="Ditunda">Ditunda</option><option value="Selesai">Selesai</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Progres (%)</label>
              <div class="flex items-center gap-4 bg-gray-50 border p-2.5 rounded-lg">
                <input v-model="editFormData.progress" type="range" min="0" max="100" class="w-full accent-blue-600" @input="syncStatusWithProgress(editFormData)">
                <span class="font-bold text-blue-700 w-12 text-right">{{ editFormData.progress }}%</span>
              </div>
            </div>
          </div>
          <div class="flex justify-end gap-3 pt-4 border-t border-gray-100 mt-2">
            <button type="button" @click="closeEditModal" class="px-5 py-2 text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-lg font-semibold transition">Batal</button>
            <button type="submit" class="px-5 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-bold shadow-md transition">Simpan Perubahan</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useActivityStore } from '@/stores/activities'
import '@/assets/admin.css' 

const router = useRouter()
const authStore = useAuthStore()
const activityStore = useActivityStore()

const isSidebarOpen = ref(false)
const activeMenu = ref('dashboard') 
const searchQuery = ref('') 
const activeTab = ref('aktif') 

const extractLokasi = (text) => {
  if (!text) return ''
  const match = text.match(/^\[(.*?)\]\s(.*)/) 
  if (match) return match[2]
  return text
}

const myActivities = computed(() => {
  return activityStore.activities.filter(keg => 
    keg.item_kegiatan?.startsWith(`[${authStore.username}]`)
  )
})

const isNotificationOpen = ref(false)
const isProfileMenuOpen = ref(false)
const notifications = ref([])
const unreadNotifications = computed(() => notifications.value.filter(n => !n.read).length)

const toggleNotification = () => {
  isNotificationOpen.value = !isNotificationOpen.value; isProfileMenuOpen.value = false 
  if (isNotificationOpen.value) notifications.value.forEach(n => n.read = true)
}
const toggleProfile = () => { isProfileMenuOpen.value = !isProfileMenuOpen.value; isNotificationOpen.value = false }
const closeDropdownsOnClickOutside = (e) => {
  if (!e.target.closest('#notification-menu')) isNotificationOpen.value = false
  if (!e.target.closest('#profile-menu')) isProfileMenuOpen.value = false
}
const scrollToTop = () => window.scrollTo({ top: 0, behavior: 'smooth' })

const showForm = ref(false); const selectedFile = ref(null); const imagePreview = ref(''); const fileInput = ref(null) 
const formData = reactive({ nama_kegiatan: '', item_kegiatan: '', progress: 0, status: 'Menunggu', tanggal_mulai: '', tanggal_selesai: '' })
const isPhotoModalOpen = ref(false); const currentPhoto = ref('')
const isEditModalOpen = ref(false)
const editFormData = reactive({ id: null, nama_kegiatan: '', item_kegiatan: '', progress: 0, status: 'Menunggu', foto_url: '', preview_url: '', tanggal_mulai: '', tanggal_selesai: '' })

const selectedToPrint = ref([])

onMounted(() => {
  if (!authStore.isAuthenticated || authStore.role !== 'admin') router.push('/')
  else { activityStore.fetchActivities(); document.addEventListener('click', closeDropdownsOnClickOutside) }
})

onUnmounted(() => document.removeEventListener('click', closeDropdownsOnClickOutside))

const openForm = () => {
  formData.item_kegiatan = '' 
  showForm.value = true
}

const getDisplayStatus = (keg) => {
  if (keg.progress == 100) return 'Selesai'
  if (keg.status) {
     if (keg.status === 'Selesai' && keg.progress < 100) return 'Selesai'
     return keg.status
  }
  return keg.progress > 0 ? 'Berjalan' : 'Menunggu'
}

const syncStatusWithProgress = (dataObj) => {
  if (dataObj.progress == 100) dataObj.status = 'Selesai'
  else if (dataObj.progress > 0 && dataObj.status === 'Menunggu') dataObj.status = 'Berjalan'
}

const totalKegiatan = computed(() => myActivities.value.length)
const countSelesai = computed(() => myActivities.value.filter(keg => getDisplayStatus(keg) === 'Selesai').length)
const countBerjalan = computed(() => myActivities.value.filter(keg => getDisplayStatus(keg) === 'Berjalan').length)
const countMenunggu = computed(() => myActivities.value.filter(keg => getDisplayStatus(keg) === 'Menunggu').length)
const countDitunda = computed(() => myActivities.value.filter(keg => getDisplayStatus(keg) === 'Ditunda').length)

const pieChartStyle = computed(() => {
  if (totalKegiatan.value === 0) return 'conic-gradient(#e5e7eb 0 100%)' 
  const p1 = (countSelesai.value / totalKegiatan.value) * 100
  const p2 = p1 + ((countBerjalan.value / totalKegiatan.value) * 100)
  const p3 = p2 + ((countMenunggu.value / totalKegiatan.value) * 100)
  return `conic-gradient(#22c55e 0% ${p1}%, #3b82f6 ${p1}% ${p2}%, #eab308 ${p2}% ${p3}%, #ef4444 ${p3}% 100%)`
})

const activeActivitiesProgress = computed(() => {
  return myActivities.value.filter(k => getDisplayStatus(k) !== 'Selesai' && k.progress > 0).sort((a, b) => b.progress - a.progress)
})

const displayedActivities = computed(() => {
  let baseData = activeTab.value === 'aktif' 
    ? myActivities.value.filter(keg => getDisplayStatus(keg) !== 'Selesai')
    : myActivities.value.filter(keg => getDisplayStatus(keg) === 'Selesai')

  if (!searchQuery.value) return baseData
  const query = searchQuery.value.toLowerCase()
  return baseData.filter(keg => 
    keg.nama_kegiatan.toLowerCase().includes(query) || 
    extractLokasi(keg.item_kegiatan).toLowerCase().includes(query)
  )
})

const isAllSelesaiSelected = computed(() => {
  const finishedList = displayedActivities.value.filter(k => getDisplayStatus(k) === 'Selesai')
  return finishedList.length > 0 && selectedToPrint.value.length === finishedList.length
})

const toggleSelectAllSelesai = () => {
  const finishedList = displayedActivities.value.filter(k => getDisplayStatus(k) === 'Selesai')
  if (isAllSelesaiSelected.value) selectedToPrint.value = []
  else selectedToPrint.value = finishedList.map(k => k.id)
}

const activitiesToPrint = computed(() => myActivities.value.filter(keg => selectedToPrint.value.includes(keg.id)))

// PERBAIKAN 2: Menggunakan FileReader agar format gambar menjadi Base64 dan tersimpan permanen
const handleFileUpload = (e) => {
  const file = e.target.files[0]; 
  if (file) { 
    selectedFile.value = file; 
    
    // Ubah gambar menjadi Base64 String agar tidak hilang saat refresh halaman
    const reader = new FileReader();
    reader.onload = (event) => {
      imagePreview.value = event.target.result;
    };
    reader.readAsDataURL(file);
  }
}

const removeImage = () => { selectedFile.value = null; imagePreview.value = ''; if (fileInput.value) fileInput.value.value = '' }

const submitActivity = async () => {
  if (!selectedFile.value) { alert('Harap unggah foto!'); return }
  
  const lokasiDenganTag = `[${authStore.username}] ${formData.item_kegiatan}`
  
  const finalData = { ...formData, item_kegiatan: lokasiDenganTag, foto_url: selectedFile.value.name, preview_url: imagePreview.value }
  await activityStore.addActivity(finalData)
  
  Object.assign(formData, { nama_kegiatan: '', item_kegiatan: '', progress: 0, status: 'Menunggu', tanggal_mulai: '', tanggal_selesai: '' })
  removeImage(); showForm.value = false
}

const openPhotoModal = (keg) => { currentPhoto.value = keg.preview_url || `https://placehold.co/600x400/eeeeee/888888?text=File:+${keg.foto_url}`; isPhotoModalOpen.value = true }

const openEditModal = (keg) => { 
  Object.assign(editFormData, keg); 
  editFormData.item_kegiatan = extractLokasi(keg.item_kegiatan)
  editFormData.status = getDisplayStatus(keg); 
  isEditModalOpen.value = true 
}

const closeEditModal = () => isEditModalOpen.value = false
const submitEdit = async () => { 
  const updatedData = { ...editFormData }
  updatedData.item_kegiatan = `[${authStore.username}] ${editFormData.item_kegiatan}`
  
  await activityStore.updateActivity(updatedData); 
  closeEditModal() 
}

const handleDelete = async (id) => { 
  if (confirm('Yakin ingin menghapus?')) { 
    await activityStore.deleteActivity(id); 
    selectedToPrint.value = selectedToPrint.value.filter(selId => selId !== id) 
  } 
}

const printLaporan = () => { 
  if(selectedToPrint.value.length === 0) {
    alert("Silakan buka Tab 'Telah Selesai' dan centang kegiatan yang ingin dicetak terlebih dahulu.")
    return
  }
  window.print() 
}

const formattedDate = computed(() => {
  const t = new Date(); const m = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
  return `${t.getDate()} ${m[t.getMonth()]} ${t.getFullYear()}`
})
const handleLogout = () => { authStore.logout(); router.push('/') }
</script>

<style scoped>
.fade-slide-enter-active, .fade-slide-leave-active { transition: all 0.2s ease; }
.fade-slide-enter-from, .fade-slide-leave-to { opacity: 0; transform: translateY(-10px); }

.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>