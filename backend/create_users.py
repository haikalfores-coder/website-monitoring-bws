from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models
from passlib.context import CryptContext

# 1. Buat koneksi langsung ke file database.db secara mandiri
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Inisialisasi library hashing untuk enkripsi password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_users():
    # Pastikan tabel sudah terbentuk di database
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Hapus semua akun lama dari tabel User
        db.query(models.User).delete()
        
        # Daftar 7 Akun Baru
        users_data = [
            {"username": "admin1", "password": "admin1", "role": "admin"},
            {"username": "admin2", "password": "admin2", "role": "admin"},
            {"username": "admin3", "password": "admin3", "role": "admin"},
            {"username": "admin4", "password": "admin4", "role": "admin"},
            {"username": "super1", "password": "super1", "role": "superuser"},
            {"username": "super2", "password": "super2", "role": "superuser"},
            {"username": "super3", "password": "super3", "role": "superuser"},
        ]
        
        # Masukkan ke Database
        for u in users_data:
            hashed_pw = pwd_context.hash(u["password"])
            
            # MENGGUNAKAN 'password_hash' SESUAI FILE models.py ANDA
            new_user = models.User(
                username=u["username"], 
                password_hash=hashed_pw, 
                role=u["role"]
            )
            db.add(new_user)
            
        db.commit()
        print("✅ SUKSES: Akun lama dihapus dan 7 Akun baru berhasil dimasukkan ke database!")
        print("Silakan login di web menggunakan username 'admin1' atau 'super1'.")
        
    except Exception as e:
        print(f"❌ TERJADI KESALAHAN: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_users()