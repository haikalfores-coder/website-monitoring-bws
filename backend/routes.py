from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import models
from passlib.context import CryptContext
import os
import shutil
import uuid

# Inisialisasi Router DENGAN PREFIX /api
router = APIRouter(prefix="/api")

# Inisialisasi library hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Setup folder untuk menyimpan foto
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LoginRequest(BaseModel):
    username: str
    password: str

# KegiatanCreate (BaseModel) kita hapus dari endpoint POST/PUT karena kita pakai Form()
# Namun KegiatanResponse tetap kita gunakan untuk format response.
class KegiatanResponse(BaseModel):
    id: int
    nama_kegiatan: str
    item_kegiatan: str
    foto_url: Optional[str] = ""
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


# -- PERBAIKAN POST: Menggunakan Form(...) dan File(...) --
@router.post("/kegiatan", response_model=KegiatanResponse, status_code=status.HTTP_201_CREATED)
def tambah_kegiatan(
    nama_kegiatan: str = Form(...),
    item_kegiatan: str = Form(...),
    progress: int = Form(0),
    status_kegiatan: str = Form("Menunggu", alias="status"),
    tanggal_mulai: str = Form(""),
    tanggal_selesai: str = Form(""),
    foto: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    foto_url = ""
    # Jika ada file foto yang diupload
    if foto and foto.filename:
        file_extension = foto.filename.split(".")[-1]
        file_name = f"{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)
            
        foto_url = f"/uploads/{file_name}" # URL path untuk diakses frontend

    db_kegiatan = models.Kegiatan(
        nama_kegiatan=nama_kegiatan,
        item_kegiatan=item_kegiatan,
        foto_url=foto_url,
        progress=progress,
        status=status_kegiatan,
        tanggal_mulai=tanggal_mulai,
        tanggal_selesai=tanggal_selesai,
        laporan_ready=False
    )

    db.add(db_kegiatan)
    db.commit()
    db.refresh(db_kegiatan)
    return db_kegiatan


# -- PERBAIKAN PUT: Menggunakan Form(...) dan File(...) --
@router.put("/kegiatan/{kegiatan_id}", response_model=KegiatanResponse)
def update_kegiatan(
    kegiatan_id: int,
    nama_kegiatan: str = Form(None),
    item_kegiatan: str = Form(None),
    progress: int = Form(None),
    status_kegiatan: str = Form(None, alias="status"),
    tanggal_mulai: str = Form(None),
    tanggal_selesai: str = Form(None),
    delete_foto: str = Form(None),
    foto: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    db_kegiatan = db.query(models.Kegiatan).filter(models.Kegiatan.id == kegiatan_id).first()
    if not db_kegiatan:
        raise HTTPException(status_code=404, detail="Kegiatan tidak ditemukan")
    
    # Update field teks jika ada
    if nama_kegiatan is not None: db_kegiatan.nama_kegiatan = nama_kegiatan
    if item_kegiatan is not None: db_kegiatan.item_kegiatan = item_kegiatan
    if progress is not None: db_kegiatan.progress = progress
    if status_kegiatan is not None: db_kegiatan.status = status_kegiatan
    if tanggal_mulai is not None: db_kegiatan.tanggal_mulai = tanggal_mulai
    if tanggal_selesai is not None: db_kegiatan.tanggal_selesai = tanggal_selesai

    # Jika Frontend meminta hapus foto lama (tong sampah ditekan)
    if delete_foto == 'true':
        db_kegiatan.foto_url = ""

    # Jika ada file foto baru yang diupload
    if foto and foto.filename:
        file_extension = foto.filename.split(".")[-1]
        file_name = f"{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)
            
        db_kegiatan.foto_url = f"/uploads/{file_name}"

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