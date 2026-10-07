from typing import Literal

from pydantic import BaseModel, Field


VerificationStatus = Literal[
    "verified",
    "partially_verified",
    "unverified",
    "contradicted",
]

EvidenceStrength = Literal[
    "strong",
    "moderate",
    "weak",
    "insufficient",
]

SourceQuality = Literal[
    "high",
    "medium",
    "low",
    "mixed",
]


class FactCheckResult(BaseModel):
    claim: str = Field(
        description="The claim being checked."
    )

    status: VerificationStatus = Field(
        description="Overall verification status of the claim."
    )

    evidence_strength: EvidenceStrength = Field(
        description="Overall strength of the evidence supporting the verification decision."
    )

    source_quality: SourceQuality = Field(
        description="Overall quality of the sources used to evaluate the claim."
    )

    source_quality_reason: str = Field(
        description="Explanation of why the sources were judged to have this quality."
    )

    independent_sources: int = Field(
        description="Approximate number of genuinely independent sources providing meaningful evidence."
    )

    direct_evidence: bool = Field(
        description="Whether the evidence directly supports the actual claim."
    )

    explanation: str = Field(
        description="Why the claim received this verification status and evidence assessment."
    )

    evidence_limitations: list[str] = Field(
        description="Important limitations, uncertainties, geographic limitations, temporal limitations, or evidence gaps."
    )

    supporting_sources: list[str] = Field(
        description="URLs supporting the claim."
    )

    contradicting_sources: list[str] = Field(
        description="URLs that contradict or challenge the claim."
    )


class FactCheckReport(BaseModel):
    results: list[FactCheckResult] = Field(
        description="Fact-checking results for the supplied claims."
    )