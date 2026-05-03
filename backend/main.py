from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routes import orders, auth, catalog, config
from connection_manager import manager

load_dotenv()

app = FastAPI(
    title="Rocket07 Delivery Service API",
    description="Backend API for Rocket07 Delivery Service",
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
app.include_router(auth.router)
app.include_router(orders.router)
app.include_router(catalog.router)
app.include_router(config.router)


@app.websocket("/ws/orders")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time order updates."""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Rocket07 Delivery Service API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 4000))

    uvicorn.run("main:app", host="0.0.0.0", port=port)