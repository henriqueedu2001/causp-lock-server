from fastapi import FastAPI
from .database import init_db
from .routers import router as qr_router

app = FastAPI(title="CAUSP-LOCK API")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(qr_router)
