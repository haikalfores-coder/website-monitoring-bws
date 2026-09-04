import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import rute dan database
from routes import router
from models import Base, engine

app = FastAPI(
    title="API Monitoring BWS Sumatera III",
    description="Sistem backend untuk monitoring kegiatan, dikelola oleh Admin dan dipantau oleh Superuser.",
    version="1.0.0"
)

# Konfigurasi CORS (Cross-Origin Resource Sharing)
# CATATAN: JANGAN tambahkan slash '/' di paling akhir domain Netlify/Firebase!
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://starlit-starburst-b4f3be.netlify.app",  # Perbaikan: Slash '/' di ujung sudah dihapus
    "https://monitoring-bws-b8e36.web.app",          # Perbaikan: Slash '/' di ujung sudah dihapus
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
    # Server hosting (Render/Railway) akan memberikan Port dinamis lewat environment variable.
    port = int(os.environ.get("PORT", 8000))
    
    # Reload diaktifkan hanya jika dijalankan secara lokal (development mode)
    # Jika di Render, disarankan reload=False agar server lebih cepat dan hemat resource.
    is_dev = os.environ.get("ENVIRONMENT", "production") == "development"
    
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=is_dev)