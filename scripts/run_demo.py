from __future__ import annotations

from pathlib import Path

from app.schemas import DiagnosisRequest
from app.services.pipeline import DiagnosisPipeline


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    request = DiagnosisRequest.model_validate_json(
        (ROOT / "data" / "demo_request.json").read_text(encoding="utf-8")
    )
    result = DiagnosisPipeline().run(request)

    output_dir = ROOT / "outputs"
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "demo_diagnosis_report.md"
    output_path.write_text(result.markdown_report, encoding="utf-8")

    print(result.markdown_report)
    print(f"\nReport written to: {output_path}")


if __name__ == "__main__":
    main()