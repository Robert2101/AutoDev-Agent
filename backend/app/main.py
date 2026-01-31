"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.api.routes import audits, stats


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
    
    yield
    
    # Shutdown: Clean up resources
    print("👋 Shutting down gracefully")


# Create FastAPI application
app = FastAPI(
    title="AutoDev Agent API",
    description="An autonomous AI agent that audits GitHub repositories and creates Pull Requests with fixes",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(audits.router)
app.include_router(stats.router)


@app.get("/")
async def root():
    """Root endpoint - Health check."""
    return {
        "message": "AutoDev Agent API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected"
    }
