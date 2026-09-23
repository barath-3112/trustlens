from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .database import connect_db, close_db
from .routers import auth, scans

@asynccontextmanager
async def lifespan(app):
    try: await connect_db()
    except Exception as exc: app.state.database_error=str(exc)
    yield
    await close_db()
app=FastAPI(title="TrustLens API",version="1.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=get_settings().cors_origins.split(","),allow_credentials=False,allow_methods=["*"],allow_headers=["*"])
app.include_router(auth.router); app.include_router(scans.router)
@app.get("/api/health")
async def health():
    if getattr(app.state,"database_error",None): raise HTTPException(503,"Database unavailable; configure MONGODB_URI")
    return {"status":"ok","service":"trustlens-api"}
