from __future__ import annotations

from app.schemas import (
    AnomalyAssessment,
    CounterfactualExperiment,
    DecisionAdvice,
    Divergence,
    RiskItem,
    RootCauseHypothesis,
)


class ReportGenerator:
    def render(
        self,
        risk_items: list[RiskItem],
        anomaly: AnomalyAssessment,
        divergence: Divergence,
        hypotheses: list[RootCauseHypothesis],
        experiments: list[CounterfactualExperiment],
        decision: DecisionAdvice,
    ) -> str:
        lines = [
            "# AutoGuard AI 异常诊断报告",
            "",
            "## 1. OTA风险摘要",
        ]
        for item in risk_items:
            lines.append(
                f"- **{item.change_id}｜{item.risk_level}风险**：{item.affected_function}；"
                f"场景：{'、'.join(item.risk_scene)}；理由：{item.rationale}"
            )

        lines.extend(
            [
                "",
                "## 2. 异常评估",
                f"- 事件类型：{anomaly.event_type}",
                f"- 行为偏离：{anomaly.behavior_deviation}",
                f"- OOD分数：{anomaly.ood_score}",
                f"- 安全风险：{anomaly.safety_risk}",
                f"- 混杂因素：{'、'.join(anomaly.confounders) if anomaly.confounders else '未发现'}",
                f"- 疑似软件回归：{'是' if anomaly.suspected_software_regression else '否'}",
                "",
                "## 3. 首个版本分歧",
                f"- 时间：{divergence.timestamp_s}s",
                f"- 字段：{divergence.field}",
                f"- 旧版本：{divergence.old_value}",
                f"- 新版本：{divergence.new_value}",
                f"- 传播链：{' → '.join(divergence.propagation_chain)}",
                "",
                "## 4. 根因候选",
            ]
        )
        for hypothesis in hypotheses:
            lines.extend(
                [
                    f"### {hypothesis.hypothesis_id}（置信度 {hypothesis.confidence:.0%}）",
                    hypothesis.statement,
                    "",
                    "证据：",
                ]
            )
            for evidence in hypothesis.support:
                lines.append(f"- `{evidence.source}` / `{evidence.locator}`：{evidence.value}")
            lines.extend(
                [
                    f"- 反证：{'；'.join(hypothesis.counter_evidence)}",
                    f"- 可证伪预测：{hypothesis.falsifiable_prediction}",
                    "",
                ]
            )

        lines.extend(["## 5. 反事实实验"])
        for experiment in experiments:
            lines.append(
                f"- **{experiment.experiment_id}**：{experiment.intervention}；"
                f"{experiment.baseline_acceleration_mps2} → "
                f"{experiment.result_acceleration_mps2} m/s²；{experiment.conclusion}"
            )

        lines.extend(
            [
                "",
                "## 6. 发布建议",
                f"- 建议动作：**{decision.action}**",
                f"- 理由：{'；'.join(decision.reasons)}",
                f"- 下一步：{'；'.join(decision.next_steps)}",
                "",
                "> 本报告为技术诊断建议，不替代研发、质量、安全或法规负责人作最终判断。",
            ]
        )
        return "\n".join(lines)
