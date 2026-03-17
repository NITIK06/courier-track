from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routes import auth, shipments, dashboard
from seed_data import run_seed

# ── FastAPI app ─────────────────────────────────────────
app = FastAPI(
    title="CourierTrack API",
    description="Backend for managing courier shipments across 10 branches",
    version="1.0.0"
)

# ── RUN SEED DATA AUTOMATICALLY ─────────────────────────
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    run_seed()

# ── CORS ────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── ROUTES ──────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(shipments.router)
app.include_router(dashboard.router)

# ── FRONTEND ────────────────────────────────────────────
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# ── HEALTH CHECK ────────────────────────────────────────
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "CourierTrack API is running"}