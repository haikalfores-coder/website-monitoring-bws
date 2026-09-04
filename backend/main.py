from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os  # Tambahkan modul ini untuk membaca Port dari server hosting

# Menghapus tanda komentar agar rute dan database terhubung
from routes import router
from models import Base, engine

app = FastAPI(
    title="API Monitoring BWS Sumatera III",
    description="Sistem backend untuk monitoring kegiatan, dikelola oleh Admin dan dipantau oleh Superuser.",
    version="1.0.0"
)

# Konfigurasi CORS (Cross-Origin Resource Sharing)
# WAJIB: Masukkan URL domain Netlify / Firebase Frontend Anda ke dalam daftar ini nanti
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://bws-monitoring.netlify.app",  # GANTI INI DENGAN LINK NETLIFY ANDA NANTI
    "https://bws-monitoring.web.app",      # GANTI INI DENGAN LINK FIREBASE ANDA NANTI
    # "*"  <-- Hapus tanda pagar di depan bintang jika Anda ingin mengizinkan SEMUA domain (mudah untuk testing tapi kurang aman)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Membuat tabel di database saat server pertama kali berjalan
Base.metadata.create_all(bind=engine)

# Menghubungkan endpoint API dari file routes.py
# Prefix "/api" sudah dipindahkan ke routes.py, jadi di sini cukup includenya saja
app.include_router(router)

@app.get("/")
def check_health():
    """Endpoint dasar untuk memastikan server berjalan"""
    return {
        "status": "Online",
        "instansi": "BWS Sumatera III Pekanbaru",
        "pesan": "Server FastAPI siap menerima request."
    }

if __name__ == "__main__":
    # Server hosting (Render/Railway) akan memberikan Port dinamis.
    # Jika dijalankan di komputer sendiri, akan fallback ke port 8000.
    port = int(os.environ.get("PORT", 8000))
    
    # Host WAJIB diubah dari "127.0.0.1" menjadi "0.0.0.0" agar bisa diakses dari internet
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)