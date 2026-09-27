<nav class="sidebar-menu">
        <div class="menu-title">MENU UTAMA</div>
        
        <!-- Menu Gabungan Dashboard & Data -->
        <a href="#" @click.prevent="activeMenu = 'dashboard'; scrollToTop(); isSidebarOpen = false" class="menu-item" :class="{ 'active': activeMenu === 'dashboard' }">
          <i class="fa-solid fa-chart-line"></i> <!-- Bisa diganti fa-house atau icon lain -->
          <span>Dashboard & Data</span>
        </a>

        <div class="menu-title">LAPORAN & SISTEM</div>
        
        <!-- Tombol Cetak di Sidebar -->
        <a href="#" @click.prevent="printLaporan" class="menu-item font-bold transition" :class="selectedToPrint.length > 0 ? 'text-green-600 bg-green-50 hover:bg-green-100' : 'text-gray-400 bg-gray-50 cursor-not-allowed'">
          <i class="fa-solid fa-file-pdf"></i>
          <span>Cetak PDF ({{ selectedToPrint.length }})</span>
        </a>

        <router-link to="/profil" class="menu-item" @click="isSidebarOpen = false">
          <i class="fa-solid fa-user"></i>
          <span>Profil Saya</span>
        </router-link>
      </nav>

<script setup>
import { ref, computed, onMounted, onUnmounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useActivityStore } from '@/stores/activities'
import '@/assets/admin.css' 

const router = useRouter()
const authStore = useAuthStore()
const activityStore = useActivityStore()

// --- PERBAIKAN URL GAMBAR ---
// Ambil URL backend dari Vite Env (Misal: https://monitoring-bws.railway.app)
const BACKEND_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Fungsi untuk menggabungkan path foto agar URL fotonya utuh (tidak rusak)
const getFullImageUrl = (path) => {
  if (!path) return 'https://placehold.co/600x400/eeeeee/888888?text=Tidak+Ada+Foto'
  if (path.startsWith('http') || path.startsWith('data:')) return path
  return `${BACKEND_URL}${path}`
}
// ----------------------------

const isSidebarOpen = ref(false)
const activeMenu = ref('dashboard') 
const searchQuery = ref('') 
const activeTab = ref('aktif') 
const isSubmitting = ref(false)

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

const toggleProfile = () => { isProfileMenuOpen.value = !isProfileMenuOpen.value; isNotificationOpen.value = false }
const closeDropdownsOnClickOutside = (e) => {
  if (!e.target.closest('#notification-menu')) isNotificationOpen.value = false
  if (!e.target.closest('#profile-menu')) isProfileMenuOpen.value = false
}
const scrollToTop = () => window.scrollTo({ top: 0, behavior: 'smooth' })

const showForm = ref(false); 
const selectedFile = ref(null); 
const imagePreview = ref(''); 
const fileInput = ref(null); 
const formData = reactive({ nama_kegiatan: '', item_kegiatan: '', progress: 0, status: 'Menunggu', tanggal_mulai: '', tanggal_selesai: '' })
const isPhotoModalOpen = ref(false); 
const currentPhoto = ref('')

const isEditModalOpen = ref(false)
const isSubmittingEdit = ref(false)
const editSelectedFile = ref(null)
const editImagePreview = ref('')
const editFileInput = ref(null)

// State untuk melacak apakah user sengaja menekan tombol hapus foto di modal edit
const isEditPhotoRemoved = ref(false)

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

// --- FITUR PREVIEW GAMBAR (FORM TAMBAH) ---
const handleFileUpload = (e) => {
  const file = e.target.files[0]; 
  if (file) { 
    selectedFile.value = file; 
    const reader = new FileReader();
    reader.onload = (event) => {
      imagePreview.value = event.target.result;
    };
    reader.readAsDataURL(file);
  }
}

const removeImage = () => { selectedFile.value = null; imagePreview.value = ''; if (fileInput.value) fileInput.value.value = '' }

// --- FITUR PREVIEW GAMBAR (FORM EDIT) ---
const handleEditFileUpload = (e) => {
  const file = e.target.files[0];
  if (file) {
    editSelectedFile.value = file;
    isEditPhotoRemoved.value = false; 
    const reader = new FileReader();
    reader.onload = (event) => {
      editImagePreview.value = event.target.result;
    };
    reader.readAsDataURL(file);
  }
}

const removeEditImage = () => {
  editSelectedFile.value = null;
  editImagePreview.value = '';
  isEditPhotoRemoved.value = true; 
  if (editFileInput.value) editFileInput.value.value = '';
}

