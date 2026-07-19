from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    env: str = os.getenv("AUTOGUARD_ENV", "development")
    data_dir: Path = Path(os.getenv("AUTOGUARD_DATA_DIR", "data"))
    output_dir: Path = Path(os.getenv("AUTOGUARD_OUTPUT_DIR", "outputs"))


settings = Settings()
