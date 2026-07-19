from pathlib import Path

from app.schemas import DiagnosisRequest
from app.services.pipeline import DiagnosisPipeline


def test_primary_counterfactual_removes_anomaly() -> None:
    request = DiagnosisRequest.model_validate_json(
        Path("data/demo_request.json").read_text(encoding="utf-8")
    )
    result = DiagnosisPipeline().run(request)
    primary = next(exp for exp in result.experiments if exp.hypothesis_id == "H1")
    assert primary.anomaly_removed is True
    assert result.decision.action == "暂停扩量"