// ==============================================
// SUBMIT ACTIVITY (TAMBAH DATA) - FOTO WAJIB
// ==============================================
const submitActivity = async () => {
  // Pengecekan Foto (Wajib)
  if (!selectedFile.value) {
    alert("Dokumentasi Foto wajib diunggah untuk menyimpan data kegiatan baru!");
    return;
  }

  isSubmitting.value = true;
  const lokasiDenganTag = `[${authStore.username}] ${formData.item_kegiatan}`;
  
  const formDataApi = new FormData();
  formDataApi.append('nama_kegiatan', formData.nama_kegiatan);
  formDataApi.append('item_kegiatan', lokasiDenganTag);
  formDataApi.append('progress', Number(formData.progress)); 
  formDataApi.append('status', formData.status);
  
  if (formData.tanggal_mulai) {
    formDataApi.append('tanggal_mulai', formData.tanggal_mulai);
  }
  if (formData.tanggal_selesai) {
    formDataApi.append('tanggal_selesai', formData.tanggal_selesai);
  }
  
  formDataApi.append('foto', selectedFile.value); 

  try {
    await activityStore.addActivity(formDataApi);
    
    // Reset Form
    Object.assign(formData, { nama_kegiatan: '', item_kegiatan: '', progress: 0, status: 'Menunggu', tanggal_mulai: '', tanggal_selesai: '' });
    removeImage(); 
    showForm.value = false;
  } catch (error) {
    console.error("Gagal saat submit data:", error);
    let pesanError = 'Terjadi kesalahan validasi saat menyimpan data.\n';
    if (error.response && error.response.data) {
      if (error.response.data.errors) {
        const errorList = Object.values(error.response.data.errors).flat().join('\n- ');
        pesanError += '\nDetail Error:\n- ' + errorList;
      } else if (error.response.data.message) {
        pesanError += '\nPesan: ' + error.response.data.message;
      }
    }
    alert(pesanError);
  } finally {
    isSubmitting.value = false;
  }
}

// Menampilkan gambar pada Modal Foto dengan URL Utuh
const openPhotoModal = (keg) => { 
  currentPhoto.value = getFullImageUrl(keg.foto_url)
  isPhotoModalOpen.value = true 
}

// Membuka Modal Edit dan Menampilkan Gambar Preview dengan URL Utuh
const openEditModal = (keg) => { 
  Object.assign(editFormData, keg); 
  editFormData.item_kegiatan = extractLokasi(keg.item_kegiatan)
  editFormData.status = getDisplayStatus(keg); 
  
  // Perbaikan preview image edit
  editImagePreview.value = keg.foto_url ? getFullImageUrl(keg.foto_url) : '';
  editSelectedFile.value = null;
  isEditPhotoRemoved.value = false; 

  isEditModalOpen.value = true 
}

const closeEditModal = () => {
  isEditModalOpen.value = false
  editSelectedFile.value = null;
  editImagePreview.value = '';
  isEditPhotoRemoved.value = false;
  if (editFileInput.value) editFileInput.value.value = '';
}

// ==============================================
// SUBMIT EDIT ACTIVITY - FOTO WAJIB ADA
// ==============================================
const submitEdit = async () => { 
  // Pengecekan Foto (Wajib ada)
  if (!editImagePreview.value && !editSelectedFile.value) {
    alert("Dokumentasi Foto wajib ada! Silakan unggah foto baru jika yang lama dihapus.");
    return;
  }

  isSubmittingEdit.value = true;
  try {
    const lokasiDenganTag = `[${authStore.username}] ${editFormData.item_kegiatan}`;

    // Gunakan FormData jika user mengunggah foto baru ATAU jika user sengaja MENGHAPUS foto
    if (editSelectedFile.value || isEditPhotoRemoved.value) {
      const formDataApi = new FormData();
      
      formDataApi.append('id', editFormData.id);
      formDataApi.append('nama_kegiatan', editFormData.nama_kegiatan);
      formDataApi.append('item_kegiatan', lokasiDenganTag);
      formDataApi.append('progress', Number(editFormData.progress));
      formDataApi.append('status', editFormData.status);
      
      if (editFormData.tanggal_mulai) {
        formDataApi.append('tanggal_mulai', editFormData.tanggal_mulai);
      }
      if (editFormData.tanggal_selesai) {
        formDataApi.append('tanggal_selesai', editFormData.tanggal_selesai);
      }
      
      if (editSelectedFile.value) {
        formDataApi.append('foto', editSelectedFile.value);
      } 
      if (isEditPhotoRemoved.value) {
        formDataApi.append('delete_foto', 'true');
        formDataApi.append('remove_foto', 'true'); 
      }

      await activityStore.updateActivity(formDataApi);
    } 
    // Jika tidak ada perubahan sama sekali pada foto (pakai JSON)
    else {
      const updatedData = { ...editFormData };
      updatedData.item_kegiatan = lokasiDenganTag;
      updatedData.progress = Number(updatedData.progress);
      
      // Hapus properti tanggal jika kosong agar tidak men-trigger error date format
      if (!updatedData.tanggal_mulai) delete updatedData.tanggal_mulai;
      if (!updatedData.tanggal_selesai) delete updatedData.tanggal_selesai;

      await activityStore.updateActivity(updatedData);
    }

    closeEditModal();
  } catch (error) {
    console.error("Gagal saat mengupdate data:", error);
    let pesanError = 'Terjadi kesalahan saat mengupdate data.\n';
    if (error.response && error.response.data) {
      if (error.response.data.errors) {
        const errorList = Object.values(error.response.data.errors).flat().join('\n- ');
        pesanError += '\nDetail Error:\n- ' + errorList;
      } else if (error.response.data.message) {
        pesanError += '\nPesan: ' + error.response.data.message;
      }
    }
    alert(pesanError);
  } finally {
    isSubmittingEdit.value = false;
  }
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