import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from database import connect_to_mongo, close_mongo_connection
from routers import categories, products, currency
from config import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Ensure upload directory exists at import time so StaticFiles mount works
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title="E-Commerce API",
    description="DevNet E-Commerce Platform — FastAPI backend",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Global exception handler ─────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": str(exc)},
    )


# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(categories.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(currency.router, prefix="/api")

# ── Static files (uploaded images) ───────────────────────────────────────────
app.mount("/api/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


@app.get("/")
async def root():
    return {"message": "E-Commerce API is running", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "ok"}
