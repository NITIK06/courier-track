from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routes import auth, shipments, dashboard

# ── Create all tables in MySQL if they don't exist ────────────────────────────
Base.metadata.create_all(bind=engine)

# ── FastAPI app ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="CourierTrack API",
    description="Backend for managing courier shipments across 10 branches",
    version="1.0.0"
)

# ── CORS — allows your frontend HTML to call this API ─────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # In production: replace * with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register all route files ──────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(shipments.router)
app.include_router(dashboard.router)

# ── Serve frontend HTML as static files ──────────────────────────────────────
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


@app.get("/health")
def health_check():
    """Quick check that the server is running"""
    return {"status": "ok", "message": "CourierTrack API is running"}
