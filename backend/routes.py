
import os
import shutil
import uuid

from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    File,
    UploadFile,
    Form
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext

import models


# =====================================================
# 1. KONFIGURASI DASAR
# =====================================================

router = APIRouter(prefix="/api")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# =====================================================
# 2. KONFIGURASI JWT
# =====================================================

SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY belum dikonfigurasi")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

bearer_scheme = HTTPBearer(auto_error=False)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =====================================================
# 3. KONEKSI DATABASE
# =====================================================

def get_db():
    db = models.SessionLocal()

    try:
        yield db
    finally:
        db.close()


# =====================================================
# 4. AUTENTIKASI DAN OTORISASI
# =====================================================

def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db)
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token autentikasi diperlukan",
            headers={"WWW-Authenticate": "Bearer"}
        )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token tidak valid"
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau sudah kedaluwarsa",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Pengguna tidak ditemukan"
        )

    return user


def require_admin(
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Anda tidak memiliki izin untuk melakukan tindakan ini"
        )

    return current_user


# =====================================================
# 5. MODEL REQUEST DAN RESPONSE
# =====================================================

class LoginRequest(BaseModel):
    username: str
    password: str


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
    tanggal_selesai: Optional[str]

    class Config:
        from_attributes = True


# =====================================================
# 6. LOGIN
# =====================================================

@router.post("/login")
def login(
    user_credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.username == user_credentials.username
    ).first()

    if not user or not pwd_context.verify(
        user_credentials.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah"
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "message": "Login berhasil",
        "role": user.role,
        "username": user.username,
        "access_token": access_token,
        "token_type": "bearer"
    }


# =====================================================
# 7. MELIHAT SELURUH KEGIATAN
# ADMIN DAN SUPERUSER
# =====================================================

@router.get(
    "/kegiatan",
    response_model=List[KegiatanResponse]
)
def get_semua_kegiatan(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    kegiatan = db.query(models.Kegiatan).order_by(
        models.Kegiatan.id.desc()
    ).all()

    return kegiatan


# =====================================================
# 8. MENAMBAH KEGIATAN
# ADMIN SAJA
# =====================================================

@router.post(
    "/kegiatan",
    response_model=KegiatanResponse,
    status_code=status.HTTP_201_CREATED
)
def tambah_kegiatan(
    nama_kegiatan: str = Form(...),
    item_kegiatan: str = Form(...),
    progress: int = Form(0),
    status_kegiatan: str = Form("Menunggu", alias="status"),
    tanggal_mulai: str = Form(""),
    tanggal_selesai: str = Form(""),
    foto: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    foto_url = ""

    if foto and foto.filename:
        file_extension = foto.filename.split(".")[-1]
        file_name = f"{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, file_name)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(foto.file, buffer)

        foto_url = f"/uploads/{file_name}"

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


# =====================================================
# 9. MENYIAPKAN LAPORAN
# ADMIN SAJA
# DILETAKKAN SEBELUM ROUTE DINAMIS
# =====================================================

@router.put("/kegiatan/prepare-report")
def siapkan_laporan(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    kegiatan_belum_siap = db.query(
        models.Kegiatan
    ).filter(
        models.Kegiatan.laporan_ready == False
    ).all()

    if not kegiatan_belum_siap:
        return {
            "message": "Semua laporan sudah disiapkan sebelumnya"
        }

    for keg in kegiatan_belum_siap:
        keg.laporan_ready = True

    db.commit()

    return {
        "message": f"{len(kegiatan_belum_siap)} laporan berhasil disiapkan",
        "status": "success"
    }


# =====================================================
# 10. MENGUBAH KEGIATAN
# ADMIN SAJA
# =====================================================

@router.put(
    "/kegiatan/{kegiatan_id}",
    response_model=KegiatanResponse
)
def update_kegiatan(
    kegiatan_id: int,
    nama_kegiatan: Optional[str] = Form(None),
    item_kegiatan: Optional[str] = Form(None),
    progress: Optional[int] = Form(None),
    status_kegiatan: Optional[str] = Form(None, alias="status"),
    tanggal_mulai: Optional[str] = Form(None),
    tanggal_selesai: Optional[str] = Form(None),
    delete_foto: Optional[str] = Form(None),
    foto: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    db_kegiatan = db.query(models.Kegiatan).filter(
        models.Kegiatan.id == kegiatan_id
    ).first()

    if not db_kegiatan:
        raise HTTPException(
            status_code=404,
            detail="Kegiatan tidak ditemukan"
        )

    if nama_kegiatan is not None:
        db_kegiatan.nama_kegiatan = nama_kegiatan

    if item_kegiatan is not None:
        db_kegiatan.item_kegiatan = item_kegiatan

    if progress is not None:
        db_kegiatan.progress = progress

    if status_kegiatan is not None:
        db_kegiatan.status = status_kegiatan

    if tanggal_mulai is not None:
        db_kegiatan.tanggal_mulai = tanggal_mulai

    if tanggal_selesai is not None:
        db_kegiatan.tanggal_selesai = tanggal_selesai

    if delete_foto == "true":
        db_kegiatan.foto_url = ""

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


# =====================================================
# 11. MENGHAPUS KEGIATAN
# ADMIN SAJA
# =====================================================

@router.delete(
    "/kegiatan/{kegiatan_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def hapus_kegiatan(
    kegiatan_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    kegiatan = db.query(models.Kegiatan).filter(
        models.Kegiatan.id == kegiatan_id
    ).first()

    if not kegiatan:
        raise HTTPException(
            status_code=404,
            detail="Kegiatan tidak ditemukan"
        )

    db.delete(kegiatan)
    db.commit()

    return None
