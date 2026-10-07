from app.graph.nodes import report_synthesizer_node
from app.graph.state import ResearchState
from app.models.evidence import ResearchEvidence, EvidenceItem
from app.models.fact_check import FactCheckReport, FactCheckResult


question = "What is the future of Generative AI in Indian healthcare?"


research_evidence = [
    ResearchEvidence(
        summary=(
            "Generative AI is being used in healthcare "
            "for clinical documentation."
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


state: ResearchState = {
    "question": question,
    "research_plan": None,
    "research_evidence": research_evidence,
    "fact_check_report": fact_check_report,
    "final_report": None,
}


result = report_synthesizer_node(state)


print("\n======================================")
print("REPORT SYNTHESIZER NODE TEST")
print("======================================")

print("\nFinal report exists:", result["final_report"] is not None)

if result["final_report"]:
    report = result["final_report"]

    print("\nTitle:")
    print(report.title)

    print("\nVerified Facts:")
    for item in report.verified_facts:
        print("-", item)

    print("\nSources:")
    for source in report.sources:
        print("-", source)

print("\nNode test completed successfully.")