"""
════════════════════════════════════════════════════════════════
WORDDEE-AI Backend - Main Application
════════════════════════════════════════════════════════════════
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes import practice, dashboard
from backend.db.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Worddee.ai Backend",
    description="AI-powered English sentence practice platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(practice.router)
app.include_router(dashboard.router)


@app.get("/")
async def root():
    """
    Root endpoint - service information.
    """
    return {
        "service": "Worddee.ai Backend",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "practice": "/api/practice",
            "dashboard": "/api/dashboard"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "worddee-backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
