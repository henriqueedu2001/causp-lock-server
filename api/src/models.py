from sqlmodel import SQLModel, Field
from datetime import datetime

class QRCode(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    payload: str
    signature: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime | None = None
