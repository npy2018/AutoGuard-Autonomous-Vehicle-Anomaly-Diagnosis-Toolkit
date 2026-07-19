from pathlib import Path

from app.schemas import DiagnosisRequest
from app.services.impact_analysis import ImpactAnalyzer


def load_request() -> DiagnosisRequest:
    return DiagnosisRequest.model_validate_json(
        Path("data/demo_request.json").read_text(encoding="utf-8")
    )


def test_pedestrian_change_is_high_risk() -> None:
    risks = ImpactAnalyzer().analyze(load_request().ota)
    assert risks[0].risk_level == "高"
    assert "异常急刹" in risks[0].possible_behavior
