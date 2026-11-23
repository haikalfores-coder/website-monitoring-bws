from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import os # Tambahkan modul os untuk membaca environment variable

# Mengambil URL Database dari layanan hosting (jika ada), 
# jika tidak ada (sedang di komputer lokal), gunakan SQLite
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# Menyesuaikan penamaan prefix PostgreSQL (Hosting seperti Render sering menggunakan 'postgres://', 
# sedangkan SQLAlchemy versi baru membutuhkan 'postgresql://')
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Pembuatan Engine
# Argumen 'check_same_thread' HANYA boleh digunakan untuk SQLite. 
# Jika dipakai di PostgreSQL (saat hosting), aplikasi akan error.
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Pembuatan session untuk berinteraksi dengan database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class untuk mendefinisikan model tabel
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False) # Menyimpan nilai 'admin' atau 'superuser'

class Kegiatan(Base):
    __tablename__ = "kegiatan"

    id = Column(Integer, primary_key=True, index=True)
    nama_kegiatan = Column(String, index=True, nullable=False)
    item_kegiatan = Column(String, nullable=False)
    foto_url = Column(String, nullable=True) # URL atau nama file gambar
    preview_url = Column(String, nullable=True) # Menyimpan Blob URL / Base64 preview
    progress = Column(Integer, default=0) # Persentase 0-100
    status = Column(String, default="Menunggu") # Menunggu, Berjalan, Ditunda, Selesai
    tanggal_mulai = Column(String, nullable=True) # Waktu mulai kegiatan
    tanggal_selesai = Column(String, nullable=True) # Waktu selesai kegiatan
    laporan_ready = Column(Boolean, default=False) # Status penyiapan laporan oleh admin
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
