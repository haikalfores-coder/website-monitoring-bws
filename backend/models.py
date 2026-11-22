
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
import os

# Menentukan lokasi database
# Railway menggunakan Volume di /app/data
# Komputer lokal menggunakan database.db di folder proyek
if os.getenv("RAILWAY_ENVIRONMENT"):
    DATABASE_PATH = "/app/data/database.db"
else:
    DATABASE_PATH = "./database.db"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Pembuatan Engine SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Pembuatan session untuk berinteraksi dengan database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class untuk mendefinisikan model tabel
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)


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
