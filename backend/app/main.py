from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine
from app.routers import auth, words, attempts, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify DB connectivity
    yield
    # Shutdown: dispose engine
    await engine.dispose()


app = FastAPI(
    title="Zhuyin Practice API",
    description="Backend API for Zhuyin (Bopomofo) input practice",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(words.router, prefix="/api/words", tags=["words"])
app.include_router(attempts.router, prefix="/api/attempts", tags=["attempts"])
app.include_router(health.router, prefix="/api/health", tags=["health"])
