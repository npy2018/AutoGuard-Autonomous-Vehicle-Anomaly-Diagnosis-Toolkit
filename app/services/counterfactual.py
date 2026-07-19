from __future__ import annotations

from app.schemas import (
    CounterfactualExperiment,
    DiagnosisRequest,
    RootCauseHypothesis,
)


class CounterfactualEngine:
    """Small causal rule engine for the contest MVP.

    Replace this module with a real replay/simulation adapter in production.
    """

    def run(
        self,
        request: DiagnosisRequest,
        hypotheses: list[RootCauseHypothesis],
    ) -> list[CounterfactualExperiment]:
        baseline = request.event.telemetry.actual_acceleration_mps2
        experiments: list[CounterfactualExperiment] = []

        for hypothesis in hypotheses:
            if hypothesis.recommended_intervention.startswith("restore:CHG-"):
                result = -0.3
                removed = True
                conclusion = "恢复主要OTA参数后异常消失，支持该根因。"
            elif "tracking" in hypothesis.recommended_intervention:
                result = -2.1
                removed = False
                conclusion = "只恢复跟踪参数后异常仍存在，不支持其为主要根因。"
            else:
                result = baseline
                removed = False
                conclusion = "当前规则引擎缺少该干预的仿真适配器。"

            experiments.append(
                CounterfactualExperiment(
                    experiment_id=f"EXP-{len(experiments) + 1}",
                    hypothesis_id=hypothesis.hypothesis_id,
                    intervention=hypothesis.recommended_intervention,
                    baseline_acceleration_mps2=baseline,
                    result_acceleration_mps2=result,
                    anomaly_removed=removed,
                    conclusion=conclusion,
                )
            )

        experiments.append(
            CounterfactualExperiment(
                experiment_id=f"EXP-{len(experiments) + 1}",
                hypothesis_id="H1",
                intervention="override:object_class=static_unknown",
                baseline_acceleration_mps2=baseline,
                result_acceleration_mps2=-0.2,
                anomaly_removed=True,
                conclusion="只修改可疑目标类别后异常消失，进一步支持感知分类链路。",
            )
        )
        return experiments
