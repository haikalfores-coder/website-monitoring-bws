from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import models
from passlib.context import CryptContext

# Inisialisasi Router DENGAN PREFIX /api
router = APIRouter(prefix="/api")

# Inisialisasi library hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LoginRequest(BaseModel):
    username: str
    password: str

class KegiatanCreate(BaseModel):
    nama_kegiatan: str
    item_kegiatan: str
    foto_url: str
    progress: int
    status: Optional[str] = "Menunggu"
    preview_url: Optional[str] = ""
    tanggal_mulai: Optional[str] = ""
    tanggal_selesai: Optional[str] = ""

class KegiatanResponse(BaseModel):
    id: int
    nama_kegiatan: str
    item_kegiatan: str
    foto_url: str
    progress: int
    laporan_ready: bool
    status: Optional[str] = "Menunggu"
    preview_url: Optional[str] = ""
    tanggal_mulai: Optional[str] = ""
    tanggal_selesai: Optional[str] = ""

    class Config:
        from_attributes = True

@router.post("/login")
def login(user_credentials: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
    
    if not user or not pwd_context.verify(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah"
        )
    
    return {"message": "Login berhasil", "role": user.role, "username": user.username}

@router.get("/kegiatan", response_model=List[KegiatanResponse])
def get_semua_kegiatan(db: Session = Depends(get_db)):
    kegiatan = db.query(models.Kegiatan).order_by(models.Kegiatan.id.desc()).all()
    return kegiatan

@router.post("/kegiatan", response_model=KegiatanResponse, status_code=status.HTTP_201_CREATED)
def tambah_kegiatan(kegiatan: KegiatanCreate, db: Session = Depends(get_db)):
    db_kegiatan = models.Kegiatan(
        nama_kegiatan=kegiatan.nama_kegiatan,
        item_kegiatan=kegiatan.item_kegiatan,
        foto_url=kegiatan.foto_url,
        progress=kegiatan.progress,
        laporan_ready=False
    )
    
    for key, value in kegiatan.dict(exclude_unset=True).items():
        if hasattr(db_kegiatan, key):
            setattr(db_kegiatan, key, value)

    db.add(db_kegiatan)
    db.commit()
    db.refresh(db_kegiatan)
    return db_kegiatan

@router.put("/kegiatan/{kegiatan_id}", response_model=KegiatanResponse)
def update_kegiatan(kegiatan_id: int, kegiatan_update: KegiatanCreate, db: Session = Depends(get_db)):
    db_kegiatan = db.query(models.Kegiatan).filter(models.Kegiatan.id == kegiatan_id).first()
    if not db_kegiatan:
        raise HTTPException(status_code=404, detail="Kegiatan tidak ditemukan")
    
    for key, value in kegiatan_update.dict(exclude_unset=True).items():
        if hasattr(db_kegiatan, key):
            setattr(db_kegiatan, key, value)
            
    db.commit()
    db.refresh(db_kegiatan)
    return db_kegiatan

@router.delete("/kegiatan/{kegiatan_id}", status_code=status.HTTP_204_NO_CONTENT)
def hapus_kegiatan(kegiatan_id: int, db: Session = Depends(get_db)):
    kegiatan = db.query(models.Kegiatan).filter(models.Kegiatan.id == kegiatan_id).first()
    if not kegiatan:
        raise HTTPException(status_code=404, detail="Kegiatan tidak ditemukan")
    
    db.delete(kegiatan)
    db.commit()
    return {"message": "Kegiatan berhasil dihapus"}

@router.put("/kegiatan/prepare-report")
def siapkan_laporan(db: Session = Depends(get_db)):
    kegiatan_belum_siap = db.query(models.Kegiatan).filter(models.Kegiatan.laporan_ready == False).all()
    
    if not kegiatan_belum_siap:
        return {"message": "Semua laporan sudah disiapkan sebelumnya"}

    for keg in kegiatan_belum_siap:
        keg.laporan_ready = True
    
    db.commit()
    return {"message": f"{len(kegiatan_belum_siap)} laporan berhasil disiapkan", "status": "success"}