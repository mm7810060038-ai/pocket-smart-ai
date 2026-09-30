from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import APP_NAME
from .database import init_db
from .routes import pages, auth, planners


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=APP_NAME,
    version="1.0.0",
    lifespan=lifespan
)


# =========================
# Static Files
# =========================

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Routers
# =========================

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(planners.router)


# =========================
# Health Check
# =========================

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": APP_NAME
    }


@app.get("/startup")
async def startup():
    return {
        "status": "ready",
        "app": APP_NAME
    }


# =========================
# Run Application
# =========================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )