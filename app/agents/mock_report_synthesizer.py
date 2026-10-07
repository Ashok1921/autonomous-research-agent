from app.models.final_report import FinalResearchReport
from app.models.evidence import ResearchEvidence
from app.models.fact_check import FactCheckReport


def synthesize_report_mock(
    question: str,
    research_evidence: list[ResearchEvidence],
    fact_check_report: FactCheckReport,
) -> FinalResearchReport:

    verified_facts = []
    uncertain_findings = []
    contradicted_claims = []
    sources = []

    # Process fact-check results
    for result in fact_check_report.results:

        if result.status == "verified":
            verified_facts.append(result.claim)

        elif result.status == "partially_verified":
            uncertain_findings.append(result.claim)

        elif result.status == "contradicted":
            contradicted_claims.append(result.claim)

        # Collect supporting sources
        for source in result.supporting_sources:
            if source not in sources:
                sources.append(source)

        # Collect contradicting sources
        for source in result.contradicting_sources:
            if source not in sources:
                sources.append(source)

    # Collect sources from research evidence
    for evidence in research_evidence:
        for item in evidence.findings:
            if item.source_url and item.source_url not in sources:
                sources.append(item.source_url)

    key_findings = []

    for evidence in research_evidence:
        for item in evidence.findings:
            key_findings.append(item.claim)

    opportunities = [
        "Clinical documentation support",
        "Administrative workload reduction",
        "AI-assisted healthcare workflows",
    ]

    challenges = [
        "Evidence quality and verification",
        "Patient data privacy and security",
        "Clinical safety and human oversight",
        "Regulatory and governance requirements",
    ]

    return FinalResearchReport(
        title="The Future of Generative AI in Indian Healthcare",

        executive_summary=(
            "Generative AI has potential applications in healthcare, "
            "including clinical documentation and administrative support. "
            "The available evidence indicates that these applications "
            "should be evaluated carefully with attention to evidence "
            "quality, patient safety, privacy, and regulatory requirements."
        ),

        key_findings=key_findings,

        verified_facts=verified_facts,

        uncertain_or_partial_findings=uncertain_findings,

        contradicted_claims=contradicted_claims,

        opportunities=opportunities,

        challenges=challenges,

        future_outlook=(
            "The future development of Generative AI in Indian healthcare "
            "will depend on clinical validation, responsible deployment, "
            "data governance, regulatory frameworks, and integration with "
            "existing healthcare workflows. The supplied evidence alone "
            "is insufficient to make precise long-term adoption forecasts."
        ),

        conclusion=(
            "Generative AI presents potential opportunities for improving "
            "healthcare workflows, but further evidence is required to "
            "determine its long-term impact in India. Deployment should "
            "maintain appropriate human oversight and evidence-based "
            "evaluation."
        ),

        sources=sources,
    )