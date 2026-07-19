from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class OtaChange(BaseModel):
    change_id: str
    component: str
    change_type: Literal["code", "model", "parameter", "calibration", "config"]
    field: str
    old_value: Any
    new_value: Any
    description: str = ""


class OtaPassport(BaseModel):
    ota_version: str
    previous_version: str
    vehicle_model: str
    odd: list[str]
    changes: list[OtaChange]


class SensorHealth(BaseModel):
    camera_occlusion: float = Field(ge=0, le=1)
    camera_overexposure: float = Field(ge=0, le=1)
    radar_health: float = Field(ge=0, le=1)
    calibration_ok: bool
    time_sync_ok: bool


class HardwareHealth(BaseModel):
    brake_ok: bool
    steering_ok: bool
    tire_pressure_ok: bool


class SceneContext(BaseModel):
    weather: str
    lighting: str
    road_type: str
    object_type: str
    known_scene: bool = True


class Telemetry(BaseModel):
    speed_mps: float
    actual_acceleration_mps2: float
    expected_acceleration_min_mps2: float
    expected_acceleration_max_mps2: float
    jerk_mps3: float
    min_ttc_s: float


class EventPacket(BaseModel):
    event_id: str
    timestamp: str
    ota_version: str
    scene: SceneContext
    telemetry: Telemetry
    sensor_health: SensorHealth
    hardware_health: HardwareHealth


class ReplayFrame(BaseModel):
    timestamp_s: float
    object_class: str
    object_confidence: float
    crossing_probability: float
    planner_risk_cost: float
    acceleration_command_mps2: float
    latent_signature: list[float] = Field(default_factory=list)


class ReplayTrace(BaseModel):
    version: str
    frames: list[ReplayFrame]


class HistoricalCase(BaseModel):
    case_id: str
    title: str
    description: str
    root_cause: str
    fix: str


class DiagnosisRequest(BaseModel):
    ota: OtaPassport
    event: EventPacket
    old_replay: ReplayTrace
    new_replay: ReplayTrace
    historical_cases: list[HistoricalCase] = Field(default_factory=list)


class EvidenceRef(BaseModel):
    source: str
    locator: str
    value: Any


class RiskItem(BaseModel):
    change_id: str
    affected_function: str
    risk_scene: list[str]
    possible_behavior: list[str]
    risk_level: Literal["低", "中", "高"]
    rationale: str


class AnomalyAssessment(BaseModel):
    event_type: str
    behavior_deviation: float
    ood_score: float
    safety_risk: float
    confounders: list[str]
    suspected_software_regression: bool


class Divergence(BaseModel):
    timestamp_s: float
    field: str
    old_value: Any
    new_value: Any
    severity: float
    propagation_chain: list[str]


class RootCauseHypothesis(BaseModel):
    hypothesis_id: str
    statement: str
    confidence: float
    support: list[EvidenceRef]
    counter_evidence: list[str]
    falsifiable_prediction: str
    recommended_intervention: str


class CounterfactualExperiment(BaseModel):
    experiment_id: str
    hypothesis_id: str
    intervention: str
    baseline_acceleration_mps2: float
    result_acceleration_mps2: float
    anomaly_removed: bool
    conclusion: str


class DecisionAdvice(BaseModel):
    action: Literal["继续灰度", "暂停扩量", "回滚", "人工复核"]
    reasons: list[str]
    next_steps: list[str]


class DiagnosisResult(BaseModel):
    risk_items: list[RiskItem]
    anomaly: AnomalyAssessment
    first_divergence: Divergence
    hypotheses: list[RootCauseHypothesis]
    experiments: list[CounterfactualExperiment]
    decision: DecisionAdvice
    markdown_report: str
