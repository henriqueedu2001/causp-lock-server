import os
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from .database import get_session
from .crud import create_qrcode, list_qrcodes, get_qrcode
from .auth.signer import Signer       # ← aqui, import relativo!
from datetime import datetime


# pegue a chave secreta em bytes
#SECRET_KEY = bytes.fromhex(os.getenv("SECRET_KEY").replace(" ", ""))

# pega a SECRET_KEY como texto e transforma em bytes UTF-8
SECRET_KEY = os.getenv("SECRET_KEY").encode("utf-8")

router = APIRouter(prefix="/qrcodes", tags=["qrcodes"])

@router.post("/")
def post_qrcode(payload: str, expires_at: datetime | None = None, db: Session = Depends(get_session)):
    sig_bytes = Signer.sign(payload.encode(), SECRET_KEY)
    sig_hex = sig_bytes.hex()
    qr = create_qrcode(db, payload, sig_hex, expires_at)
    return qr

@router.get("/")
def get_all_qrcodes(db: Session = Depends(get_session)):
    return list_qrcodes(db)

@router.get("/{qr_id}")
def get_one_qrcode(qr_id: int, db: Session = Depends(get_session)):
    qr = get_qrcode(db, qr_id)
    if not qr:
        raise HTTPException(status_code=404, detail="QR Code não encontrado")
    return qr
