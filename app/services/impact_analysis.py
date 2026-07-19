from __future__ import annotations

from app.schemas import OtaPassport, RiskItem


class ImpactAnalyzer:
    """Convert OTA changes into structured function-scene-behavior risks."""

    def analyze(self, ota: OtaPassport) -> list[RiskItem]:
        risks: list[RiskItem] = []
        for change in ota.changes:
            text = f"{change.component} {change.field} {change.description}".lower()

            if "pedestrian" in text or "行人" in text:
                risks.append(
                    RiskItem(
                        change_id=change.change_id,
                        affected_function="行人识别与制动决策",
                        risk_scene=["雨夜反光", "广告牌", "施工围挡", "低置信行人"],
                        possible_behavior=["误识别", "无故减速", "异常急刹"],
                        risk_level="高",
                        rationale=(
                            f"{change.field} 从 {change.old_value} 调整为 {change.new_value}，"
                            "可能改变低置信目标进入高风险规划链路的概率。"
                        ),
                    )
                )
            elif "planner" in text or "规划" in text:
                risks.append(
                    RiskItem(
                        change_id=change.change_id,
                        affected_function="轨迹规划与风险代价计算",
                        risk_scene=["拥堵跟车", "窄路会车", "施工绕行"],
                        possible_behavior=["过度保守", "无效等待", "异常绕行"],
                        risk_level="中",
                        rationale="规划相关变化可能放大上游感知误差并改变最终轨迹。",
                    )
                )
            else:
                risks.append(
                    RiskItem(
                        change_id=change.change_id,
                        affected_function=change.component,
                        risk_scene=["需要结合历史案例进一步筛选"],
                        possible_behavior=["潜在性能漂移"],
                        risk_level="中",
                        rationale="检测到版本变化，但当前知识库中缺少足够具体的映射。",
                    )
                )
        return risks
