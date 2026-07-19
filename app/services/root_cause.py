from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.schemas import (
    Divergence,
    EvidenceRef,
    HistoricalCase,
    OtaPassport,
    RootCauseHypothesis,
)


class HistoricalCaseRetriever:
    def retrieve(
        self,
        query: str,
        cases: list[HistoricalCase],
        top_k: int = 2,
    ) -> list[HistoricalCase]:
        if not cases:
            return []
        corpus = [f"{c.title} {c.description} {c.root_cause}" for c in cases]
        matrix = TfidfVectorizer().fit_transform([query, *corpus])
        scores = cosine_similarity(matrix[0:1], matrix[1:]).flatten()
        ranked = scores.argsort()[::-1][:top_k]
        return [cases[int(index)] for index in ranked if scores[int(index)] > 0]


class RootCauseEngine:
    """Generate evidence-grounded, falsifiable root-cause candidates."""

    def __init__(self) -> None:
        self.retriever = HistoricalCaseRetriever()

    def generate(
        self,
        ota: OtaPassport,
        divergence: Divergence,
        cases: list[HistoricalCase],
    ) -> list[RootCauseHypothesis]:
        change = self._best_matching_change(ota, divergence)
        query = f"{change.description} {divergence.field} {divergence.new_value}"
        similar_cases = self.retriever.retrieve(query, cases)

        support = [
            EvidenceRef(
                source="replay_diff",
                locator=f"timestamp={divergence.timestamp_s}s/{divergence.field}",
                value={"old": divergence.old_value, "new": divergence.new_value},
            ),
            EvidenceRef(
                source="ota_passport",
                locator=f"change_id={change.change_id}/{change.field}",
                value={"old": change.old_value, "new": change.new_value},
            ),
        ]
        for case in similar_cases:
            support.append(
                EvidenceRef(
                    source="historical_case",
                    locator=f"case_id={case.case_id}",
                    value=case.root_cause,
                )
            )

        primary = RootCauseHypothesis(
            hypothesis_id="H1",
            statement=(
                f"{change.field} 的版本变化导致 {divergence.field} 首次分歧，"
                "并沿决策链传播为异常制动。"
            ),
            confidence=round(min(0.92, 0.68 + 0.06 * len(similar_cases)), 2),
            support=support,
            counter_evidence=["仍需通过单变量回放排除跟踪参数和环境噪声。"],
            falsifiable_prediction=(
                f"若恢复 {change.field} 的旧值，则同源回放中的异常制动应明显减弱或消失。"
            ),
            recommended_intervention=f"restore:{change.change_id}",
        )

        secondary = RootCauseHypothesis(
            hypothesis_id="H2",
            statement="目标跟踪持续时间或跨帧一致性变化放大了单帧误识别。",
            confidence=0.46,
            support=[support[0]],
            counter_evidence=["当前OTA数字护照中未发现明确的跟踪参数变更。"],
            falsifiable_prediction="若只恢复旧跟踪参数，异常制动应消失。",
            recommended_intervention="restore:tracking_persistence",
        )
        return [primary, secondary]

    @staticmethod
    def _best_matching_change(ota: OtaPassport, divergence: Divergence):
        for change in ota.changes:
            text = f"{change.field} {change.description}".lower()
            if divergence.field == "object_class" and ("pedestrian" in text or "行人" in text):
                return change
        return ota.changes[0]
