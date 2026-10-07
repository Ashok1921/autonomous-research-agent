from app.models.evidence import ResearchEvidence, EvidenceItem
from app.models.fact_check import FactCheckReport, FactCheckResult
from app.agents.mock_report_synthesizer import synthesize_report_mock


question = """
What is the future of Generative AI in Indian healthcare?
"""


research_evidence = [
    ResearchEvidence(
        summary=(
            "Generative AI is being used in healthcare for clinical "
            "documentation and administrative tasks."
        ),
        findings=[
            EvidenceItem(
                claim=(
                    "Generative AI is being used for clinical "
                    "documentation in healthcare."
                ),
                source_title="Athenahealth",
                source_url=(
                    "https://www.athenahealth.com/resources/"
                    "blog/best-practices-for-using-ai-for-clinical-notes"
                ),
                supporting_text=(
                    "Generative AI and ambient documentation tools "
                    "are being used to support clinical note creation."
                ),
                verification_needed=True,
            )
        ],
    )
]


fact_check_report = FactCheckReport(
    results=[
        FactCheckResult(
            claim=(
                "Generative AI is being used for clinical "
                "documentation in healthcare."
            ),
            status="verified",
            evidence_strength="strong",
            source_quality="high",
            source_quality_reason=(
                "The evidence includes established healthcare "
                "organizations and direct documentation use cases."
            ),
            independent_sources=3,
            direct_evidence=True,
            explanation=(
                "The claim is supported by direct evidence of "
                "Generative AI being used for clinical documentation."
            ),
            evidence_limitations=[],
            supporting_sources=[
                (
                    "https://www.athenahealth.com/resources/"
                    "blog/best-practices-for-using-ai-for-clinical-notes"
                )
            ],
            contradicting_sources=[],
        )
    ]
)


result = synthesize_report_mock(
    question,
    research_evidence,
    fact_check_report,
)


print("\n======================================")
print("FINAL RESEARCH REPORT")
print("======================================")

print(f"\nTitle:\n{result.title}")

print(f"\nExecutive Summary:\n{result.executive_summary}")

print("\nKey Findings:")
for item in result.key_findings:
    print(f"- {item}")

print("\nVerified Facts:")
for item in result.verified_facts:
    print(f"- {item}")

print("\nUncertain / Partial Findings:")
for item in result.uncertain_or_partial_findings:
    print(f"- {item}")

print("\nContradicted Claims:")
for item in result.contradicted_claims:
    print(f"- {item}")

print("\nOpportunities:")
for item in result.opportunities:
    print(f"- {item}")

print("\nChallenges:")
for item in result.challenges:
    print(f"- {item}")

print(f"\nFuture Outlook:\n{result.future_outlook}")

print(f"\nConclusion:\n{result.conclusion}")

print("\nSources:")
for source in result.sources:
    print(f"- {source}")