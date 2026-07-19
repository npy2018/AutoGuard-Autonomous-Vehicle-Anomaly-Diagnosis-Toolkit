from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.config import settings
from app.schemas import DiagnosisRequest, DiagnosisResult
from app.services.pipeline import DiagnosisPipeline

router = APIRouter(prefix="/api/v1")
pipeline = DiagnosisPipeline()


def _load_demo_request(data_dir: Path) -> DiagnosisRequest:
    path = data_dir / "demo_request.json"
    if not path.exists():
        raise FileNotFoundError(f"Demo data not found: {path}")
    return DiagnosisRequest.model_validate_json(path.read_text(encoding="utf-8"))


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/analyze", response_model=DiagnosisResult)
def analyze(request: DiagnosisRequest) -> DiagnosisResult:
    try:
        return pipeline.run(request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/demo", response_model=DiagnosisResult)
def demo() -> DiagnosisResult:
    try:
        request = _load_demo_request(settings.data_dir)
        return pipeline.run(request)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
