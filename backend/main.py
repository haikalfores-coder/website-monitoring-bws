
import os
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from sqlalchemy import text

# Import rute dan database
from routes import router
from models import Base, engine, SessionLocal, User


# --------------------------------------------------
# KONFIGURASI LOKASI PENYIMPANAN
# --------------------------------------------------

IS_RAILWAY = bool(os.getenv("RAILWAY_ENVIRONMENT"))

if IS_RAILWAY:
    DATA_DIR = "/app/data"
    UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
else:
    DATA_DIR = "."
    UPLOAD_DIR = "./uploads"

# Membuat folder penyimpanan jika belum tersedia
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)


# --------------------------------------------------
# INISIALISASI FASTAPI
# --------------------------------------------------

app = FastAPI(
    title="API Monitoring BWS Sumatera III",
    description="Sistem backend untuk monitoring kegiatan, dikelola oleh Admin dan dipantau oleh Superuser.",
    version="1.0.0"
)


# --------------------------------------------------
# KONFIGURASI CORS
# --------------------------------------------------

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# AKSES FOLDER UPLOADS
# --------------------------------------------------

app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads"
)


# --------------------------------------------------
# MEMBUAT TABEL DATABASE
# --------------------------------------------------

Base.metadata.create_all(bind=engine)

print("Lokasi database:", engine.url.database)

# Memeriksa versi SQLite yang digunakan database
with engine.connect() as connection:
    sqlite_version = connection.execute(
        text("SELECT sqlite_version()")
    ).scalar_one()

print("Versi SQLite database:", sqlite_version)


# --------------------------------------------------
# AUTO-SEEDING USER DEFAULT
# --------------------------------------------------

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def buat_user_default():
    db = SessionLocal()

    try:
        # Hapus akun admin dan super lama jika masih ada
        akun_lama = db.query(User).filter(
            User.username.in_(["admin", "super"])
        ).all()

        for akun in akun_lama:
            db.delete(akun)
            print(f"Akun lama '{akun.username}' berhasil dihapus!")

        # Daftar akun default:
        # 4 Admin dan 3 Superuser
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

            # Periksa apakah username sudah tersedia
            existing_user = db.query(User).filter(
                User.username == user_data["username"]
            ).first()

            if not existing_user:
                hashed_password = pwd_context.hash(
                    user_data["password"]
                )

                user_baru = User(
                    username=user_data["username"],
                    password_hash=hashed_password,
                    role=user_data["role"]
                )

                db.add(user_baru)

                print(
                    f"Akun '{user_data['username']}' berhasil dibuat otomatis!"
                )

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


# Menjalankan seeding sebelum server menerima request
buat_user_default()


# --------------------------------------------------
# MENGHUBUNGKAN ROUTES
# --------------------------------------------------

app.include_router(router)


# --------------------------------------------------
# ENDPOINT PEMERIKSAAN SERVER
# --------------------------------------------------

@app.get("/")
def check_health():
    return {
        "status": "Online",
        "instansi": "BWS Sumatera III Pekanbaru",
        "pesan": "Server FastAPI siap menerima request."
    }


# --------------------------------------------------
# MENJALANKAN SERVER
# --------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))

    is_dev = (
        os.environ.get("ENVIRONMENT", "production") == "development"
    )

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=is_dev
    )
