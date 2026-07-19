from __future__ import annotations

from app.schemas import DecisionAdvice, DiagnosisRequest, DiagnosisResult
from app.services.anomaly_detection import AnomalyDetector
from app.services.counterfactual import CounterfactualEngine
from app.services.impact_analysis import ImpactAnalyzer
from app.services.replay_diff import ReplayDiffer
from app.services.report import ReportGenerator
from app.services.root_cause import RootCauseEngine


class DiagnosisPipeline:
    def __init__(self) -> None:
        self.impact = ImpactAnalyzer()
        self.anomaly = AnomalyDetector()
        self.replay = ReplayDiffer()
        self.root_cause = RootCauseEngine()
        self.counterfactual = CounterfactualEngine()
        self.report = ReportGenerator()

    def run(self, request: DiagnosisRequest) -> DiagnosisResult:
        risk_items = self.impact.analyze(request.ota)
        anomaly = self.anomaly.assess(request.event)
        divergence = self.replay.compare(request.old_replay, request.new_replay)
        hypotheses = self.root_cause.generate(
            request.ota,
            divergence,
            request.historical_cases,
        )
        experiments = self.counterfactual.run(request, hypotheses)

        confirmed = any(
            exp.hypothesis_id == "H1" and exp.anomaly_removed for exp in experiments
        )
        if confirmed and anomaly.suspected_software_regression:
            decision = DecisionAdvice(
                action="暂停扩量",
                reasons=[
                    "异常发生于已知场景且未发现显著硬件或传感器混杂因素",
                    "新旧版本存在可定位的首个行为分歧",
                    "反事实实验支持OTA变更与异常制动存在因果关联",
                ],
                next_steps=[
                    "冻结当前灰度比例",
                    "验证时序一致性或参数回调修复方案",
                    "补充真实低置信行人和广告牌场景回归测试",
                    "修复后从1%灰度重新开始",
                ],
            )
        else:
            decision = DecisionAdvice(
                action="人工复核",
                reasons=["现有证据不足以确认版本因果关系"],
                next_steps=["补充数据", "延长观测窗口", "执行更多单变量实验"],
            )

        markdown_report = self.report.render(
            risk_items,
            anomaly,
            divergence,
            hypotheses,
            experiments,
            decision,
        )
        return DiagnosisResult(
            risk_items=risk_items,
            anomaly=anomaly,
            first_divergence=divergence,
            hypotheses=hypotheses,
            experiments=experiments,
            decision=decision,
            markdown_report=markdown_report,
        )
