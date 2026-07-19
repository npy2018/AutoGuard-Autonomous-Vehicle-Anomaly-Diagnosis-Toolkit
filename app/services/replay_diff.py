from __future__ import annotations

import math

from app.schemas import Divergence, ReplayFrame, ReplayTrace


class ReplayDiffer:
    """Locate the first meaningful divergence between old and new replays."""

    FIELDS = (
        "object_class",
        "object_confidence",
        "crossing_probability",
        "planner_risk_cost",
        "acceleration_command_mps2",
    )

    def compare(self, old: ReplayTrace, new: ReplayTrace) -> Divergence:
        if len(old.frames) != len(new.frames):
            raise ValueError("Old and new replay traces must contain the same number of frames")

        for old_frame, new_frame in zip(old.frames, new.frames, strict=True):
            if not math.isclose(old_frame.timestamp_s, new_frame.timestamp_s, abs_tol=1e-6):
                raise ValueError("Replay frames are not time-aligned")

            divergence = self._frame_divergence(old_frame, new_frame)
            if divergence is not None:
                return divergence

        raise ValueError("No meaningful divergence found")

    def _frame_divergence(self, old: ReplayFrame, new: ReplayFrame) -> Divergence | None:
        if old.object_class != new.object_class:
            return Divergence(
                timestamp_s=new.timestamp_s,
                field="object_class",
                old_value=old.object_class,
                new_value=new.object_class,
                severity=1.0,
                propagation_chain=[
                    "目标分类变化",
                    "横穿概率变化",
                    "规划风险代价变化",
                    "制动指令变化",
                ],
            )

        numeric_thresholds = {
            "object_confidence": 0.15,
            "crossing_probability": 0.2,
            "planner_risk_cost": 0.25,
            "acceleration_command_mps2": 0.8,
        }
        for field, threshold in numeric_thresholds.items():
            old_value = float(getattr(old, field))
            new_value = float(getattr(new, field))
            delta = abs(new_value - old_value)
            if delta >= threshold:
                return Divergence(
                    timestamp_s=new.timestamp_s,
                    field=field,
                    old_value=old_value,
                    new_value=new_value,
                    severity=round(min(1.0, delta / max(threshold, 1e-6)), 3),
                    propagation_chain=[f"{field} 首次显著变化", "下游决策发生偏移"],
                )

        if old.latent_signature and new.latent_signature:
            distance = math.sqrt(
                sum((a - b) ** 2 for a, b in zip(old.latent_signature, new.latent_signature))
            )
            if distance >= 0.5:
                return Divergence(
                    timestamp_s=new.timestamp_s,
                    field="latent_signature",
                    old_value=old.latent_signature,
                    new_value=new.latent_signature,
                    severity=round(min(1.0, distance), 3),
                    propagation_chain=["潜空间表征漂移", "轨迹分布发生变化"],
                )
        return None
