from fastapi import FastAPI
import uvicorn

from .routers import sensors, metrics

app = FastAPI(root_path="/api", redirect_slashes=False)

app.include_router(sensors.router, tags=["Sensors"], prefix="/sensors")
app.include_router(metrics.router, tags=["Metrics"], prefix="/metrics")


@app.get("")
async def read_root():
    return f"hello, I am the backend, I speak for the trees."


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
