
from app.models.evidence import ResearchEvidence, EvidenceItem
from app.models.fact_check import FactCheckReport, FactCheckResult
from app.graph.state import ResearchState
from app.agents.report_synthesizer import synthesize_report

from langgraph.graph import StateGraph, START, END


question = "What is the future of Generative AI in Indian healthcare?"


# ============================================================
# MOCK DATA
# ============================================================

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


# ============================================================
# MOCK NODES
# ============================================================

def mock_planner(state: ResearchState):
    print("\n[MOCK PLANNER]")
    print("Planner skipped — using existing mock research data.")

    return {
        "research_plan": {
            "objective": (
                "Assess the future of Generative AI "
                "in Indian healthcare."
            ),
            "tasks": [
                "Identify current healthcare applications",
                "Evaluate opportunities",
                "Identify challenges",
                "Assess future outlook",
            ],
        }
    }


def mock_web_researcher(state: ResearchState):
    print("\n[MOCK WEB RESEARCHER]")
    print("Web research skipped — using existing mock evidence.")

    return {
        "research_evidence": research_evidence
    }


def mock_fact_checker(state: ResearchState):
    print("\n[MOCK FACT CHECKER]")
    print("Fact checking skipped — using existing mock report.")

    return {
        "fact_check_report": fact_check_report
    }


# ============================================================
# REPORT SYNTHESIZER NODE WRAPPER
# ============================================================

def report_synthesizer_node(state: ResearchState):
    print("\n[REPORT SYNTHESIZER]")
    print("Calling existing synthesize_report()...")

    final_report = synthesize_report(
        question=state["question"],
        research_evidence=state["research_evidence"],
        fact_check_report=state["fact_check_report"],
    )

    return {
        "final_report": final_report
    }


# ============================================================
# BUILD MOCK GRAPH
# ============================================================

print("\n======================================")
print("MOCK LANGGRAPH WORKFLOW TEST")
print("======================================")


print("\nBuilding mock graph...")


builder = StateGraph(ResearchState)

builder.add_node("planner", mock_planner)
builder.add_node("web_researcher", mock_web_researcher)
builder.add_node("fact_checker", mock_fact_checker)
builder.add_node("report_synthesizer", report_synthesizer_node)


builder.add_edge(START, "planner")
builder.add_edge("planner", "web_researcher")
builder.add_edge("web_researcher", "fact_checker")
builder.add_edge("fact_checker", "report_synthesizer")
builder.add_edge("report_synthesizer", END)


graph = builder.compile()


print("Mock graph compiled successfully.")


# ============================================================
# INITIAL STATE
# ============================================================

initial_state = {
    "question": question,
    "research_plan": None,
    "research_evidence": research_evidence,
    "fact_check_report": fact_check_report,
    "final_report": None,
}


# ============================================================
# INVOKE GRAPH
# ============================================================

print("\nInvoking mock workflow...")
print("Gemini Planner: SKIPPED")
print("Tavily Web Research: SKIPPED")
print("Gemini Fact Checker: SKIPPED")
print("Report Synthesizer: RUNNING")
print()


result = graph.invoke(initial_state)


# ============================================================
# RESULT
# ============================================================

print("\n======================================")
print("WORKFLOW COMPLETED")
print("======================================")


final_report = result.get("final_report")


if final_report is None:
    print("\nERROR: final_report is None")
else:
    print("\nFinal report generated successfully!")

    print("\nTITLE:")
    print(final_report.title)

    print("\nEXECUTIVE SUMMARY:")
    print(final_report.executive_summary)

    print("\nKEY FINDINGS:")
    for finding in final_report.key_findings:
        print(f"- {finding}")

    print("\nVERIFIED FACTS:")
    for fact in final_report.verified_facts:
        print(f"- {fact}")

    print("\nUNCERTAIN / PARTIAL FINDINGS:")
    for item in final_report.uncertain_or_partial_findings:
        print(f"- {item}")

    print("\nCONCLUSION:")
    print(final_report.conclusion)

    print("\nSOURCES:")
    for source in final_report.sources:
        print(f"- {source}")
