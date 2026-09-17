#main.py
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext  # Tambahan untuk hash password

# Import rute dan database
from routes import router
from models import Base, engine, SessionLocal, User  # Tambahan import SessionLocal dan User

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

# Membuat tabel di database saat server pertama kali berjalan
Base.metadata.create_all(bind=engine)

# --- FUNGSI AUTO-SEEDING (Membuat User Default Otomatis) ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def buat_user_default():
    db = SessionLocal()
    try:
        # 1. Cek dan buat akun Admin
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            hashed_password = pwd_context.hash("admin")
            admin_baru = User(username="admin", password_hash=hashed_password, role="admin")
            db.add(admin_baru)
            print("Akun 'admin' berhasil dibuat otomatis!")

        # 2. Cek dan buat akun Superuser
        super_user = db.query(User).filter(User.username == "super").first()
        if not super_user:
            hashed_password = pwd_context.hash("super")
            super_baru = User(username="super", password_hash=hashed_password, role="superuser")
            db.add(super_baru)
            print("Akun 'super' berhasil dibuat otomatis!")

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