import os
import uvicorn
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # <-- TAMBAHAN WAJIB
from passlib.context import CryptContext  

# Import rute dan database
from routes import router
from models import Base, engine, SessionLocal, User  

app = FastAPI(
    title="API Monitoring BWS Sumatera III",
    description="Sistem backend untuk monitoring kegiatan, dikelola oleh Admin dan dipantau oleh Superuser.",
    version="1.0.0"
)

# Konfigurasi CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# --- TAMBAHAN WAJIB: BUAT DAN BUKA AKSES FOLDER UPLOADS ---
os.makedirs("uploads", exist_ok=True) # Buat folder otomatis jika belum ada
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# ---------------------------------------------------------

# Membuat tabel di database saat server pertama kali berjalan
Base.metadata.create_all(bind=engine)

# --- FUNGSI AUTO-SEEDING (Membuat User Default Otomatis) ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def buat_user_default():
    db = SessionLocal()
    try:
        # Hapus akun 'admin' dan 'super' lama jika ada
        akun_lama = db.query(User).filter(User.username.in_(["admin", "super"])).all()
        for akun in akun_lama:
            db.delete(akun)
            print(f"Akun lama '{akun.username}' berhasil dihapus!")

        # Daftar akun default: Tepat 4 Admin dan 3 Superuser
        default_users = [
            {"username": "admin1", "password": "admin1", "role": "admin"},
            {"username": "admin2", "password": "admin2", "role": "admin"},
            {"username": "admin3", "password": "admin3", "role": "admin"},
            {"username": "admin4", "password": "admin4", "role": "admin"},
            {"username": "super1", "password": "super1", "role": "superuser"},
            {"username": "super2", "password": "super2", "role": "superuser"},
            {"username": "super3", "password": "super3", "role": "superuser"},
        ]

        for user_data in default_users:
            # Cek apakah username sudah ada di database
            existing_user = db.query(User).filter(User.username == user_data["username"]).first()
            
            if not existing_user:
                hashed_password = pwd_context.hash(user_data["password"])
                # Menyesuaikan dengan kolom 'password_hash' di model Anda
                user_baru = User(
                    username=user_data["username"], 
                    password_hash=hashed_password, 
                    role=user_data["role"]
                )
                db.add(user_baru)
                print(f"Akun '{user_data['username']}' berhasil dibuat otomatis!")

        db.commit()
    finally:
        db.close()

# Jalankan fungsi seeding sebelum server menerima request
buat_user_default()
# -----------------------------------------------------------

# Menghubungkan endpoint API dari file routes.py
app.include_router(router)

@app.get("/")
def check_health():
    return {
        "status": "Online",
        "instansi": "BWS Sumatera III Pekanbaru",
        "pesan": "Server FastAPI siap menerima request."
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    is_dev = os.environ.get("ENVIRONMENT", "production") == "development"
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=is_dev)

print("Versi SQLite:", sqlite3.sqlite_version)
