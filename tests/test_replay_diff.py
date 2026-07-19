from pathlib import Path

from app.schemas import DiagnosisRequest
from app.services.replay_diff import ReplayDiffer


def test_first_divergence_is_object_class() -> None:
    request = DiagnosisRequest.model_validate_json(
        Path("data/demo_request.json").read_text(encoding="utf-8")
    )
    result = ReplayDiffer().compare(request.old_replay, request.new_replay)
    assert result.timestamp_s == 12.34
    assert result.field == "object_class"
    assert result.old_value == "static_unknown"
    assert result.new_value == "pedestrian"
