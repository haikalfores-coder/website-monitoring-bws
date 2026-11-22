
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import os

# ==========================================
# KONFIGURASI LOKASI DATABASE
# ==========================================

RAILWAY_DATA_DIR = "/app/data"

# Jika direktori Volume Railway tersedia, gunakan database di Volume.
# Jika tidak, gunakan database lokal.
if os.path.isdir(RAILWAY_DATA_DIR):
    DATABASE_PATH = os.path.join(RAILWAY_DATA_DIR, "database.db")
else:
    DATABASE_PATH = "./database.db"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

print("Lokasi database yang digunakan:", DATABASE_PATH)


# ==========================================
# PEMBUATAN ENGINE SQLITE
# ==========================================

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# ==========================================
# SESSION DATABASE
# ==========================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ==========================================
# BASE MODEL
# ==========================================

Base = declarative_base()


# ==========================================
# TABEL USER
# ==========================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)


# ==========================================
# TABEL KEGIATAN
# ==========================================

class Kegiatan(Base):
    __tablename__ = "kegiatan"

    id = Column(Integer, primary_key=True, index=True)
    nama_kegiatan = Column(String, index=True, nullable=False)
    item_kegiatan = Column(String, nullable=False)
    foto_url = Column(String, nullable=True)
    preview_url = Column(String, nullable=True)
    progress = Column(Integer, default=0)
    status = Column(String, default="Menunggu")
    tanggal_mulai = Column(String, nullable=True)
    tanggal_selesai = Column(String, nullable=True)
    laporan_ready = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
