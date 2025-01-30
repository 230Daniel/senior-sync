import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

# Do this before importing our files, as some read environment variables on startup.
load_dotenv()

from .routers import sensors, metrics, alerts

logging.basicConfig(level=logging.INFO)

app = FastAPI(root_path="/api", redirect_slashes=False)

# CORS used in development to allow frontend on different domain to talk to the backend.
if origins := os.getenv("CORS_ALLOWED_ORIGINS"):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins.split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(sensors.router, tags=["Sensors"], prefix="/sensors")
app.include_router(metrics.router, tags=["Metrics"], prefix="/metrics")
app.include_router(alerts.router, tags=["Alerts"], prefix="/alerts")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
