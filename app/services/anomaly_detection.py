from __future__ import annotations

from app.schemas import AnomalyAssessment, EventPacket


class AnomalyDetector:
    """Explainable anomaly score with confounder filtering."""

    def assess(self, event: EventPacket) -> AnomalyAssessment:
        telemetry = event.telemetry
        if telemetry.actual_acceleration_mps2 < telemetry.expected_acceleration_min_mps2:
            gap = telemetry.expected_acceleration_min_mps2 - telemetry.actual_acceleration_mps2
        elif telemetry.actual_acceleration_mps2 > telemetry.expected_acceleration_max_mps2:
            gap = telemetry.actual_acceleration_mps2 - telemetry.expected_acceleration_max_mps2
        else:
            gap = 0.0

        behavior_deviation = min(1.0, gap / 2.5 + abs(telemetry.jerk_mps3) / 20.0)
        ood_score = 0.2 if event.scene.known_scene else 0.8
        ttc_risk = 0.0 if telemetry.min_ttc_s >= 4 else min(1.0, (4 - telemetry.min_ttc_s) / 4)
        safety_risk = min(1.0, 0.65 * behavior_deviation + 0.35 * ttc_risk)

        confounders: list[str] = []
        if event.sensor_health.camera_occlusion > 0.35:
            confounders.append("摄像头遮挡")
        if event.sensor_health.camera_overexposure > 0.5:
            confounders.append("摄像头过曝")
        if event.sensor_health.radar_health < 0.7:
            confounders.append("雷达健康度偏低")
        if not event.sensor_health.calibration_ok:
            confounders.append("传感器标定异常")
        if not event.sensor_health.time_sync_ok:
            confounders.append("传感器时间同步异常")
        if not event.hardware_health.brake_ok:
            confounders.append("制动硬件异常")
        if not event.hardware_health.steering_ok:
            confounders.append("转向硬件异常")
        if not event.hardware_health.tire_pressure_ok:
            confounders.append("胎压异常")

        return AnomalyAssessment(
            event_type="异常急刹" if telemetry.actual_acceleration_mps2 < -1.5 else "行为偏离",
            behavior_deviation=round(behavior_deviation, 3),
            ood_score=round(ood_score, 3),
            safety_risk=round(safety_risk, 3),
            confounders=confounders,
            suspected_software_regression=(
                behavior_deviation >= 0.6 and ood_score < 0.6 and not confounders
            ),
        )
