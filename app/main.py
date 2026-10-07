from app.graph.workflow import build_research_graph
from app.utils.report_saver import save_report


def main():
    question = """
    What is the future of Generative AI in Indian healthcare?
    """

    graph = build_research_graph()

    initial_state = {
        "question": question,
        "research_plan": None,
        "research_evidence": [],
        "fact_check_report": None,
        "final_report": None,
        "status": "started",
        "error_message": None,
    }

    print("\n======================================")
    print("AUTONOMOUS RESEARCH AGENT")
    print("======================================")

    result = graph.invoke(initial_state)

    status = result["status"]

    print("\n======================================")
    print("WORKFLOW STATUS")
    print("======================================")

    print(f"\nStatus: {status}")

    # Stop cleanly if any stage failed
    if status != "completed":
        print("\n======================================")
        print("WORKFLOW ERROR")
        print("======================================")

        print(f"\nError: {result['error_message']}")

        print("\nThe workflow stopped safely.")
        return

    # --------------------------------------
    # RESEARCH PLAN
    # --------------------------------------

    print("\n======================================")
    print("RESEARCH PLAN")
    print("======================================")

    plan = result["research_plan"]

    print(f"\nObjective:\n{plan.objective}")

    print("\nTasks:")
    for index, task in enumerate(plan.tasks, start=1):
        print(f"{index}. {task}")

    # --------------------------------------
    # RESEARCH EVIDENCE
    # --------------------------------------

    print("\n======================================")
    print("RESEARCH EVIDENCE")
    print("======================================")

    evidence = result["research_evidence"]

    for index, research in enumerate(evidence, start=1):
        print(f"\n--- Research Task {index} ---")
        print(f"Summary: {research.summary}")

        for finding in research.findings:
            print(f"\nClaim: {finding.claim}")
            print(f"Source: {finding.source_title}")
            print(f"URL: {finding.source_url}")
            print(
                f"Verification needed: "
                f"{finding.verification_needed}"
            )

    # --------------------------------------
    # FACT CHECK REPORT
    # --------------------------------------

    print("\n======================================")
    print("FACT CHECK REPORT")
    print("======================================")

    fact_check_report = result["fact_check_report"]

    for index, item in enumerate(
        fact_check_report.results,
        start=1,
    ):
        print(f"\n--- Claim {index} ---")
        print(f"Claim: {item.claim}")
        print(f"Status: {item.status}")
        print(f"Explanation: {item.explanation}")

        print("\nSupporting sources:")
        for source in item.supporting_sources:
            print(f"- {source}")

        print("\nContradicting sources:")
        for source in item.contradicting_sources:
            print(f"- {source}")

    # --------------------------------------
    # FINAL REPORT
    # --------------------------------------

    print("\n======================================")
    print("FINAL RESEARCH REPORT")
    print("======================================")

    final_report = result["final_report"]
    
    report_path = save_report(final_report)

    print(f"\nReport saved to: {report_path}")

    print(f"\nTitle:\n{final_report.title}")

    print(f"\nExecutive Summary:\n{final_report.executive_summary}")

    print("\nKey Findings:")
    for finding in final_report.key_findings:
        print(f"- {finding}")

    print("\nVerified Facts:")
    for fact in final_report.verified_facts:
        print(f"- {fact}")

    print("\nUncertain / Partial Findings:")
    for finding in final_report.uncertain_or_partial_findings:
        print(f"- {finding}")

    print("\nContradicted Claims:")
    for claim in final_report.contradicted_claims:
        print(f"- {claim}")

    print("\nOpportunities:")
    for opportunity in final_report.opportunities:
        print(f"- {opportunity}")

    print("\nChallenges:")
    for challenge in final_report.challenges:
        print(f"- {challenge}")

    print(f"\nFuture Outlook:\n{final_report.future_outlook}")

    print(f"\nConclusion:\n{final_report.conclusion}")

    print("\nSources:")
    for source in final_report.sources:
        print(f"- {source}")

    print("\n======================================")
    print("RESEARCH COMPLETED SUCCESSFULLY")
    print("======================================")


if __name__ == "__main__":
    main()