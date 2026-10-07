from app.agents.planner import create_research_plan
from app.agents.web_researcher import research_task
from app.agents.fact_checker import fact_check_claims
from app.graph.state import ResearchState
from app.agents.report_synthesizer import synthesize_report
from app.utils.checkpoint import save_research_evidence
from app.utils.checkpoint import save_research_evidence, load_research_evidence
from app.models.evidence import ResearchEvidence


def planner_node(state: ResearchState) -> ResearchState:
    question = state["question"]

    try:
        research_plan = create_research_plan(question)

        return {
            **state,
            "research_plan": research_plan,
            "research_evidence": [],
            "fact_check_report": None,
            "status": "planner_completed",
            "error_message": None,
        }

    except Exception as exc:
        return {
            **state,
            "status": "planner_failed",
            "error_message": str(exc),
        }
        
def resume_research_node(state: ResearchState) -> ResearchState:
    try:
        saved_evidence = load_research_evidence()

        evidence = [
            ResearchEvidence.model_validate(item)
            for item in saved_evidence
        ]

        print(
            f"\n[Checkpoint] Resumed "
            f"{len(evidence)} research evidence items."
        )

        return {
            **state,
            "research_evidence": evidence,
            "status": "web_research_completed",
            "error_message": None,
        }

    except Exception as exc:
        return {
            **state,
            "status": "web_research_failed",
            "error_message": f"Failed to load research checkpoint: {exc}",
        }

        


def web_research_node(state: ResearchState) -> ResearchState:
    research_plan = state["research_plan"]

    if research_plan is None:
        return {
            **state,
            "status": "web_research_failed",
            "error_message": "Research plan is missing.",
        }

    evidence = []

    try:
        for task in research_plan.tasks:
            print(f"\n[Web Research] {task}")

            result = research_task(task)

            evidence.append(result)

            print(
                f"[Web Research] Completed "
                f"{len(evidence)}/{len(research_plan.tasks)} tasks"
            )

            # Save progress after every completed research task.
            save_research_evidence(evidence)

        return {
            **state,
            "research_evidence": evidence,
            "status": "web_research_completed",
            "error_message": None,
        }

    except Exception as exc:
        # Preserve whatever research completed before the failure.
        if evidence:
            save_research_evidence(evidence)

        return {
            **state,
            "research_evidence": evidence,
            "status": "web_research_failed",
            "error_message": str(exc),
        }


def fact_checker_node(state: ResearchState) -> ResearchState:
    research_evidence = state["research_evidence"]

    if not research_evidence:
        return {
            **state,
            "status": "fact_checker_failed",
            "error_message": "Research evidence is missing.",
        }

    claims = []

    for evidence in research_evidence:
        for finding in evidence.findings:
            claims.append(finding.claim)

    print(f"\n[Fact Checker] Checking {len(claims)} claims...")

    try:
        fact_check_report = fact_check_claims(claims)

        return {
            **state,
            "fact_check_report": fact_check_report,
            "status": "fact_checker_completed",
            "error_message": None,
        }

    except Exception as exc:
        return {
            **state,
            "status": "fact_checker_failed",
            "error_message": str(exc),
        }


def report_synthesizer_node(state: ResearchState) -> ResearchState:
    question = state["question"]
    research_evidence = state["research_evidence"]
    fact_check_report = state["fact_check_report"]

    if not research_evidence:
        return {
            **state,
            "status": "report_synthesizer_failed",
            "error_message": "Research evidence is missing.",
        }

    if fact_check_report is None:
        return {
            **state,
            "status": "report_synthesizer_failed",
            "error_message": "Fact check report is missing.",
        }

    print("\n[Report Synthesizer] Generating final report...")

    try:
        final_report = synthesize_report(
            question=question,
            research_evidence=research_evidence,
            fact_check_report=fact_check_report,
        )

        return {
            **state,
            "final_report": final_report,
            "status": "completed",
            "error_message": None,
        }

    except Exception as exc:
        return {
            **state,
            "status": "report_synthesizer_failed",
            "error_message": str(exc),
        }