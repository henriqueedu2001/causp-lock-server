from sqlmodel import select
from sqlmodel import Session
from .models import QRCode

def create_qrcode(db: Session, payload: str, signature: str, expires_at=None):
    qr = QRCode(payload=payload, signature=signature, expires_at=expires_at)
    db.add(qr)
    db.commit()
    db.refresh(qr)
    return qr

def list_qrcodes(db: Session):
    return db.exec(select(QRCode).order_by(QRCode.created_at.desc())).all()

def get_qrcode(db: Session, qr_id: int):
    return db.get(QRCode, qr_id)
