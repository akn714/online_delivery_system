from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routes import orders

load_dotenv()

app = FastAPI(
    title="Online Delivery System API",
    description="Backend API for Online Delivery Registration System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(orders.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Online Delivery System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 4000))

    uvicorn.run("main:app", host="0.0.0.0", port=port)