from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.api.routes import router

app = FastAPI(
    title="AutoGuard AI",
    version="0.1.0",
    description="AI-powered anomaly diagnosis toolkit for autonomous vehicle OTA regression",
)
app.include_router(router)


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(Path(__file__).parent / "static" / "index.html")
